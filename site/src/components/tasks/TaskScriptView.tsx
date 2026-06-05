"use client";

import Link from "next/link";
import type { Task } from "@/lib/types";
import { getNode } from "@/lib/graph";

interface Props {
  task: Task;
  onClose: () => void;
}

export default function TaskScriptView({ task, onClose }: Props) {
  return (
    <div
      className="rounded-xl border p-5 mt-4"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
        boxShadow: "var(--bp-shadow-md)",
      }}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h2 className="text-xl font-bold mb-1" style={{ color: "var(--bp-text-0)" }}>
            {task.title}
          </h2>
          <p className="text-sm" style={{ color: "var(--bp-text-2)" }}>
            {task.problem}
          </p>
        </div>
        <button
          onClick={onClose}
          aria-label="Close task script"
          className="shrink-0 w-8 h-8 flex items-center justify-center rounded-full transition-colors hover:bg-[var(--bp-surface-2)]"
          style={{ color: "var(--bp-text-1)" }}
        >
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M4 4l8 8M12 4l-8 8" strokeLinecap="round" />
          </svg>
        </button>
      </div>

      <div
        className="text-sm mb-4 px-3 py-2 rounded-md border-l-2"
        style={{
          background: "var(--bp-surface-2)",
          color: "var(--bp-text-1)",
          borderColor: "var(--bp-brand-500)",
        }}
      >
        <span className="font-semibold" style={{ color: "var(--bp-text-0)" }}>
          Outcome:
        </span>{" "}
        {task.outcome}
      </div>

      <h3 className="text-sm font-semibold mb-2" style={{ color: "var(--bp-text-0)" }}>
        Steps ({task.estimatedSteps})
      </h3>
      <ol className="space-y-1.5 text-sm">
        {task.skillIds.map((id, i) => {
          const node = getNode(id);
          return (
            <li key={id} className="flex items-start gap-2">
              <span
                className="shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-semibold"
                style={{
                  background: "var(--bp-brand-500)",
                  color: "#fff",
                }}
              >
                {i + 1}
              </span>
              <Link
                href={`/plugins/${id.split("/")[0]}/skills/${id.split("/")[1]}/`}
                className="underline-offset-2 hover:underline"
                style={{ color: "var(--bp-brand-500)" }}
              >
                {node?.name ?? id}
              </Link>
              <span className="text-xs" style={{ color: "var(--bp-text-3)" }}>
                {node?.category}
              </span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
