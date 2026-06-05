---
name: course-to-video
description: >
  Create course content from reference materials AND transform it into narrated
  teaching videos. Full pipeline: reference materials → course markdown → parse
  → HTML slides → narration scripts → TTS audio (edge-tts) → screenshots
  (Playwright) → compose video (ffmpeg). Use when the user asks to make a
  teaching video, course video, narrated slideshow, instructional video, course
  recording, 课件视频, 课程视频, 教学视频, 配音课件, 录课, 自动录课,
  TTS 视频, 文字转视频, markdown 转 视频, 课件录制, 幻灯片视频, slide to
  video, markdown to video, create course from materials, generate course
  content, 写课件, 生成课件, 课程制作, or wants to convert course
  content/slides/HTML into a video with voiceover. Also triggers on: "make a
  video from my course", "add narration to slides", "generate audio for course",
  "batch TTS", "edge-tts video", "course pipeline", "课程转视频",
  "生成教学视频". Even if the user only asks for partial work (just slides, just
  audio, just screenshots, just course content), use this skill — it handles
  individual stages as well as the full pipeline. IMPORTANT: content generation
  requires reference materials as anchor — never fabricate factual content.
---

# Course-to-Video：课程转视频

将 Markdown 课程文件一键转化为带旁白的教学视频。

## 输出物

- `slides.html` — 自包含 HTML 幻灯片（浏览器可预览，支持键盘翻页）
- `audio/` — 每页旁白的 MP3 音频文件
- `screenshots/` — 每页幻灯片的 PNG 截图
- `course-video.mp4` — 最终合成视频（画面 + 旁白）

## 前置检查

开始前，确认以下工具已安装。缺少任何一个就提示用户安装：

```bash
# 检查命令
ffmpeg -version          # 需要 ffmpeg
python3 -c "import edge_tts"   # 需要 edge-tts
python3 -c "from playwright.sync_api import sync_playwright"  # 需要 playwright

# 安装命令（macOS）
brew install ffmpeg
pip3 install edge-tts
pip3 install playwright && playwright install chromium

# 安装命令（Linux）
sudo apt install ffmpeg
pip3 install edge-tts
pip3 install playwright && playwright install chromium

# 安装命令（Windows）
winget install ffmpeg
pip3 install edge-tts
pip3 install playwright && playwright install chromium
```

## 流水线总览

```
Stage 0: CONTENT    参考资料 → 课程 Markdown       ← Claude 驱动 + 用户审核
Stage 1: PARSE      markdown → slides.json         ← Claude 驱动
Stage 2: SLIDES     slides.json → slides.html       ← Claude 驱动
Stage 3: NARRATE    slides.json → narrations.json   ← Claude 驱动
Stage 4: AUDIO      narrations.json → audio/*.mp3   ← 脚本驱动
Stage 5: CAPTURE    slides.html → screenshots/*.png ← 脚本驱动
Stage 6: COMPOSE    PNG + MP3 → final.mp4           ← 脚本驱动
```

### 阶段选择逻辑

- 用户已有课程 Markdown → 跳过 Stage 0，从 Stage 1 开始
- 用户有参考资料需要生成课程 → 从 Stage 0 开始
- 用户说"全部"或"生成视频"→ 根据是否有 Markdown 决定起点，运行 Stage 0/1 ~ 6
- 用户说"只要幻灯片" → 仅 Stage 1-2
- 用户说"只要音频"或"生成旁白" → 仅 Stage 3-4
- 用户说"截图"或"截取幻灯片" → 仅 Stage 5
- 用户说"合成视频"或"build video" → 仅 Stage 6
- 如果中间产物已存在，跳过对应阶段（除非用户说"重新来"或"from scratch"）

---

## Stage 0：课程内容创作

**Claude 驱动 + 用户审核。** 从参考资料中提取知识点，生成课程 Markdown 文件。

### 核心原则：必须有锚点

**禁止凭空创作事实性内容。** 课程内容必须基于以下至少一种"锚点"：

| 锚点类型 | 示例 | 准确性保障 |
|----------|------|------------|
| 用户提供的参考资料 | PDF、文档、网页链接、书籍章节 | 从资料中提取和重组，不编造 |
| 用户提供的课程大纲 + 知识点 | 用户写好的教学大纲 | 按大纲扩写，不自行发挥 |
| 用户提供的原始课件 | 已有课件要求改写/二改 | 基于原内容改写结构和风格 |

**如果用户只给了一个主题（如"Python 入门"），拒绝直接生成内容。** 告诉用户：

> "为了确保课件内容准确，我需要参考资料作为锚点。请提供以下任一：
> 1. 相关文档或教程链接
> 2. 你自己写的课程大纲和要点
> 3. 需要改写的原始课件
> 我会基于这些资料来生成课程内容。"

### 操作步骤

1. **获取锚点**：请用户提供参考资料（文件路径、URL、或直接粘贴内容）
2. **读取和消化**：读取所有参考资料，提取核心知识点
3. **生成大纲**：输出课程大纲（章节标题 + 每章要点），**提交用户审核**
4. **用户确认大纲后**：按大纲逐章生成 Markdown 课程文件
5. **每章生成后**：提示用户可审阅修改，确认无误后再继续
6. **全部章节完成后**：课程 Markdown 文件就绪，进入 Stage 1

### 课程 Markdown 文件规范

每个章节一个 `.md` 文件，文件名格式：`{序号}-{主题}.md`

```markdown
---
title: "章节标题"
description: "章节简述"
order: 1
---

# 章节标题

## 第一个小节

要点内容...

- 要点 1
- 要点 2

## 第二个小节

更多内容...

> 重点引用
```

课程首页 `index.md`：

```markdown
---
title: "课程标题"
description: "课程副标题"
---

# 课程标题

课程简介段落。

## 适合人群

- 目标学员 1
- 目标学员 2
```

### 输出确认

Stage 0 完成后，向用户确认：

> "课程内容已生成到 `{目录}`，共 {N} 个章节文件。请审阅内容是否准确。确认无误后我将开始生成幻灯片和视频。"

**用户确认后，进入 Stage 1。**

---

## Stage 1：解析 Markdown

**Claude 驱动。** 读取课程 Markdown 文件，输出 `slides.json`。

### 操作步骤

1. 询问用户课程 Markdown 文件所在目录
2. 读取 `index.md`（如有）获取课程标题、副标题
3. 按文件名前缀排序，依次读取所有 `.md` 文件
4. 按 `references/markdown-parsing.md` 中的规则将内容切分为幻灯片
5. 输出 `slides.json` 到指定目录
6. **暂停，展示幻灯片概览**（总页数、各页类型和标题），请用户确认内容完整性。用户说"继续"或"没问题"后进入 Stage 2

### JSON 格式

```json
{
  "course_title": "课程标题",
  "course_subtitle": "副标题",
  "course_tags": "标签行",
  "source_files": ["index.md", "01-intro.md"],
  "config": {
    "resolution": [1280, 720],
    "voice": "zh-CN-YunxiNeural",
    "theme": "dark"
  },
  "slides": [
    {
      "slide_number": 1,
      "type": "cover|section|content|code|summary",
      "title": "页面标题",
      "body": "正文 HTML",
      "bullet_points": ["要点1", "要点2"],
      "code_block": null,
      "notes": "原始 markdown 上下文（供旁白创作参考）"
    }
  ]
}
```

### 幻灯片类型

| type | 说明 | 渲染样式 |
|------|------|----------|
| `cover` | 课程封面 | 居中大标题 + 副标题 |
| `section` | 章节分页 | 居中标题 |
| `content` | 正文内容 | 标题 + 正文/卡片/列表 |
| `code` | 代码展示 | 标题 + 代码块 |
| `summary` | 总结 | 居中或网格布局 |

---

## Stage 2：生成 HTML 幻灯片

**Claude 驱动。** 读取 `slides.json` 和模板，输出 `slides.html`。

### 操作步骤

1. 读取本 skill 的 `references/slides-template.html` 获取模板结构
2. 根据 `config.theme` 选择主题（读取 `assets/slide-themes/dark.css` 或 `light.css`）
3. 为 `slides.json` 中的每一页生成对应的 `<div class="slide slide-{type}">` HTML
4. 第一页加上 `active` class
5. 替换模板中的 `{{COURSE_TITLE}}` 等占位符
6. 输出完整的 `slides.html`

### 关键约束

- **自包含**：所有 CSS 和 JS 必须内联，**禁止任何外部依赖**（CDN 字体会导致 Playwright 截图超时）
- **固定视口**：body 设置 `width: 1280px; height: 720px`
- **showSlide(n)**：JavaScript 函数，接受 0-based 索引，切换 `.active` class
- **内容不溢出**：每页内容控制在视口范围内，使用 `overflow: hidden` 兜底

### 幻灯片 HTML 生成规则

**封面页（cover）：**
```html
<div class="slide slide-cover active" id="slide-1">
  <div class="center" style="width:100%">
    <h1>课程标题</h1>
    <p class="subtitle">副标题</p>
    <p class="muted" style="margin-top:40px">标签行</p>
  </div>
</div>
```

**内容页（content）：**
```html
<div class="slide slide-content" id="slide-2">
  <h2>页面标题</h2>
  <!-- 使用 .grid2 + .card 展示卡片内容 -->
  <!-- 使用 <ul><li> 展示要点 -->
  <!-- 使用 <blockquote> 展示重点引用 -->
  <!-- 使用 <pre><code> 展示代码片段 -->
</div>
```

**分节页（section）：**
```html
<div class="slide slide-section" id="slide-N">
  <h2>章节标题</h2>
</div>
```

---

## Stage 3：编写旁白脚本

**Claude 驱动。** 读取 `slides.json`，为每页写旁白文字。

### 操作步骤

1. 读取本 skill 的 `references/narration-guide.md` 获取旁白写作规则
2. 读取 `slides.json` 中每页的 `notes` 和 `body`
3. 为每页编写口语化的中文旁白（100-200 字/内容页，40-80 字/封面和分节页）
4. 输出 `narrations.json`
5. **暂停，展示旁白概览**（总字数、预估总时长、抽查 2-3 页旁白），请用户确认内容质量。用户说"继续"后进入 Stage 4

### JSON 格式

```json
{
  "slides": [
    {
      "slide_number": 1,
      "narration": "大家好，欢迎来到这门课程...",
      "estimated_duration_seconds": 12.5
    }
  ]
}
```

### 旁白写作要点

- **口语化**：用"所以"不用"因此"，用"这个"不用"该"
- **补充而非重复**：不逐字念幻灯片，补充画面上没有的上下文
- **自然过渡**：每页开头用过渡句（"接下来我们看看..."）
- **控制长度**：每页不超过 250 字
- **中文 TTS 语速**：约 4 字/秒

---

## Stage 4：生成 TTS 音频

**脚本驱动。** 运行 `scripts/build_video.py tts`。

定位脚本路径：先检查 `{skill_dir}/scripts/build_video.py`（plugin 安装模式），若不存在则尝试 `~/.claude/skills/course-to-video/scripts/build_video.py`（直接安装模式）。

```bash
python3 {skill_dir}/scripts/build_video.py tts \
  --narrations output/narrations.json \
  --outdir output/audio \
  --voice zh-CN-YunxiNeural \
  --rate "-5%"
```

### 可选声音

| 声音 | 特点 | 适用场景 |
|------|------|----------|
| `zh-CN-YunxiNeural` | 男声，温暖自然 | 技术课程（推荐） |
| `zh-CN-XiaoxiaoNeural` | 女声，清晰标准 | 通用教育 |
| `zh-CN-YunjianNeural` | 男声，沉稳权威 | 正式培训 |
| `zh-CN-XiaoyiNeural` | 女声，活泼 | 入门课程 |

输出：`audio/slide_001.mp3` ~ `slide_NNN.mp3` + `audio/manifest.json`

---

## Stage 5：截取幻灯片截图

**脚本驱动。** 运行 `scripts/capture_slides.py`。

```bash
python3 {skill_dir}/scripts/capture_slides.py \
  --html output/slides.html \
  --count 16 \
  --outdir output/screenshots \
  --width 1280 --height 720 \
  --delay 500
```

如果 Playwright 的 `file://` 协议加载异常，先启动本地 HTTP 服务：

```bash
cd output && python3 -m http.server 8888 &
# 然后改用 --html http://localhost:8888/slides.html
```

输出：`screenshots/slide_001.png` ~ `slide_NNN.png`

---

## Stage 6：合成最终视频

**脚本驱动。** 运行 `scripts/build_video.py video`。

```bash
python3 {skill_dir}/scripts/build_video.py video \
  --screenshots output/screenshots \
  --audio output/audio \
  --output output/course-video.mp4 \
  --width 1280 --height 720 \
  --gap 0.5
```

### 一键全部（Stage 4 + 6）

```bash
python3 {skill_dir}/scripts/build_video.py all \
  --narrations output/narrations.json \
  --screenshots output/screenshots \
  --audio output/audio \
  --output output/course-video.mp4
```

---

## 配置选项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 分辨率 | 1280×720 | 在 `slides.json` config 中设置 |
| TTS 声音 | zh-CN-YunxiNeural | 见 Stage 4 可选声音表 |
| 主题 | dark | dark / light，在 config 中设置 |
| 语速 | -5% | edge-tts `--rate` 参数，范围 -20% ~ +50% |
| 幻灯片间隔 | 0.5s | build_video.py `--gap` 参数 |
| 渲染延迟 | 500ms | capture_slides.py `--delay` 参数 |

---

## 输出目录结构

```
output/
├── 00-intro.md ... N.md     (Stage 0 — 课程 Markdown)
├── index.md                 (Stage 0 — 课程首页)
├── slides.json              (Stage 1)
├── narrations.json          (Stage 3)
├── slides.html              (Stage 2)
├── audio/
│   ├── manifest.json        (音频时长映射)
│   ├── slide_001.mp3
│   └── ...
├── screenshots/
│   ├── slide_001.png
│   └── ...
└── course-video.mp4         (Stage 6 — 最终输出)
```

---

## Troubleshooting

| 问题 | 解决方案 |
|------|----------|
| 截图白屏 | 确保 slides.html 无外部依赖（CDN 字体等） |
| ffmpeg 报错 "height not divisible by 2" | 分辨率必须为偶数，脚本已强制 |
| edge-tts 429 限流 | 在脚本中增加请求间隔 |
| 中文 TTS 乱码 | 使用 `python3 -X utf8` 运行 |
| Playwright 浏览器未找到 | 运行 `playwright install chromium` |
| 截图字体缺失 | 确认系统已安装中文字体（`fc-list :lang=zh`） |
| 内容溢出视口 | 减少每页要点数量，或缩短文本 |
| 脚本路径找不到 | 检查 plugin 安装路径或手动指定脚本的绝对路径 |

---

## Reference Files

- **[references/slides-template.html](references/slides-template.html)** — HTML 幻灯片模板（Stage 2 时读取）
- **[references/narration-guide.md](references/narration-guide.md)** — 旁白写作详细指南（Stage 3 时读取）
- **[references/markdown-parsing.md](references/markdown-parsing.md)** — Markdown 解析详细规则（Stage 1 时读取）
- **[assets/slide-themes/dark.css](assets/slide-themes/dark.css)** — 深色主题
- **[assets/slide-themes/light.css](assets/slide-themes/light.css)** — 浅色主题
