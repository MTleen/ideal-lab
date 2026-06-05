"use client";

import { useCallback } from "react";

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
      className="absolute bottom-3 right-3 z-10 flex items-center gap-1 rounded-md border px-1.5 py-1"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
      }}
    >
      <button
        onClick={onReset}
        aria-label="Reset graph layout"
        className="w-7 h-7 flex items-center justify-center rounded transition-colors hover:bg-[var(--bp-surface-2)]"
        style={{ color: "var(--bp-text-1)" }}
        title="Reset layout"
      >
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M14 8a6 6 0 11-1.76-4.24M14 3v3h-3" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      <button
        onClick={handleFullscreen}
        aria-label="Toggle fullscreen"
        className="w-7 h-7 flex items-center justify-center rounded transition-colors hover:bg-[var(--bp-surface-2)]"
        style={{ color: "var(--bp-text-1)" }}
        title="Fullscreen"
      >
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M2 6V2h4M14 6V2h-4M2 10v4h4M14 10v4h-4" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      <button
        onClick={handleExport}
        aria-label="Export as PNG"
        className="w-7 h-7 flex items-center justify-center rounded transition-colors hover:bg-[var(--bp-surface-2)]"
        style={{ color: "var(--bp-text-1)" }}
        title="Export PNG (P2)"
      >
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M8 2v8M5 7l3 3 3-3M2 13h12" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
    </div>
  );
}
