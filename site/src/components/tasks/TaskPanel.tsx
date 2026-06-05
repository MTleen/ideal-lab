"use client";

import { useMemo } from "react";
import type { Task } from "@/lib/types";
import TaskCard from "./TaskCard";
import { getTasksContainingSkill } from "@/lib/tasks";

interface Props {
  tasks: Task[];
  selectedTaskId: string | null;
  onSelectTask: (id: string | null) => void;
  hoveredSkillId: string | null;
}

export default function TaskPanel({
  tasks,
  selectedTaskId,
  onSelectTask,
  hoveredSkillId,
}: Props) {
  /* Reverse-link: tasks that include the hovered skill */
  const highlightedTaskIds = useMemo(() => {
    if (!hoveredSkillId) return new Set<string>();
    return new Set(getTasksContainingSkill(hoveredSkillId).map((t) => t.id));
  }, [hoveredSkillId]);

  const handleSelect = (id: string) => {
    onSelectTask(selectedTaskId === id ? null : id);
  };

  const totalTasks = tasks.length;

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
    </aside>
  );
}
