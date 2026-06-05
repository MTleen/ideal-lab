"use client";

import { getEdgeCountsByRelation } from "@/lib/graph";

export default function GraphLegend() {
  const counts = getEdgeCountsByRelation();
  const shown: { label: string; n: number }[] = [
    { label: "prerequisite", n: counts.prerequisite },
    { label: "produces_for", n: counts.produces_for },
    { label: "alternative", n: counts.alternative },
  ];
  return (
    <div
      className="rounded-md border px-3 py-2 text-[11px] inline-flex items-center gap-3"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
        color: "var(--bp-text-1)",
      }}
      role="note"
      aria-label="Edge legend"
    >
      <span className="font-semibold" style={{ color: "var(--bp-text-0)" }}>
        Edges shown (call relations)
      </span>
      {shown.map((s) => (
        <span key={s.label} className="inline-flex items-center gap-1">
          <span style={{ color: "var(--bp-brand-500)" }}>→</span>
          <span>{s.label}</span>
          <span style={{ color: "var(--bp-text-3)" }}>({s.n})</span>
        </span>
      ))}
    </div>
  );
}
