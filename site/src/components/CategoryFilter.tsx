"use client";

import type { CategoryInfo } from "@/lib/types";

interface Props {
  categories: CategoryInfo[];
  selected: string;
  onSelect: (slug: string) => void;
}

export default function CategoryFilter({
  categories,
  selected,
  onSelect,
}: Props) {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <button
        onClick={() => onSelect("all")}
        className="text-sm font-medium px-4 py-1.5 rounded-full transition-colors h-8"
        style={
          selected === "all"
            ? {
                background: "var(--bp-brand-500)",
                color: "#fff",
              }
            : {
                background: "var(--bp-surface-2)",
                color: "var(--bp-text-1)",
              }
        }
      >
        All
      </button>
      {categories.map((cat) => (
        <button
          key={cat.slug}
          onClick={() => onSelect(cat.slug)}
          className="text-sm font-medium px-4 py-1.5 rounded-full transition-colors h-8"
          style={
            selected === cat.slug
              ? {
                  background: cat.color,
                  color: "#fff",
                }
              : {
                  background: "var(--bp-surface-2)",
                  color: "var(--bp-text-1)",
                }
          }
        >
          {cat.label}
        </button>
      ))}
    </div>
  );
}
