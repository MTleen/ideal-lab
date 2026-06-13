"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import ForceGraph2D, { ForceGraphMethods } from "react-force-graph-2d";
import type { GraphNode, GraphEdge, Relation } from "@/lib/types";
import GraphControls from "./GraphControls";

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

/* Relations that describe a real skill→skill flow and should be drawn.
 * enhancement / alternative are cross-cutting noise (panel-review, deep-research
 * and skill-builder fan out one-to-many) — kept only for force clustering and
 * the skill detail "Related skills" section, never painted on the canvas.
 * This is the fix for the old "render only calls" policy, which starved the
 * graph of its prerequisite skeleton and left 54% of nodes isolated. */
const VISIBLE_RELATIONS: Record<Relation, boolean> = {
  prerequisite: true,
  calls: true,
  produces_for: true,
  enhancement: false,
  alternative: false,
};

interface GraphDatum {
  id: string;
  name: string;
  plugin: string;
  category: string;
  inDegree: number;
  // d3-force injects:
  x?: number;
  y?: number;
  fx?: number;
  fy?: number;
}

interface LinkDatum {
  source: string | GraphDatum;
  target: string | GraphDatum;
  relation: Relation;
}

type Palette = {
  cat: Record<string, string>;
  edge: { prerequisite: string; calls: string; produces_for: string };
};

const FALLBACK_PALETTE: Palette = {
  cat: {
    development: "#7b5cea",
    content: "#0ea5a0",
    research: "#d98b0a",
    knowledge: "#8ba60a",
    tooling: "#9b6cea",
    other: "#6e6e82",
  },
  edge: {
    prerequisite: "#7b5cea",
    calls: "#6b7280",
    produces_for: "#d98b0a",
  },
};

/* Read colors from CSS tokens (not hardcoded hex) so the canvas tracks the
 * design system and adapts to dark mode. */
function readPalette(): Palette {
  if (typeof window === "undefined") return FALLBACK_PALETTE;
  const cs = getComputedStyle(document.documentElement);
  const token = (n: string) => cs.getPropertyValue(n).trim();
  const cat = (key: string, fb: string) =>
    token(`--bp-graph-cat-${key}`) || fb;
  const edge = (n: string, fb: string) => token(n) || fb;
  return {
    cat: {
      development: cat("development", FALLBACK_PALETTE.cat.development),
      content: cat("content", FALLBACK_PALETTE.cat.content),
      research: cat("research", FALLBACK_PALETTE.cat.research),
      knowledge: cat("knowledge", FALLBACK_PALETTE.cat.knowledge),
      tooling: cat("tooling", FALLBACK_PALETTE.cat.tooling),
      other: FALLBACK_PALETTE.cat.other,
    },
    edge: {
      prerequisite: edge("--bp-graph-edge-prerequisite", FALLBACK_PALETTE.edge.prerequisite),
      calls: edge("--bp-graph-edge-calls", FALLBACK_PALETTE.edge.calls),
      produces_for: edge("--bp-graph-edge-produces-for", FALLBACK_PALETTE.edge.produces_for),
    },
  };
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
  const paletteRef = useRef<Palette>(readPalette());
  const [, bumpRender] = useState(0);

  const highlightSet = useMemo(() => new Set(highlightedSkillIds), [highlightedSkillIds]);

  /* Re-read tokens when the theme (.dark) toggles so canvas colors follow
   * light/dark without any hardcoded value. */
  useEffect(() => {
    const apply = () => {
      paletteRef.current = readPalette();
      bumpRender((n) => n + 1);
      fgRef.current?.d3ReheatSimulation();
    };
    const mo = new MutationObserver(apply);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
    return () => mo.disconnect();
  }, []);

  /* in-degree counts ONLY visible relations (the ones we paint), so node size
   * reflects what the user can actually see. Synthetic intra-plugin clustering
   * edges are appended afterwards for force-layout grouping only. */
  const data = useMemo(() => {
    const inDeg = new Map<string, number>();
    for (const e of edges) {
      if (!VISIBLE_RELATIONS[e.relation]) continue;
      inDeg.set(e.target, (inDeg.get(e.target) ?? 0) + 1);
    }

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

    /* Hidden intra-plugin clustering edges (never painted; force-layout only) */
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

  /* Seed node positions with the golden-angle spiral so the simulation starts
   * from a sensible layout instead of a centroid pile-up. */
  const seedPositions = (w: number, h: number) => {
    data.nodes.forEach((n: any, i: number) => {
      const angle = i * 2.39996;
      const radius = Math.min(w, h) * 0.35 * Math.sqrt((i + 1) / data.nodes.length);
      n.x = w / 2 + radius * Math.cos(angle);
      n.y = h / 2 + radius * Math.sin(angle);
      n.fx = undefined;
      n.fy = undefined;
    });
  };

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

  /* Apply d3-force config + pre-warm simulation (respects prefers-reduced-motion) */
  useEffect(() => {
    const fg = fgRef.current;
    if (!fg) return;
    const w = size.w || 800;
    const h = size.h || 600;
    seedPositions(w, h);

    const reduceMotion =
      typeof window !== "undefined" &&
      window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

    if (reduceMotion) {
      for (const n of data.nodes) {
        (n as any).fx = n.x;
        (n as any).fy = n.y;
      }
      return;
    }

    fg.d3ReheatSimulation();
    fg.d3Force("charge")?.strength(-380);
    fg.d3Force("link")?.distance((l: any) => (l.relation === "enhancement" ? 40 : 80));
    fg.d3Force("center")?.strength(0.05);
    fg.d3Force("collide", (window as any).d3?.forceCollide?.(28));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, size.w, size.h]);

  const handleReset = () => {
    const fg = fgRef.current;
    if (!fg) return;
    seedPositions(size.w || 800, size.h || 600);
    fg.d3ReheatSimulation();
  };

  /* Node radius from visible in-degree. */
  const radiusOf = (n: GraphDatum) =>
    Math.max(18, Math.min(36, Math.sqrt(n.inDegree + 1) * 9));

  const isDim = (n: GraphDatum) =>
    highlightSet.size > 0 && !highlightSet.has(n.id) && n.id !== focusedSkillId;
  const isFocused = (n: GraphDatum) => n.id === focusedSkillId;

  /* Custom node paint. */
  const paintNode = (node: GraphDatum, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const r = radiusOf(node);
    const x = node.x ?? 0;
    const y = node.y ?? 0;
    const color = paletteRef.current.cat[node.category] ?? paletteRef.current.cat.other;
    const dimmed = isDim(node);

    /* Focus glow */
    if (isFocused(node)) {
      ctx.beginPath();
      ctx.arc(x, y, r + 6, 0, 2 * Math.PI);
      ctx.fillStyle = "rgba(123, 92, 234, 0.35)";
      ctx.fill();
    }

    ctx.globalAlpha = dimmed ? 0.25 : highlightSet.has(node.id) || isFocused(node) ? 1 : 0.95;

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
    const maxChars = Math.max(5, Math.floor((r * 1.6) / fontSize));
    const displayLabel = label.length > maxChars ? label.slice(0, maxChars - 1) + "…" : label;
    ctx.fillText(displayLabel, x, y);

    /* Larger tooltip-style label on focus */
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

  /* Arrowhead at the target end of a link, inset by the node radius. */
  const drawArrow = (
    ctx: CanvasRenderingContext2D,
    fromX: number, fromY: number,
    toX: number, toY: number,
    inset: number,
  ) => {
    const ang = Math.atan2(toY - fromY, toX - fromX);
    const size = 7;
    const tipX = toX - inset * Math.cos(ang);
    const tipY = toY - inset * Math.sin(ang);
    ctx.beginPath();
    ctx.moveTo(tipX, tipY);
    ctx.lineTo(tipX - size * Math.cos(ang - Math.PI / 6), tipY - size * Math.sin(ang - Math.PI / 6));
    ctx.lineTo(tipX + size * Math.cos(ang - Math.PI / 6), tipY + size * Math.sin(ang - Math.PI / 6));
    ctx.closePath();
    ctx.fill();
  };

  /* Custom link paint — render the three flow relations with distinct styles:
   *   prerequisite  solid + arrowhead (phase ordering, the workflow backbone)
   *   calls         thin solid, no head (orchestrator invokes phase skills)
   *   produces_for  dashed + arrowhead (utility output consumed downstream)
   * enhancement / alternative / synthetic clustering edges are skipped. */
  const paintLink = (link: LinkDatum, ctx: CanvasRenderingContext2D) => {
    if (!VISIBLE_RELATIONS[link.relation]) return;
    const src = link.source as GraphDatum;
    const tgt = link.target as GraphDatum;
    if (typeof src.x !== "number" || typeof tgt.x !== "number") return;

    const relation = link.relation as "prerequisite" | "calls" | "produces_for";
    const dim = isDim(src) || isDim(tgt);
    const color = paletteRef.current.edge[relation];

    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.globalAlpha = dim ? 0.12 : 0.7;

    if (relation === "produces_for") {
      ctx.setLineDash([5, 3]);
      ctx.lineWidth = 1.4;
    } else if (relation === "prerequisite") {
      ctx.setLineDash([]);
      ctx.lineWidth = 1.5;
    } else {
      ctx.setLineDash([]);
      ctx.lineWidth = 1;
    }

    ctx.beginPath();
    ctx.moveTo(src.x!, src.y!);
    ctx.lineTo(tgt.x!, tgt.y!);
    ctx.stroke();

    if (relation !== "calls") {
      drawArrow(ctx, src.x!, src.y!, tgt.x!, tgt.y!, radiusOf(tgt) + 2);
    }
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
          cooldownTicks={typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ? 0 : 120}
          warmupTicks={typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ? 0 : 40}
          nodeCanvasObject={paintNode}
          nodePointerAreaPaint={paintPointerArea as any}
          linkCanvasObjectMode={() => "replace" as const}
          linkCanvasObject={paintLink as any}
          onNodeClick={(n: any) => onNodeClick?.((n as GraphDatum) as unknown as GraphNode)}
          onNodeHover={(n: any) => {
            const datum = (n as GraphDatum | null) ?? null;
            onNodeHover?.(datum ? (datum as unknown as GraphNode) : null);
          }}
        />
      )}
      <GraphControls onReset={handleReset} />
    </div>
  );
}
