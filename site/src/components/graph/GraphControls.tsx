"use client";

import { useCallback } from "react";
import { ArrowCounterClockwise, CornersOut, DownloadSimple } from "@phosphor-icons/react";

interface Props {
  onReset?: () => void;
  onFullscreen?: () => void;
  onExport?: () => void;
}

export default function GraphControls({ onReset, onFullscreen, onExport }: Props) {
  const handleFullscreen = useCallback(() => {
    if (typeof document === "undefined") return;
    const el = document.documentElement;
    if (!document.fullscreenElement) {
      el.requestFullscreen?.().catch(() => {});
    } else {
      document.exitFullscreen?.().catch(() => {});
    }
    onFullscreen?.();
  }, [onFullscreen]);

  const handleExport = useCallback(() => {
    if (typeof document === "undefined") return;
    const canvas = document.querySelector("canvas") as HTMLCanvasElement | null;
    if (!canvas) return;
    const url = canvas.toDataURL("image/png");
    const a = document.createElement("a");
    a.href = url;
    a.download = `ideal-lab-graph-${new Date().toISOString().slice(0, 10)}.png`;
    a.click();
    onExport?.();
  }, [onExport]);

  return (
    <div
      className="absolute bottom-3 right-3 flex items-center gap-1 rounded-md border px-1.5 py-1"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
        zIndex: "var(--bp-z-graph-controls)" as unknown as number,
      }}
    >
      <button
        onClick={onReset}
        aria-label="Reset graph layout"
        className="w-7 h-7 flex items-center justify-center rounded transition-colors hover:bg-[var(--bp-surface-2)]"
        style={{ color: "var(--bp-text-1)" }}
        title="Reset layout"
      >
        <ArrowCounterClockwise size={14} weight="regular" />
      </button>
      <button
        onClick={handleFullscreen}
        aria-label="Toggle fullscreen"
        className="w-7 h-7 flex items-center justify-center rounded transition-colors hover:bg-[var(--bp-surface-2)]"
        style={{ color: "var(--bp-text-1)" }}
        title="Fullscreen"
      >
        <CornersOut size={14} weight="regular" />
      </button>
      <button
        onClick={handleExport}
        aria-label="Export as PNG"
        className="w-7 h-7 flex items-center justify-center rounded transition-colors hover:bg-[var(--bp-surface-2)]"
        style={{ color: "var(--bp-text-1)" }}
        title="Export PNG"
      >
        <DownloadSimple size={14} weight="regular" />
      </button>
    </div>
  );
}
