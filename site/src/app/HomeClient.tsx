"use client";

import { useState, useMemo, useCallback, useEffect } from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { GraphNode, CategoryInfo } from "@/lib/types";
import { getAllTasks, getTasksContainingSkill } from "@/lib/tasks";
import { graphNodes, graphEdges, getNode, getEdgeCountsByRelation } from "@/lib/graph";
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
  /* Visible relations = only the three edge types painted on the canvas
   * (prerequisite / calls / produces_for). enhancement / alternative are
   * hidden cross-cutting noise, so we don't advertise their count. */
  const visibleRelations = useMemo(() => {
    const c = getEdgeCountsByRelation();
    return c.prerequisite + c.calls + c.produces_for;
  }, []);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [hoveredSkillId, setHoveredSkillId] = useState<string | null>(null);
  const [scriptVisible, setScriptVisible] = useState(false);
  /* Defer mounting of the (graphically rich) TaskPanel for one tick so it
   * fades in alongside GraphCanvas instead of popping in next to the loader. */
  const [panelReady, setPanelReady] = useState(false);
  useEffect(() => {
    const t = window.setTimeout(() => setPanelReady(true), 120);
    return () => window.clearTimeout(t);
  }, []);

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

  const router = useRouter();
  const handleNodeClick = useCallback(
    (node: GraphNode) => {
      const [plugin, skill] = node.id.split("/");
      // Use router.push so basePath is applied automatically
      router.push(`/plugins/${plugin}/skills/${skill}/`);
    },
    [router],
  );

  return (
    <div>
      {/* Hero band */}
      <section className="container-site pt-8 pb-12">
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
          Plugins that compose into working Claude Code workflows
        </h1>
        <p
          className="max-w-2xl leading-relaxed mb-5"
          style={{ fontSize: 17, color: "var(--bp-text-1)" }}
        >
          Click any skill to see what it does, who uses it, and which problems it solves.
          Pick a task to highlight the skills that work together.
        </p>
        {/* Metadata strip — kept monotone to avoid competing with H1 */}
        <div
          className="flex flex-wrap items-center gap-x-6 gap-y-1 text-[13px] font-mono"
          style={{ color: "var(--bp-text-2)" }}
        >
          <span>{graphNodes.length} skills</span>
          <span style={{ color: "var(--bp-text-3)" }}>·</span>
          <span>{pluginSlugs.length} plugins</span>
          <span style={{ color: "var(--bp-text-3)" }}>·</span>
          <span>{visibleRelations} relations</span>
        </div>
      </section>

      {/* Graph + Task Panel split */}
      <section className="container-site pb-12">
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
          {panelReady ? (
            <TaskPanel
              tasks={tasks}
              selectedTaskId={selectedTaskId}
              onSelectTask={handleSelectTask}
              hoveredSkillId={hoveredSkillId}
            />
          ) : (
            <aside
              className="flex flex-col h-full overflow-hidden p-4 gap-2"
              style={{ background: "var(--bp-surface-0)" }}
              aria-hidden="true"
            >
              <div className="skeleton h-3 w-16" />
              <div className="skeleton h-2 w-32 mb-3" />
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="skeleton h-12 w-full" />
              ))}
            </aside>
          )}
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

      {/* Common problems (top 4 plugins, mixed sizes for rhythm) */}
      <section className="container-site py-12">
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
          style={{
            /* Asymmetric 2-col: one wider card + a 2x2 stack on desktop, single col on mobile */
            gridTemplateColumns: "minmax(0, 1.4fr) minmax(0, 1fr)",
            gridAutoRows: "minmax(0, auto)",
          }}
        >
          {pluginSlugs.slice(0, 4).map((slug, i) => {
            const pp = getPluginPainPoints(slug);
            if (pp.length === 0) return null;
            const first = pp[0];
            const featured = i === 0;
            return (
              <Link
                key={slug}
                href={`/plugins/${slug}/`}
                className="block rounded-lg border p-4 transition-all no-underline"
                style={{
                  background: "var(--bp-surface-1)",
                  borderColor: "var(--bp-border-0)",
                  color: "inherit",
                  gridColumn: featured ? "1 / -1" : "auto",
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

      {/* All plugins — list (NOT a uniform card grid) */}
      <section className="container-site py-12">
        <div className="flex items-baseline justify-between mb-2">
          <h2
            className="text-2xl font-bold"
            style={{ color: "var(--bp-text-0)" }}
          >
            All plugins
          </h2>
          <span
            className="text-sm font-mono"
            style={{ color: "var(--bp-text-3)" }}
          >
            {pluginSlugs.length}
          </span>
        </div>
        <p className="text-sm mb-6" style={{ color: "var(--bp-text-2)" }}>
          Browse by category or jump into a specific plugin.
        </p>
        <ul
          className="divide-y rounded-lg border overflow-hidden"
          style={{ borderColor: "var(--bp-border-0)" }}
        >
          {pluginSlugs.map((slug) => (
            <li key={slug}>
              <Link
                href={`/plugins/${slug}/`}
                className="flex items-center justify-between px-4 py-2.5 text-sm transition-colors no-underline hover:bg-[var(--bp-surface-1)]"
                style={{ color: "var(--bp-text-0)" }}
              >
                <span className="font-medium">{slug}</span>
                <span
                  className="text-[11px] font-mono"
                  style={{ color: "var(--bp-text-3)" }}
                >
                  →
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
