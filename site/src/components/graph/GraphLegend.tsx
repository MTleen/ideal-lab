"use client";

export default function GraphLegend() {
  return (
    <div
      className="rounded-md border px-3 py-2 text-[11px] inline-flex items-center gap-2"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
        color: "var(--bp-text-1)",
      }}
      role="note"
      aria-label="Edge legend"
    >
      <span className="font-semibold" style={{ color: "var(--bp-text-0)" }}>
        Edge
      </span>
      <div className="flex items-center gap-1.5">
        <svg width="18" height="6">
          <line
            x1="0"
            y1="3"
            x2="18"
            y2="3"
            stroke="var(--bp-brand-500)"
            strokeWidth="1.5"
          />
        </svg>
        <span>A 调用 / 喂给 B（prerequisite / produces_for / embeds / enhancement / alternative）</span>
      </div>
    </div>
  );
}
