"use client";

import { useEffect, useRef, useState } from "react";
import * as d3 from "d3-force";
import type { GraphNode, GraphEdge } from "@/lib/types";

interface Props {
  centerId: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  width?: number;
  height?: number;
}

const CATEGORY_COLORS: Record<string, string> = {
  development: "#7b5cea",
  content: "#0ea5a0",
  research: "#d98b0a",
  knowledge: "#8ba60a",
  tooling: "#9b6cea",
  other: "#6e6e82",
};

interface Positioned {
  id: string;
  name: string;
  category: string;
  x: number;
  y: number;
}

export default function MiniGraph({
  centerId,
  nodes,
  edges,
  width = 360,
  height = 240,
}: Props) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [positions, setPositions] = useState<Positioned[]>([]);

  useEffect(() => {
    /* Build d3-force nodes */
    const simNodes = nodes.map((n) => ({ id: n.id, name: n.name, category: n.category }));
    const simEdges = edges
      .filter(
        (e) =>
          simNodes.find((n) => n.id === e.source) &&
          simNodes.find((n) => n.id === e.target),
      )
      .map((e) => ({ source: e.source, target: e.target }));

    if (simNodes.length === 0) return;

    /* Pre-position center at middle */
    const center = simNodes.find((n) => n.id === centerId);
    if (center) {
      (center as any).fx = width / 2;
      (center as any).fy = height / 2;
    }

    const sim = d3
      .forceSimulation(simNodes as any)
      .force(
        "link",
        d3
          .forceLink(simEdges)
          .id((d: any) => d.id)
          .distance(60)
          .strength(0.5),
      )
      .force("charge", d3.forceManyBody().strength(-150))
      .force("center", d3.forceCenter(width / 2, height / 2).strength(0.1))
      .force("collide", d3.forceCollide(20))
      .stop();

    /* Run 80 ticks synchronously (synchronous for predictable layout) */
    for (let i = 0; i < 80; i++) sim.tick();

    setPositions(
      simNodes.map((n: any) => ({
        id: n.id,
        name: n.name,
        category: n.category,
        x: n.x,
        y: n.y,
      })),
    );
  }, [centerId, nodes, edges, width, height]);

  const center = positions.find((p) => p.id === centerId);
  const neighbors = positions.filter((p) => p.id !== centerId);

  return (
    <div
      className="rounded-lg border p-3 my-3"
      style={{
        background: "var(--bp-mini-bg)",
        borderColor: "var(--bp-mini-border)",
      }}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="text-[11px] font-semibold" style={{ color: "var(--bp-text-1)" }}>
          Local context (1-hop)
        </div>
        <a
          href={`/?task=&focus=${encodeURIComponent(centerId)}`}
          className="text-[11px] underline-offset-2 hover:underline"
          style={{ color: "var(--bp-brand-500)" }}
        >
          Open in full graph →
        </a>
      </div>
      <svg
        ref={svgRef}
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={`Mini graph centered on ${centerId}`}
        style={{ display: "block", maxWidth: "100%" }}
      >
        {/* Edges */}
        {edges
          .filter(
            (e) =>
              positions.find((p) => p.id === e.source) &&
              positions.find((p) => p.id === e.target),
          )
          .map((e, i) => {
            const s = positions.find((p) => p.id === e.source);
            const t = positions.find((p) => p.id === e.target);
            if (!s || !t) return null;
            return (
              <line
                key={i}
                x1={s.x}
                y1={s.y}
                x2={t.x}
                y2={t.y}
                stroke="var(--bp-mini-edge, #a3a3a3)"
                strokeWidth={1}
              />
            );
          })}

        {/* Neighbors */}
        {neighbors.map((n) => (
          <g key={n.id} transform={`translate(${n.x}, ${n.y})`}>
            <circle
              r={8}
              fill={CATEGORY_COLORS[n.category] ?? CATEGORY_COLORS.other}
              stroke="var(--bp-mini-neighbor-stroke, #888)"
              strokeWidth={1}
            />
            <text
              x={11}
              y={3}
              fontSize={9}
              fill="var(--bp-text-1, #555)"
              style={{ pointerEvents: "none" }}
            >
              {n.name.length > 16 ? n.name.slice(0, 15) + "…" : n.name}
            </text>
          </g>
        ))}

        {/* Center */}
        {center && (
          <g transform={`translate(${center.x}, ${center.y})`}>
            <circle
              r={10}
              fill="var(--bp-mini-center-fill, #7b5cea)"
              stroke="#fff"
              strokeWidth={2}
            />
            <text
              x={13}
              y={3}
              fontSize={10}
              fontWeight={600}
              fill="var(--bp-text-0, #1a1a2e)"
              style={{ pointerEvents: "none" }}
            >
              {center.name.length > 16 ? center.name.slice(0, 15) + "…" : center.name}
            </text>
          </g>
        )}
      </svg>
    </div>
  );
}
