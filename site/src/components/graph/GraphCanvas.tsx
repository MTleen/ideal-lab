"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import ForceGraph2D, { ForceGraphMethods } from "react-force-graph-2d";
import type { GraphNode, GraphEdge, Relation } from "@/lib/types";

interface Props {
  nodes: GraphNode[];
  edges: GraphEdge[];
  /** Skill ids to highlight (rest are dimmed). */
  highlightedSkillIds?: string[];
  /** Currently focused skill id (extra glow). */
  focusedSkillId?: string | null;
  onNodeClick?: (node: GraphNode) => void;
  onNodeHover?: (node: GraphNode | null) => void;
}

const CATEGORY_COLORS: Record<string, string> = {
  development: "#7b5cea",
  content: "#0ea5a0",
  research: "#d98b0a",
  knowledge: "#8ba60a",
  tooling: "#9b6cea",
  other: "#6e6e82",
};

const EDGE_COLOR = "var(--bp-brand-500)";

interface GraphDatum {
  id: string;
  name: string;
  plugin: string;
  category: string;
  inDegree: number;
  // d3-force injects:
  x?: number;
  y?: number;
}

interface LinkDatum {
  source: string | GraphDatum;
  target: string | GraphDatum;
  relation: Relation;
}

export default function GraphCanvas({
  nodes,
  edges,
  highlightedSkillIds = [],
  focusedSkillId = null,
  onNodeClick,
  onNodeHover,
}: Props) {
  const fgRef = useRef<ForceGraphMethods<GraphDatum, LinkDatum> | undefined>(undefined);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [size, setSize] = useState({ w: 0, h: 0 });
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; node: GraphDatum } | null>(null);

  const highlightSet = useMemo(() => new Set(highlightedSkillIds), [highlightedSkillIds]);

  /* Build graph data: include hidden intra-plugin edges to enforce clustering */
  const data = useMemo(() => {
    const inDeg = new Map<string, number>();
    for (const e of edges) inDeg.set(e.target, (inDeg.get(e.target) ?? 0) + 1);

    const gNodes: GraphDatum[] = nodes.map((n) => ({
      id: n.id,
      name: n.name,
      plugin: n.plugin,
      category: n.category,
      inDegree: inDeg.get(n.id) ?? 0,
    }));

    const gEdges: LinkDatum[] = edges.map((e) => ({
      source: e.source,
      target: e.target,
      relation: e.relation,
    }));

    /* Hidden intra-plugin clustering edges */
    const byPlugin = new Map<string, GraphDatum[]>();
    for (const n of gNodes) {
      const arr = byPlugin.get(n.plugin) ?? [];
      arr.push(n);
      byPlugin.set(n.plugin, arr);
    }
    for (const cluster of byPlugin.values()) {
      if (cluster.length < 2) continue;
      const a = cluster[0];
      for (let i = 1; i < cluster.length; i++) {
        gEdges.push({ source: a.id, target: cluster[i].id, relation: "enhancement" });
      }
    }

    return { nodes: gNodes, links: gEdges };
  }, [nodes, edges]);

  /* Resize observer */
  useEffect(() => {
    if (!containerRef.current) return;
    const el = containerRef.current;
    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const r = entry.contentRect;
        setSize({ w: Math.floor(r.width), h: Math.floor(r.height) });
      }
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /* Apply d3-force config + pre-warm simulation */
  useEffect(() => {
    const fg = fgRef.current;
    if (!fg) return;
    // Pre-position nodes: spread across the canvas using golden angle
    const w = size.w || 800;
    const h = size.h || 600;
    data.nodes.forEach((n: any, i: number) => {
      const angle = i * 2.39996; // golden angle
      const radius = Math.min(w, h) * 0.35 * Math.sqrt((i + 1) / data.nodes.length);
      n.x = w / 2 + radius * Math.cos(angle);
      n.y = h / 2 + radius * Math.sin(angle);
    });
    fg.d3ReheatSimulation();

    fg.d3Force("charge")?.strength(-380);
    fg.d3Force("link")?.distance((l: any) => (l.relation === "enhancement" ? 40 : 80));
    fg.d3Force("center")?.strength(0.05);
    fg.d3Force("collide", (window as any).d3?.forceCollide?.(28));
  }, [data, size.w, size.h]);

  /* Node radius from in-degree. Large enough to hold a short label inside. */
  const radiusOf = (n: GraphDatum) =>
    Math.max(18, Math.min(36, Math.sqrt(n.inDegree + 1) * 9));

  const isDim = (n: GraphDatum) =>
    highlightSet.size > 0 && !highlightSet.has(n.id) && n.id !== focusedSkillId;

  const isFocused = (n: GraphDatum) => n.id === focusedSkillId;

  /* Custom node paint — circle big enough to contain a short label, with the
   * skill name always visible. Plugin cluster label drawn outside the node. */
  const paintNode = (node: GraphDatum, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const r = radiusOf(node);
    const x = node.x ?? 0;
    const y = node.y ?? 0;
    const color = CATEGORY_COLORS[node.category] ?? CATEGORY_COLORS.other;
    const dimmed = isDim(node);

    /* Focus glow */
    if (isFocused(node)) {
      ctx.beginPath();
      ctx.arc(x, y, r + 6, 0, 2 * Math.PI);
      ctx.fillStyle = "rgba(123, 92, 234, 0.35)";
      ctx.fill();
    }

    ctx.globalAlpha = dimmed ? 0.25 : (highlightSet.has(node.id) || isFocused(node) ? 1 : 0.95);

    /* Node body */
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.lineWidth = isFocused(node) ? 2.5 : 1;
    ctx.strokeStyle = isFocused(node) ? "#fff" : "rgba(0,0,0,0.25)";
    ctx.stroke();

    /* Always-visible label inside the node */
    const fontSize = Math.max(8, Math.min(11, r / 3.5));
    ctx.font = `600 ${fontSize}px Satoshi, system-ui, -apple-system, sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = dimmed ? "rgba(255, 255, 255, 0.7)" : "#fff";
    const label = node.name;
    const maxChars = Math.max(5, Math.floor(r * 1.6 / fontSize));
    const displayLabel = label.length > maxChars ? label.slice(0, maxChars - 1) + "…" : label;
    ctx.fillText(displayLabel, x, y);

    /* Bigger tooltip-style label on hover */
    if (isFocused(node) && globalScale > 0.2) {
      const tipFont = Math.max(10, 12 / globalScale);
      ctx.font = `600 ${tipFont}px Satoshi, system-ui, -apple-system, sans-serif`;
      const maxTipChars = Math.max(12, Math.floor(120 / tipFont));
      const tipLabel = label.length > maxTipChars ? label.slice(0, maxTipChars - 1) + "…" : label;
      const tipTextW = ctx.measureText(tipLabel).width;
      const padding = 6;
      const boxX = x - tipTextW / 2 - padding;
      const boxY = y + r + 6;
      const boxH = tipFont + padding;
      ctx.fillStyle = "rgba(26, 26, 46, 0.95)";
      ctx.beginPath();
      ctx.roundRect(boxX, boxY, tipTextW + padding * 2, boxH, 4);
      ctx.fill();
      ctx.fillStyle = "#fff";
      ctx.textBaseline = "middle";
      ctx.fillText(tipLabel, x, boxY + boxH / 2);
    }

    ctx.globalAlpha = 1;
  };

  /* Custom link paint — only render "real" call relations (prerequisite,
   * produces_for, alternative). Enhancement/embeds edges are hidden because
   * they don't reflect an actual call between plugins. 146 of 183 edges are
   * enhancement, hiding them leaves the ~19 meaningful call edges. */
  const HARD_RELATIONS = new Set<Relation>(["prerequisite", "produces_for", "alternative"]);
  const EDGE_COLOR = "var(--bp-brand-500)";

  const paintLink = (link: LinkDatum, ctx: CanvasRenderingContext2D) => {
    const src = link.source as GraphDatum;
    const tgt = link.target as GraphDatum;
    if (typeof src.x !== "number" || typeof tgt.x !== "number") return;
    if (!HARD_RELATIONS.has(link.relation)) return;
    const dim = isDim(src) || isDim(tgt);
    ctx.strokeStyle = EDGE_COLOR;
    ctx.globalAlpha = dim ? 0.15 : 0.6;
    ctx.lineWidth = 1;
    ctx.setLineDash([]);

    ctx.beginPath();
    ctx.moveTo(src.x!, src.y!);
    ctx.lineTo(tgt.x!, tgt.y!);
    ctx.stroke();
    ctx.globalAlpha = 1;
  };

  /* Pointer area (invisible) for hover/click */
  const paintPointerArea = (node: GraphDatum, color: string, ctx: CanvasRenderingContext2D) => {
    const r = radiusOf(node) + 2;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(node.x!, node.y!, r, 0, 2 * Math.PI);
    ctx.fill();
  };

  return (
    <div
      ref={containerRef}
      className="relative w-full h-full"
      style={{ minHeight: 360, background: "var(--bp-surface-0)" }}
      role="application"
      aria-label="Skill knowledge graph. Use Tab to focus a node, Enter to open."
    >
      {size.w > 0 && size.h > 0 && (
        <ForceGraph2D
          ref={fgRef}
          width={size.w}
          height={size.h}
          graphData={data}
          backgroundColor="rgba(0,0,0,0)"
          nodeRelSize={6}
          nodeId="id"
          nodeVal={(n: any) => radiusOf(n as GraphDatum)}
          linkDirectionalParticles={0}
          enableNodeDrag
          enableZoomInteraction
          enablePanInteraction
          cooldownTicks={120}
          warmupTicks={40}
          nodeCanvasObject={paintNode}
          nodePointerAreaPaint={paintPointerArea as any}
          linkCanvasObjectMode={() => "replace" as const}
          linkCanvasObject={paintLink as any}
          onNodeClick={(n: any) => onNodeClick?.((n as GraphDatum) as unknown as GraphNode)}
          onNodeHover={(n: any) => {
            const datum = (n as GraphDatum | null) ?? null;
            setHoveredId(datum?.id ?? null);
            onNodeHover?.(datum ? (datum as unknown as GraphNode) : null);
          }}
        />
      )}
      {tooltip && (
        <div
          className="pointer-events-none absolute z-10 rounded-md border px-3 py-2 text-xs"
          style={{
            left: tooltip.x + 12,
            top: tooltip.y + 12,
            background: "var(--bp-surface-1)",
            borderColor: "var(--bp-border-1)",
            color: "var(--bp-text-0)",
            boxShadow: "var(--bp-shadow-md)",
            maxWidth: 240,
          }}
        >
          <div className="font-semibold">{tooltip.node.name}</div>
          <div className="text-[10px]" style={{ color: "var(--bp-text-2)" }}>
            {tooltip.node.plugin} · {tooltip.node.category}
          </div>
        </div>
      )}
    </div>
  );
}
