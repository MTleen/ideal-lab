"use client";

import { useState, useMemo, useCallback, useEffect } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import type { GraphNode, Task, CategoryInfo } from "@/lib/types";
import { getAllTasks, getTasksContainingSkill } from "@/lib/tasks";
import { graphNodes, graphEdges, getNode } from "@/lib/graph";
import { getPluginPainPoints } from "@/lib/plugin-pain-points";
import TaskPanel from "@/components/tasks/TaskPanel";
import TaskScriptView from "@/components/tasks/TaskScriptView";
import GraphLegend from "@/components/graph/GraphLegend";

const GraphCanvas = dynamic(() => import("@/components/graph/GraphCanvas"), {
  ssr: false,
  loading: () => (
    <div
      className="w-full h-full flex items-center justify-center"
      style={{ minHeight: 360, background: "var(--bp-surface-0)" }}
    >
      <p className="text-sm" style={{ color: "var(--bp-text-2)" }}>
        Loading knowledge graph...
      </p>
    </div>
  ),
});

interface Props {
  categories: CategoryInfo[];
  pluginSlugs: string[];
}

export default function HomeClient({ categories, pluginSlugs }: Props) {
  const tasks = useMemo(() => getAllTasks(), []);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [hoveredSkillId, setHoveredSkillId] = useState<string | null>(null);
  const [scriptVisible, setScriptVisible] = useState(false);

  /* Read task from URL */
  useEffect(() => {
    if (typeof window === "undefined") return;
    const params = new URLSearchParams(window.location.search);
    const t = params.get("task");
    if (t && tasks.find((x) => x.id === t)) {
      setSelectedTaskId(t);
      setScriptVisible(true);
    }
  }, [tasks]);

  /* Write task to URL */
  const handleSelectTask = useCallback(
    (id: string | null) => {
      setSelectedTaskId(id);
      setScriptVisible(id !== null);
      if (typeof window !== "undefined") {
        const url = new URL(window.location.href);
        if (id) url.searchParams.set("task", id);
        else url.searchParams.delete("task");
        window.history.replaceState(null, "", url.toString());
      }
    },
    [],
  );

  const selectedTask = useMemo(
    () => (selectedTaskId ? tasks.find((t) => t.id === selectedTaskId) ?? null : null),
    [selectedTaskId, tasks],
  );

  const highlightedSkillIds = useMemo(
    () => (selectedTask ? selectedTask.skillIds : []),
    [selectedTask],
  );

  const handleNodeClick = useCallback((node: GraphNode) => {
    const [plugin, skill] = node.id.split("/");
    window.location.href = `/plugins/${plugin}/skills/${skill}/`;
  }, []);

  return (
    <div>
      {/* Hero band */}
      <section className="container-site pt-8 pb-4">
        <div
          className="inline-block text-[11px] font-medium tracking-widest uppercase mb-3 px-3 py-1 rounded-full"
          style={{
            background: "var(--bp-surface-2)",
            color: "var(--bp-brand-500)",
          }}
        >
          Best Practices
        </div>
        <h1
          className="font-black leading-[1.05] tracking-[-0.03em] mb-3"
          style={{
            fontSize: "clamp(32px, 4.5vw, 56px)",
            color: "var(--bp-text-0)",
            maxWidth: 720,
          }}
        >
          {graphNodes.length} skills · {pluginSlugs.length} plugins · {graphEdges.length} relations
        </h1>
        <p
          className="max-w-2xl leading-relaxed"
          style={{ fontSize: 17, color: "var(--bp-text-1)" }}
        >
          Click any skill to see what it does, who uses it, and which problems it solves.
          Pick a task to highlight the skills that work together.
        </p>
      </section>

      {/* Graph + Task Panel split */}
      <section className="container-site pb-8">
        <div
          className="grid gap-4 rounded-xl border overflow-hidden"
          style={{
            gridTemplateColumns: "minmax(0, 7fr) minmax(280px, 3fr)",
            borderColor: "var(--bp-border-0)",
            background: "var(--bp-surface-1)",
            height: "min(70vh, 660px)",
          }}
        >
          <div className="relative h-full overflow-hidden">
            <GraphCanvas
              nodes={graphNodes}
              edges={graphEdges}
              highlightedSkillIds={highlightedSkillIds}
              focusedSkillId={hoveredSkillId}
              onNodeClick={handleNodeClick}
              onNodeHover={(n) => setHoveredSkillId(n?.id ?? null)}
            />
          </div>
          <TaskPanel
            tasks={tasks}
            selectedTaskId={selectedTaskId}
            onSelectTask={handleSelectTask}
            hoveredSkillId={hoveredSkillId}
          />
        </div>
        {/* Legend as bottom strip — gives graph full vertical space */}
        <div
          className="mt-3 flex flex-wrap items-center"
        >
          <GraphLegend />
        </div>
        <style>{`
          @media (max-width: 900px) {
            .container-site > .grid { grid-template-columns: 1fr !important; }
          }
        `}</style>
      </section>

      {/* Task script (when selected) */}
      {scriptVisible && selectedTask && (
        <section className="container-site">
          <TaskScriptView
            task={selectedTask}
            onClose={() => {
              handleSelectTask(null);
              setScriptVisible(false);
            }}
          />
        </section>
      )}

      {/* Plugin index with pain points (top 4) */}
      <section className="container-site pt-8 pb-4">
        <h2
          className="text-2xl font-bold mb-2"
          style={{ color: "var(--bp-text-0)" }}
        >
          Common problems
        </h2>
        <p className="text-sm mb-6" style={{ color: "var(--bp-text-2)" }}>
          Each plugin solves real pain points documented from its SKILL.md capabilities.
        </p>
        <div
          className="grid gap-4"
          style={{ gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}
        >
          {pluginSlugs.slice(0, 4).map((slug) => {
            const pp = getPluginPainPoints(slug);
            if (pp.length === 0) return null;
            const first = pp[0];
            return (
              <Link
                key={slug}
                href={`/plugins/${slug}/`}
                className="block rounded-lg border p-4 transition-all no-underline"
                style={{
                  background: "var(--bp-surface-1)",
                  borderColor: "var(--bp-border-0)",
                  color: "inherit",
                }}
              >
                <div
                  className="text-[10px] font-medium tracking-widest uppercase mb-1.5"
                  style={{ color: "var(--bp-brand-500)" }}
                >
                  {slug}
                </div>
                <h3
                  className="text-sm font-semibold mb-1.5"
                  style={{ color: "var(--bp-text-0)" }}
                >
                  {first.title}
                </h3>
                <p
                  className="text-xs leading-relaxed"
                  style={{ color: "var(--bp-text-2)" }}
                >
                  {first.detail.slice(0, 120)}…
                </p>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Plugin grid */}
      <section className="container-site py-8">
        <h2
          className="text-2xl font-bold mb-2"
          style={{ color: "var(--bp-text-0)" }}
        >
          All plugins ({pluginSlugs.length})
        </h2>
        <p className="text-sm mb-6" style={{ color: "var(--bp-text-2)" }}>
          Browse by category or jump into a specific plugin.
        </p>
        <div
          className="grid gap-3"
          style={{ gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))" }}
        >
          {pluginSlugs.map((slug) => (
            <Link
              key={slug}
              href={`/plugins/${slug}/`}
              className="rounded-lg border px-3 py-2.5 text-sm transition-colors no-underline"
              style={{
                background: "var(--bp-surface-1)",
                borderColor: "var(--bp-border-0)",
                color: "var(--bp-text-0)",
              }}
            >
              {slug}
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
