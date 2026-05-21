import Link from "next/link";
import type { PluginData } from "@/lib/types";
import { getCategory, detectCategory } from "@/lib/utils";

export default function PluginCard({ plugin }: { plugin: PluginData }) {
  const cat = getCategory(detectCategory(plugin));

  return (
    <Link
      href={`/plugins/${plugin.slug}`}
      className="group block rounded-xl border transition-all duration-200 overflow-hidden no-underline"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
        boxShadow: "var(--bp-shadow-sm)",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-4px)";
        e.currentTarget.style.boxShadow = "var(--bp-shadow-lg)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "var(--bp-shadow-sm)";
      }}
    >
      {/* Category color strip */}
      <div className="h-1 w-full" style={{ background: cat.color }} />

      <div className="p-5">
        {/* Category label */}
        <div
          className="text-[10px] font-medium tracking-widest uppercase mb-2"
          style={{ color: cat.color }}
        >
          {cat.label}
        </div>

        {/* Name */}
        <h3
          className="text-lg font-semibold mb-2 leading-tight"
          style={{ color: "var(--bp-text-0)" }}
        >
          {plugin.meta.name}
        </h3>

        {/* Description */}
        <p
          className="text-sm leading-relaxed mb-4 line-clamp-2"
          style={{ color: "var(--bp-text-2)" }}
        >
          {plugin.meta.description}
        </p>

        {/* Skill badges */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {plugin.skills.slice(0, 3).map((s) => (
            <span
              key={s.slug}
              className="text-[11px] font-medium px-2 py-0.5 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-text-1)",
              }}
            >
              {s.name}
            </span>
          ))}
          {plugin.skills.length > 3 && (
            <span
              className="text-[11px] font-medium px-2 py-0.5 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-text-3)",
              }}
            >
              +{plugin.skills.length - 3}
            </span>
          )}
        </div>

        {/* Meta bar */}
        <div className="flex items-center gap-3 text-[11px]" style={{ color: "var(--bp-text-3)" }}>
          <span>v{plugin.meta.version}</span>
          <span>{plugin.skillCount} skills</span>
        </div>
      </div>
    </Link>
  );
}
