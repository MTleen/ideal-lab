"use client";

import { getEdgeCountsByRelation } from "@/lib/graph";

/* Categories that actually occur in the data (content / development / knowledge /
 * research). tooling / other exist in the palette as fallbacks but have no nodes. */
const CATEGORIES = [
  { key: "development", label: "开发" },
  { key: "content", label: "内容" },
  { key: "knowledge", label: "知识" },
  { key: "research", label: "研究" },
];

/* Mini SVG swatches mirror the canvas stroke styles in GraphCanvas:
 *   prerequisite  solid line + arrowhead
 *   calls         thin solid line, no head
 *   produces_for  dashed line + arrowhead
 */
function EdgeSwatch({
  color,
  dashed = false,
  arrow = false,
  width = 22,
}: {
  color: string;
  dashed?: boolean;
  arrow?: boolean;
  width?: number;
}) {
  return (
    <svg width={width} height={8} aria-hidden="true" style={{ flexShrink: 0 }}>
      <line
        x1={1}
        y1={4}
        x2={arrow ? 15 : width - 1}
        y2={4}
        stroke={color}
        strokeWidth={dashed ? 1.4 : 1.2}
        strokeDasharray={dashed ? "3 2" : undefined}
      />
      {arrow && <polygon points="15,1 20,4 15,7" fill={color} />}
    </svg>
  );
}

export default function GraphLegend() {
  const counts = getEdgeCountsByRelation();
  return (
    <div
      className="flex flex-wrap items-center gap-x-5 gap-y-2 text-[11px]"
      style={{ color: "var(--bp-text-2)" }}
      role="note"
      aria-label="图谱图例：节点类别与关系类型"
    >
      {/* 节点类别 */}
      <span className="font-semibold uppercase tracking-wider" style={{ color: "var(--bp-text-1)" }}>
        节点
      </span>
      {CATEGORIES.map((c) => (
        <span key={c.key} className="inline-flex items-center gap-1.5">
          <span
            className="w-2.5 h-2.5 rounded-full"
            style={{ background: `var(--bp-graph-cat-${c.key})` }}
          />
          <span style={{ color: "var(--bp-text-1)" }}>{c.label}</span>
        </span>
      ))}

      <span className="mx-1" style={{ color: "var(--bp-border-1)" }}>
        │
      </span>

      {/* 关系类型（仅画出的三种） */}
      <span className="font-semibold uppercase tracking-wider" style={{ color: "var(--bp-text-1)" }}>
        关系
      </span>
      <span className="inline-flex items-center gap-1.5">
        <EdgeSwatch color="var(--bp-graph-edge-prerequisite)" arrow />
        <span>
          前置 <span style={{ color: "var(--bp-text-3)" }}>· {counts.prerequisite}</span>
        </span>
      </span>
      <span className="inline-flex items-center gap-1.5">
        <EdgeSwatch color="var(--bp-graph-edge-calls)" />
        <span>
          调用 <span style={{ color: "var(--bp-text-3)" }}>· {counts.calls}</span>
        </span>
      </span>
      <span className="inline-flex items-center gap-1.5">
        <EdgeSwatch color="var(--bp-graph-edge-produces-for)" dashed arrow />
        <span>
          产出 <span style={{ color: "var(--bp-text-3)" }}>· {counts.produces_for}</span>
        </span>
      </span>
    </div>
  );
}
