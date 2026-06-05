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
        Edges
      </span>
      <span className="inline-flex items-center gap-1">
        <span style={{ color: "var(--bp-brand-500)" }}>→</span>
        <span>calls (orchestrator → phase skills)</span>
      </span>
    </div>
  );
}
