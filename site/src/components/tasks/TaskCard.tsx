"use client";

import { useState } from "react";
import type { Task } from "@/lib/types";

interface Props {
  task: Task;
  isSelected: boolean;
  isHighlighted: boolean;
  onClick: () => void;
}

const SCOPE_META: Record<string, { label: string; color: string }> = {
  lead: { label: "主导", color: "#7b5cea" },
  support: { label: "辅助", color: "#0ea5a0" },
  infra: { label: "基建", color: "#d98b0a" },
};

export default function TaskCard({ task, isSelected, isHighlighted, onClick }: Props) {
  const [focused, setFocused] = useState(false);
  const scope = SCOPE_META[task.scope] ?? SCOPE_META.lead;

  return (
    <button
      type="button"
      onClick={onClick}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      className="text-left w-full rounded-lg border px-4 py-3 transition-all"
      style={{
        background: isSelected
          ? "var(--bp-task-card-selected-bg)"
          : "var(--bp-task-card-bg)",
        borderColor: isHighlighted
          ? "var(--bp-task-card-highlight-border)"
          : focused
            ? "var(--bp-task-card-border-hover)"
            : "var(--bp-task-card-border)",
        boxShadow: isSelected ? "var(--bp-shadow-sm)" : "none",
        cursor: "pointer",
      }}
      aria-pressed={isSelected}
    >
      <div className="flex items-start justify-between gap-2 mb-1.5">
        <h3
          className="text-sm font-semibold leading-snug"
          style={{ color: "var(--bp-text-0)" }}
        >
          {task.title}
        </h3>
        <span
          className="text-[10px] font-medium px-1.5 py-0.5 rounded shrink-0"
          style={{
            background: "var(--bp-task-pill-bg)",
            color: scope.color,
          }}
        >
          {scope.label}
        </span>
      </div>
      <div className="flex items-center gap-2 text-[11px]" style={{ color: "var(--bp-text-2)" }}>
        <span>{task.skillIds.length} 个技能</span>
        <span>·</span>
        <span>{task.estimatedSteps} 步</span>
      </div>
    </button>
  );
}
