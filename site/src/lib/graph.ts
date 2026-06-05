import graphData from "../../../skills-graph.json";
import type { GraphNode, GraphEdge, SkillsGraph, Relation } from "./types";

/* Loaded once at module init (build-time IO) */

const graph = graphData as unknown as SkillsGraph;

export const graphNodes: GraphNode[] = graph.nodes;
export const graphEdges: GraphEdge[] = graph.edges;
export const graphMetadata = graph.metadata;

/* Indexed lookups */

const nodeById = new Map(graphNodes.map((n) => [n.id, n]));
const nodesByPlugin = new Map<string, GraphNode[]>();
for (const node of graphNodes) {
  const arr = nodesByPlugin.get(node.plugin) ?? [];
  arr.push(node);
  nodesByPlugin.set(node.plugin, arr);
}

const outEdges = new Map<string, GraphEdge[]>();
const inEdges = new Map<string, GraphEdge[]>();
for (const edge of graphEdges) {
  const o = outEdges.get(edge.source) ?? [];
  o.push(edge);
  outEdges.set(edge.source, o);
  const i = inEdges.get(edge.target) ?? [];
  i.push(edge);
  inEdges.set(edge.target, i);
}

/* ── Public API ── */

export function getNode(id: string): GraphNode | undefined {
  return nodeById.get(id);
}

export function getPluginCluster(slug: string): GraphNode[] {
  return nodesByPlugin.get(slug) ?? [];
}

export function getInDegree(id: string): number {
  return inEdges.get(id)?.length ?? 0;
}

export function getOutDegree(id: string): number {
  return outEdges.get(id)?.length ?? 0;
}

export function getRelated(
  id: string,
): { upstream: GraphNode[]; downstream: GraphNode[]; enhancement: GraphNode[] } {
  const upstream: GraphNode[] = [];
  const downstream: GraphNode[] = [];
  const enhancement: GraphNode[] = [];

  for (const e of inEdges.get(id) ?? []) {
    const n = nodeById.get(e.source);
    if (!n) continue;
    if (e.relation === "prerequisite") upstream.push(n);
    else if (e.relation === "enhancement") enhancement.push(n);
  }
  for (const e of outEdges.get(id) ?? []) {
    const n = nodeById.get(e.target);
    if (!n) continue;
    if (e.relation === "prerequisite" || e.relation === "produces_for") downstream.push(n);
  }
  return { upstream, downstream, enhancement };
}

/* 1-hop subgraph for mini graph (center + direct neighbors) */
export function getSubgraph(centerId: string, depth = 1): { nodes: GraphNode[]; edges: GraphEdge[] } {
  const visited = new Set<string>([centerId]);
  const queue: Array<{ id: string; d: number }> = [{ id: centerId, d: 0 }];
  const collected: GraphEdge[] = [];

  while (queue.length > 0) {
    const { id, d } = queue.shift()!;
    if (d >= depth) continue;
    for (const e of inEdges.get(id) ?? []) {
      collected.push(e);
      if (!visited.has(e.source)) {
        visited.add(e.source);
        queue.push({ id: e.source, d: d + 1 });
      }
    }
    for (const e of outEdges.get(id) ?? []) {
      collected.push(e);
      if (!visited.has(e.target)) {
        visited.add(e.target);
        queue.push({ id: e.target, d: d + 1 });
      }
    }
  }

  return {
    nodes: Array.from(visited)
      .map((id) => nodeById.get(id))
      .filter((n): n is GraphNode => Boolean(n)),
    edges: collected,
  };
}

/* Edge counts for legend */
export function getEdgeCountsByRelation(): Record<Relation, number> {
  const counts: Record<Relation, number> = {
    enhancement: 0,
    prerequisite: 0,
    calls: 0,
    produces_for: 0,
    alternative: 0,
  };
  for (const e of graphEdges) counts[e.relation]++;
  return counts;
}
