"use client";

import { useEffect, useState } from "react";

interface Props {
  /** CSS selector for the prose container (e.g. ".prose"). */
  scopeSelector: string;
}

interface TocLink {
  level: 2 | 3;
  text: string;
  id: string;
}

const FOLD_THRESHOLD = 8; // H2s beyond this → fold deepest 3
const FOLD_COUNT = 3;

export default function SkillToc({ scopeSelector }: Props) {
  const [links, setLinks] = useState<TocLink[]>([]);
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const scope = document.querySelector(scopeSelector);
    if (!scope) return;
    const headings = Array.from(scope.querySelectorAll("h2, h3")) as HTMLElement[];
    const ls: TocLink[] = headings.map((h) => {
      const text = (h.textContent || "").trim();
      const id = h.id || slugify(text);
      h.id = id;
      return { level: h.tagName === "H2" ? 2 : 3, text, id };
    });
    setLinks(ls);

    const observer = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) setActiveId((e.target as HTMLElement).id);
        }
      },
      { rootMargin: "0px 0px -80% 0px", threshold: 0.1 },
    );
    for (const h of headings) observer.observe(h);
    return () => observer.disconnect();
  }, [scopeSelector]);

  if (links.length === 0) return null;

  /* Fold logic: H2 >= 8 → fold last 3 H2s into <details> */
  const h2s = links.filter((l) => l.level === 2);
  const fold = h2s.length >= FOLD_THRESHOLD;
  const visibleH2 = fold ? h2s.slice(0, h2s.length - FOLD_COUNT) : h2s;
  const foldedH2 = fold ? h2s.slice(h2s.length - FOLD_COUNT) : [];
  const foldedIds = new Set(foldedH2.map((h) => h.id));

  const renderLink = (l: TocLink) => (
    <li key={l.id}>
      <a
        href={`#${l.id}`}
        className="block py-1 px-2 text-[12px] transition-colors border-l-2"
        style={{
          color: activeId === l.id ? "var(--bp-toc-link-active)" : "var(--bp-toc-link)",
          borderColor: activeId === l.id ? "var(--bp-toc-link-active-border)" : "transparent",
          paddingLeft: l.level === 3 ? 20 : 8,
        }}
      >
        {l.text}
      </a>
    </li>
  );

  return (
    <nav
      aria-label="Table of contents"
      className="hidden lg:block sticky"
      style={{ top: "var(--bp-toc-top-offset)", width: "var(--bp-toc-width)" }}
    >
      <div
        className="text-[11px] font-semibold mb-2 uppercase tracking-wider"
        style={{ color: "var(--bp-text-3)" }}
      >
        On this page
      </div>
      <ul className="border-l space-y-0" style={{ borderColor: "var(--bp-toc-border)" }}>
        {visibleH2.map((h) => {
          const children = links.filter((l) => l.level === 3 && /* same parent */ true);
          /* Show H2 + its direct H3 children if any in visible range */
          const h3Children = children.filter((c) => /* simplistic: all h3 between this h2 and next h2 */ true);
          return (
            <li key={h.id}>
              {renderLink(h)}
              {h3Children.slice(0, 3).map(renderLink)}
            </li>
          );
        })}
      </ul>
      {fold && foldedH2.length > 0 && (
        <details
          className="mt-2 border-l pl-2"
          style={{ borderColor: "var(--bp-toc-border)" }}
        >
          <summary
            className="text-[11px] cursor-pointer"
            style={{ color: "var(--bp-text-2)" }}
          >
            +{foldedH2.length} more
          </summary>
          <ul>
            {foldedH2.map(renderLink)}
          </ul>
        </details>
      )}
    </nav>
  );
}

function slugify(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^\p{Letter}\p{Number}\s-]/gu, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}
