#!/usr/bin/env python3
"""用 ffmpeg 将幻灯片截图 + TTS 音频合成为最终视频。"""
import argparse
import json
import os
import sys
import subprocess
import asyncio


def check_ffmpeg():
    """检查 ffmpeg 和 ffprobe 是否可用。"""
    for cmd in ["ffmpeg", "ffprobe"]:
        result = subprocess.run(["which", cmd], capture_output=True)
        if result.returncode != 0:
            print(f"Error: {cmd} not found. Install with: brew install ffmpeg")
            sys.exit(1)


def get_audio_duration(path):
    """获取音频文件时长（秒）。"""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 3.0  # fallback: 3 seconds


def generate_silence(duration, output_path):
    """生成指定时长的静音 MP3 文件。"""
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
        "-t", str(duration), "-c:a", "libmp3lame", "-b:a", "192k",
        output_path
    ], capture_output=True)


def build_video(args):
    """主函数：截图 + 音频 → 视频片段 → 合并。"""
    check_ffmpeg()

    screenshots_dir = os.path.abspath(args.screenshots)
    audio_dir = os.path.abspath(args.audio)
    output_path = os.path.abspath(args.output)

    if not os.path.isdir(screenshots_dir):
        print(f"Error: Screenshots directory not found: {screenshots_dir}")
        sys.exit(1)
    if not os.path.isdir(audio_dir):
        print(f"Error: Audio directory not found: {audio_dir}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Discover slides
    slide_files = sorted([
        f for f in os.listdir(screenshots_dir)
        if f.startswith("slide_") and f.endswith(".png")
    ])

    if not slide_files:
        print("Error: No slide_*.png files found in screenshots directory")
        sys.exit(1)

    # Load manifest if available (for pre-computed durations)
    manifest_path = os.path.join(audio_dir, "manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            data = json.load(f)
            for item in data.get("slides", []):
                manifest[item["slide_number"]] = item["duration"]

    # Segments directory
    segments_dir = os.path.join(screenshots_dir, "_segments")
    os.makedirs(segments_dir, exist_ok=True)

    segments = []
    total_slides = len(slide_files)

    for idx, slide_file in enumerate(slide_files):
        slide_num = idx + 1
        slide_path = os.path.join(screenshots_dir, slide_file)

        # Find corresponding audio (support both 001 and 01 numbering)
        audio_file = None
        for fmt in [f"slide_{slide_num:03d}.mp3", f"slide_{slide_num:02d}.mp3"]:
            candidate = os.path.join(audio_dir, fmt)
            if os.path.exists(candidate):
                audio_file = candidate
                break

        # Generate silence if no audio
        if not audio_file:
            silence_path = os.path.join(segments_dir, f"silence_{slide_num:03d}.mp3")
            generate_silence(3.0, silence_path)
            audio_file = silence_path

        # Get duration
        if slide_num in manifest:
            duration = manifest[slide_num]
        else:
            duration = get_audio_duration(audio_file)

        duration += args.gap  # Add inter-slide gap

        seg_path = os.path.join(segments_dir, f"segment_{slide_num:03d}.mp4")
        w, h = args.width, args.height

        print(f"  [{slide_num}/{total_slides}] Building segment ({duration:.1f}s)...")

        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", slide_path,
            "-i", audio_file,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-t", str(duration),
            "-shortest",
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black",
            seg_path
        ], capture_output=True)

        if os.path.exists(seg_path):
            segments.append(seg_path)
        else:
            print(f"  Warning: Failed to create segment for slide {slide_num}")

    if not segments:
        print("Error: No segments were created!")
        sys.exit(1)

    # Concatenate all segments
    list_file = os.path.join(segments_dir, "concat.txt")
    with open(list_file, "w") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")

    print(f"\n  Merging {len(segments)} segments...")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c:v", "libx264", "-c:a", "aac",
        "-movflags", "+faststart",
        output_path
    ], capture_output=True)

    # Cleanup
    if not args.keep_segments:
        for seg in segments:
            os.remove(seg)
        for f in os.listdir(segments_dir):
            if f.startswith("silence_"):
                os.remove(os.path.join(segments_dir, f))
        if os.path.exists(list_file):
            os.remove(list_file)
        # Remove _segments dir if empty
        try:
            os.rmdir(segments_dir)
        except OSError:
            pass

    # Summary
    if os.path.exists(output_path):
        dur = get_audio_duration(output_path)
        mins, secs = divmod(int(dur), 60)
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n  Video saved: {output_path}")
        print(f"  Duration: {mins}m {secs}s | Size: {size_mb:.1f} MB")
    else:
        print("\n  Error: Final video was not created!")
        sys.exit(1)


async def generate_tts(narrations_path, output_dir, voice="zh-CN-YunxiNeural", rate="-5%"):
    """用 edge-tts 生成每页旁白音频。"""
    try:
        import edge_tts
    except ImportError:
        print("Error: edge-tts not installed. Run: pip3 install edge-tts")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with open(narrations_path) as f:
        data = json.load(f)

    slides = data.get("slides", [])
    manifest = {"slides": []}

    for item in slides:
        num = item["slide_number"]
        text = item["narration"]
        out_path = os.path.join(output_dir, f"slide_{num:03d}.mp3")

        if os.path.exists(out_path):
            print(f"  [{num}/{len(slides)}] [skip] Already exists")
        else:
            print(f"  [{num}/{len(slides)}] Generating TTS...")
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            await communicate.save(out_path)

        duration = get_audio_duration(out_path)
        manifest["slides"].append({
            "slide_number": num,
            "duration": duration
        })

    # Write manifest
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n  TTS done. {len(slides)} audio files generated.")
    print(f"  Manifest saved: {manifest_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="课程视频构建工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # video subcommand
    video_parser = subparsers.add_parser("video", help="合成视频")
    video_parser.add_argument("--screenshots", required=True, help="截图目录")
    video_parser.add_argument("--audio", required=True, help="音频目录")
    video_parser.add_argument("--output", default="./course-video.mp4", help="输出视频路径")
    video_parser.add_argument("--width", type=int, default=1280, help="视频宽度")
    video_parser.add_argument("--height", type=int, default=720, help="视频高度")
    video_parser.add_argument("--gap", type=float, default=0.5, help="幻灯片间隔秒数")
    video_parser.add_argument("--keep-segments", action="store_true", help="保留中间片段")

    # tts subcommand
    tts_parser = subparsers.add_parser("tts", help="生成 TTS 音频")
    tts_parser.add_argument("--narrations", required=True, help="narrations.json 路径")
    tts_parser.add_argument("--outdir", default="./audio", help="音频输出目录")
    tts_parser.add_argument("--voice", default="zh-CN-YunxiNeural", help="TTS 声音")
    tts_parser.add_argument("--rate", default="-5%", help="语速调整 (如 +10%%, -5%%)")

    # all subcommand
    all_parser = subparsers.add_parser("all", help="TTS + 合成视频")
    all_parser.add_argument("--narrations", required=True, help="narrations.json 路径")
    all_parser.add_argument("--screenshots", required=True, help="截图目录")
    all_parser.add_argument("--audio", default="./audio", help="音频目录")
    all_parser.add_argument("--output", default="./course-video.mp4", help="输出视频路径")
    all_parser.add_argument("--width", type=int, default=1280)
    all_parser.add_argument("--height", type=int, default=720)
    all_parser.add_argument("--gap", type=float, default=0.5)
    all_parser.add_argument("--voice", default="zh-CN-YunxiNeural")
    all_parser.add_argument("--rate", default="-5%")
    all_parser.add_argument("--keep-segments", action="store_true")

    args = parser.parse_args()

    if args.command == "video":
        build_video(args)
    elif args.command == "tts":
        asyncio.run(generate_tts(args.narrations, args.outdir, args.voice, args.rate))
    elif args.command == "all":
        asyncio.run(generate_tts(args.narrations, args.audio, args.voice, args.rate))
        build_video(args)
    else:
        parser.print_help()
