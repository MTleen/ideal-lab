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

const CATEGORY_META: Record<string, { label: string; color: string }> = {
  development: { label: "development", color: "#7b5cea" },
  content: { label: "content", color: "#0ea5a0" },
  research: { label: "research", color: "#d98b0a" },
  knowledge: { label: "knowledge", color: "#8ba60a" },
  tooling: { label: "tooling", color: "#9b6cea" },
  other: { label: "other", color: "#6e6e82" },
};

export default function GraphLegend() {
  const counts = getEdgeCountsByRelation();
  return (
    <div
      className="absolute bottom-3 left-3 z-10 rounded-md border px-3 py-2 text-[11px]"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
        color: "var(--bp-text-1)",
      }}
    >
      <div className="font-semibold mb-1.5" style={{ color: "var(--bp-text-0)" }}>
        Skill category
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1 mb-2">
        {Object.entries(CATEGORY_META).map(([k, m]) => (
          <div key={k} className="flex items-center gap-1.5">
            <span
              className="inline-block w-2.5 h-2.5 rounded-full"
              style={{ background: m.color }}
            />
            <span>{m.label}</span>
          </div>
        ))}
      </div>
      <div className="font-semibold mb-1.5" style={{ color: "var(--bp-text-0)" }}>
        Relation
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {(Object.keys(RELATION_META) as Relation[]).map((r) => {
          const m = RELATION_META[r];
          return (
            <div key={r} className="flex items-center gap-1.5">
              <svg width="20" height="6">
                <line
                  x1="0"
                  y1="3"
                  x2="20"
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
    </div>
  );
}
