"use client";

import { getEdgeCountsByRelation } from "@/lib/graph";
import type { Relation } from "@/lib/types";

const RELATION_META: Record<Relation, { label: string; color: string; dash?: number[] }> = {
  enhancement: { label: "enhancement", color: "#a3a3a3" },
  prerequisite: { label: "prerequisite", color: "#7b5cea" },
  embeds: { label: "embeds", color: "#0ea5a0", dash: [3, 3] },
  produces_for: { label: "produces_for", color: "#d98b0a" },
  alternative: { label: "alternative", color: "#9b6cea", dash: [1, 3] },
};

export default function GraphLegend() {
  const counts = getEdgeCountsByRelation();
  return (
    <div
      className="rounded-md border px-3 py-2 text-[11px] inline-flex items-center gap-4"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
        color: "var(--bp-text-1)",
      }}
      role="note"
      aria-label="Edge relation legend"
    >
      <span className="font-semibold" style={{ color: "var(--bp-text-0)" }}>
        Edge
      </span>
      {(Object.keys(RELATION_META) as Relation[]).map((r) => {
        const m = RELATION_META[r];
        return (
          <div key={r} className="flex items-center gap-1.5">
            <svg width="18" height="6">
              <line
                x1="0"
                y1="3"
                x2="18"
                y2="3"
                stroke={m.color}
                strokeWidth="1.5"
                strokeDasharray={m.dash?.join(" ")}
              />
            </svg>
            <span>
              {m.label} <span style={{ color: "var(--bp-text-3)" }}>({counts[r]})</span>
            </span>
          </div>
        );
      })}
    </div>
  );
}
