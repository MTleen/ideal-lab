"use client";

import { useState, useMemo } from "react";
import type { Task, Relation } from "@/lib/types";
import TaskCard from "./TaskCard";
import { getEdgeCountsByRelation } from "@/lib/graph";
import { getAllTasks, getTasksContainingSkill } from "@/lib/tasks";

interface Props {
  tasks: Task[];
  selectedTaskId: string | null;
  onSelectTask: (id: string | null) => void;
  hoveredSkillId: string | null;
}

const RELATION_LABELS: Record<Relation, string> = {
  enhancement: "enhancement",
  prerequisite: "prerequisite",
  embeds: "embeds",
  produces_for: "produces_for",
  alternative: "alternative",
};

export default function TaskPanel({
  tasks,
  selectedTaskId,
  onSelectTask,
  hoveredSkillId,
}: Props) {
  const [selectedRelations, setSelectedRelations] = useState<Set<Relation>>(new Set());
  const edgeCounts = useMemo(() => getEdgeCountsByRelation(), []);

  /* Reverse-link: tasks that include the hovered skill */
  const highlightedTaskIds = useMemo(() => {
    if (!hoveredSkillId) return new Set<string>();
    return new Set(getTasksContainingSkill(hoveredSkillId).map((t) => t.id));
  }, [hoveredSkillId]);

  const toggleRelation = (r: Relation) => {
    const next = new Set(selectedRelations);
    if (next.has(r)) next.delete(r);
    else next.add(r);
    setSelectedRelations(next);
  };

  const handleSelect = (id: string) => {
    onSelectTask(selectedTaskId === id ? null : id);
  };

  const totalTasks = getAllTasks().length;

  return (
    <aside
      className="flex flex-col h-full overflow-hidden"
      style={{ background: "var(--bp-surface-0)" }}
      aria-label="Task panel"
    >
      <div className="px-4 pt-4 pb-2">
        <h2 className="text-sm font-semibold mb-1" style={{ color: "var(--bp-text-0)" }}>
          Tasks
        </h2>
        <p className="text-[11px]" style={{ color: "var(--bp-text-2)" }}>
          {totalTasks} scenarios · click to highlight involved skills
        </p>
      </div>

      <div className="flex-1 overflow-y-auto px-4 pb-3 space-y-2">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            isSelected={selectedTaskId === task.id}
            isHighlighted={highlightedTaskIds.has(task.id) && selectedTaskId !== task.id}
            onClick={() => handleSelect(task.id)}
          />
        ))}
      </div>

      <div
        className="px-4 py-3 border-t space-y-2"
        style={{ borderColor: "var(--bp-border-0)" }}
      >
        <div className="text-[11px] font-semibold" style={{ color: "var(--bp-text-1)" }}>
          Relation type
        </div>
        <div className="space-y-1">
          {(Object.keys(RELATION_LABELS) as Relation[]).map((r) => (
            <label
              key={r}
              className="flex items-center gap-2 text-[11px] cursor-pointer"
              style={{ color: "var(--bp-text-1)" }}
            >
              <input
                type="checkbox"
                checked={selectedRelations.has(r)}
                onChange={() => toggleRelation(r)}
                style={{ accentColor: "var(--bp-task-checkbox-accent)" }}
              />
              <span>{RELATION_LABELS[r]}</span>
              <span style={{ color: "var(--bp-text-3)" }}>({edgeCounts[r]})</span>
            </label>
          ))}
        </div>
        {(selectedTaskId || selectedRelations.size > 0) && (
          <button
            onClick={() => {
              onSelectTask(null);
              setSelectedRelations(new Set());
            }}
            className="text-[11px] font-medium mt-1"
            style={{ color: "var(--bp-brand-500)" }}
          >
            Clear filters
          </button>
        )}
      </div>
    </aside>
  );
}
