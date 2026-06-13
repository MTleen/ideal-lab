"use client";

import { useState } from "react";
import Link from "next/link";
import type { GraphNode, GraphEdge } from "@/lib/types";
import { getNode, getSubgraph, graphEdges } from "@/lib/graph";
import MiniGraph from "@/components/graph-mini/MiniGraph";

interface Props {
  skillId: string;
}

const RELATION_LABELS: Record<string, string> = {
  prerequisite: "upstream (prerequisite)",
  produces_for: "downstream (produces_for)",
  enhancement: "enhancement",
};

export default function SkillRelated({ skillId }: Props) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const center = getNode(skillId);
  if (!center) return null;

  // We need direct neighbors by relation type
  const directUpstream: GraphNode[] = [];
  const directDownstream: GraphNode[] = [];
  const enhancements: GraphNode[] = [];

  for (const e of graphEdges as GraphEdge[]) {
    if (e.target === skillId && e.relation === "prerequisite") {
      const n = getNode(e.source);
      if (n) directUpstream.push(n);
    } else if (e.source === skillId && e.relation === "produces_for") {
      const n = getNode(e.target);
      if (n) directDownstream.push(n);
    } else if (
      (e.target === skillId || e.source === skillId) &&
      e.relation === "enhancement"
    ) {
      const other = e.target === skillId ? e.source : e.target;
      const n = getNode(other);
      if (n) enhancements.push(n);
    }
  }

  const renderGroup = (
    label: string,
    items: GraphNode[],
    key: string,
  ) => {
    if (items.length === 0) return null;
    const isOpen = expanded === key;
    return (
      <div className="mb-2">
        <div className="text-[11px] font-semibold mb-1" style={{ color: "var(--bp-text-1)" }}>
          {label} ({items.length})
        </div>
        <div className="flex flex-wrap gap-1.5">
          {items.map((n) => {
            const itemKey = `${key}-${n.id}`;
            const itemOpen = expanded === itemKey;
            return (
              <span key={n.id}>
                <button
                  onClick={() => setExpanded(itemOpen ? null : itemKey)}
                  className="text-[11px] px-2 py-0.5 rounded-full border transition-colors"
                  style={{
                    background: itemOpen
                      ? "var(--bp-brand-500)"
                      : "var(--bp-surface-1)",
                    borderColor: "var(--bp-border-0)",
                    color: itemOpen ? "#fff" : "var(--bp-text-1)",
                  }}
                >
                  {n.name}
                </button>
              </span>
            );
          })}
        </div>
        {isOpen && (
          <div className="mt-2">
            {items.map((n) => {
              const itemKey = `${key}-${n.id}`;
              if (expanded !== itemKey) return null;
              const sub = getSubgraph(n.id, 1);
              return (
                <div key={n.id}>
                  <div className="text-xs mb-1" style={{ color: "var(--bp-text-1)" }}>
                    <Link
                      href={`/plugins/${n.plugin}/skills/${n.id.split("/")[1]}/`}
                      className="underline-offset-2 hover:underline"
                      style={{ color: "var(--bp-brand-500)" }}
                    >
                      {n.name}
                    </Link>{" "}
                    <span style={{ color: "var(--bp-text-3)" }}>· {n.category}</span>
                  </div>
                  <MiniGraph
                    centerId={n.id}
                    nodes={sub.nodes}
                    edges={sub.edges}
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  return (
    <section
      className="rounded-xl border p-5 my-6"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
      }}
    >
      <h2 className="text-base font-semibold mb-3" style={{ color: "var(--bp-text-0)" }}>
        Related skills
      </h2>
      {renderGroup(RELATION_LABELS.prerequisite, directUpstream, "up")}
      {renderGroup(RELATION_LABELS.produces_for, directDownstream, "down")}
      {renderGroup(RELATION_LABELS.enhancement, enhancements, "enh")}
      {directUpstream.length === 0 &&
        directDownstream.length === 0 &&
        enhancements.length === 0 && (
          <p className="text-sm" style={{ color: "var(--bp-text-3)" }}>
            No related skills registered.
          </p>
        )}
    </section>
  );
}
