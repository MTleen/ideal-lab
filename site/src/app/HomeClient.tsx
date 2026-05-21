"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { PluginData, CategoryInfo } from "@/lib/types";
import PluginCard from "@/components/PluginCard";
import SearchBar from "@/components/SearchBar";
import CategoryFilter from "@/components/CategoryFilter";
import { formatDate } from "@/lib/utils";

interface Props {
  plugins: PluginData[];
  categories: CategoryInfo[];
}

export default function HomeClient({
  plugins,
  categories,
}: Props) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");

  const filtered = useMemo(() => {
    let results = plugins;

    // Category filter
    if (category !== "all") {
      results = results.filter((p) => {
        const kw = (p.meta.keywords ?? []).join(" ");
        if (/workflow|development|requirement|testing|review/.test(kw))
          return category === "development";
        if (/content|ppt|presentation|document|writing/.test(kw))
          return category === "content";
        if (/research|analysis|deep/.test(kw)) return category === "research";
        if (/knowledge|wiki/.test(kw)) return category === "knowledge";
        if (/tooling|maintainer|ralph/.test(kw)) return category === "tooling";
        return category === "other";
      });
    }

    // Search
    if (query.trim()) {
      const q = query.toLowerCase();
      results = results.filter((p) => {
        if (p.meta.name.toLowerCase().includes(q)) return true;
        if (p.meta.description.toLowerCase().includes(q)) return true;
        if ((p.meta.keywords ?? []).some((k) => k.toLowerCase().includes(q)))
          return true;
        if (p.skills.some((s) => s.name.toLowerCase().includes(q))) return true;
        return false;
      });
    }

    return results;
  }, [plugins, query, category]);

  const timeline = useMemo(() => {
    return [...plugins]
      .filter((p) => p.updatedAt)
      .sort(
        (a, b) =>
          new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
      )
      .slice(0, 8);
  }, [plugins]);

  return (
    <div className="container-site">
      {/* Filter bar */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-4 mb-10">
        <SearchBar value={query} onChange={setQuery} />
        <div className="sm:ml-auto">
          <CategoryFilter
            categories={categories}
            selected={category}
            onSelect={setCategory}
          />
        </div>
      </div>

      {/* Results */}
      {filtered.length > 0 ? (
        <div className="grid gap-6" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))" }}>
          {filtered.map((p, i) => (
            <div
              key={p.slug}
              style={{
                animation: `stagger-item 0.5s var(--bp-ease-out-expo) ${i * 60}ms both`,
              }}
            >
              <PluginCard plugin={p} />
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-20">
          <div
            className="w-16 h-16 mx-auto mb-6 rounded-full flex items-center justify-center"
            style={{ background: "var(--bp-surface-2)" }}
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 16 16"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              style={{ color: "var(--bp-text-3)" }}
            >
              <circle cx="7" cy="7" r="4.5" />
              <path d="M10.5 10.5L14 14" />
            </svg>
          </div>
          <p className="text-sm" style={{ color: "var(--bp-text-2)" }}>
            No plugins match your search
          </p>
          <button
            onClick={() => { setQuery(""); setCategory("all"); }}
            className="mt-3 text-sm font-medium"
            style={{ color: "var(--bp-brand-500)" }}
          >
            Clear filters
          </button>
        </div>
      )}

      {/* Timeline */}
      {timeline.length > 0 && (
        <div className="mt-20">
          <h2
            className="text-lg font-semibold mb-6"
            style={{ color: "var(--bp-text-0)" }}
          >
            Recently Updated
          </h2>
          <div
            className="rounded-xl border divide-y overflow-hidden"
            style={{
              borderColor: "var(--bp-border-0)",
              borderBottomColor: "var(--bp-border-0)",
            }}
          >
            {timeline.map((p) => (
              <Link
                key={p.slug}
                href={`/plugins/${p.slug}`}
                className="flex items-center gap-4 px-5 py-3 transition-colors no-underline hover:bg-[var(--bp-surface-1)]"
                style={{ color: "inherit", borderColor: "var(--bp-border-0)" }}
              >
                <span
                  className="text-xs shrink-0 w-20"
                  style={{ color: "var(--bp-text-3)" }}
                >
                  {formatDate(p.updatedAt)}
                </span>
                <span
                  className="text-sm font-medium"
                  style={{ color: "var(--bp-text-0)" }}
                >
                  {p.meta.name}
                </span>
                <span
                  className="text-xs ml-auto"
                  style={{ color: "var(--bp-text-3)" }}
                >
                  v{p.meta.version}
                </span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

