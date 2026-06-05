import { getAllPlugins, loadPlugin } from "@/lib/plugins";
import type { SkillMeta } from "@/lib/types";
import { notFound } from "next/navigation";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import Link from "next/link";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkHtml from "remark-html";
import { parseSkillSummary } from "@/lib/skill-summary";
import SkillCapabilities from "@/components/skill/SkillCapabilities";
import SkillRelated from "@/components/skill/SkillRelated";
import SkillToc from "@/components/skill/SkillToc";

export function generateStaticParams() {
  const plugins = getAllPlugins();
  const params: { plugin: string; skill: string }[] = [];
  for (const p of plugins) {
    if (!p.skills) continue;
    for (const s of p.skills) {
      params.push({ plugin: p.slug, skill: s.slug });
    }
  }
  return params;
}

export default async function SkillPage({
  params,
}: {
  params: Promise<{ plugin: string; skill: string }>;
}) {
  const { plugin: pluginSlug, skill: skillSlug } = await params;
  const plugin = loadPlugin(pluginSlug);
  if (!plugin) notFound();

  const skill = plugin.skills.find((s: SkillMeta) => s.slug === skillSlug);
  if (!skill) notFound();

  const rendered = await unified().use(remarkParse).use(remarkHtml).process(skill.content);
  const html = rendered.toString();
  const summary = parseSkillSummary(skill.content);
  const skillId = `${plugin.slug}/${skill.slug}`;

  return (
    <>
      <Nav />
      <main className="flex-1 pt-14">
        <div className="container-site py-4">
          <Link
            href={`/plugins/${pluginSlug}/`}
            className="inline-flex items-center gap-1.5 text-sm font-medium transition-colors no-underline"
            style={{ color: "var(--bp-text-2)" }}
          >
            <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M10 3L5 8l5 5" />
            </svg>
            {plugin.meta.name}
          </Link>
        </div>

        {/* Header */}
        <section className="container-site pb-6">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            {skill.phase && (
              <span
                className="text-[10px] font-semibold tracking-widest uppercase px-2.5 py-1 rounded-full"
                style={{
                  background: "var(--bp-brand-500)",
                  color: "#fff",
                }}
              >
                Phase {skill.phase}
              </span>
            )}
            <span
              className="text-[10px] font-medium tracking-widest uppercase px-2.5 py-1 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-text-2)",
              }}
            >
              {plugin.meta.name}
            </span>
          </div>
          <h1
            className="font-bold leading-tight tracking-tight mb-3"
            style={{
              fontSize: "clamp(28px, 4vw, 48px)",
              color: "var(--bp-text-0)",
              maxWidth: 720,
            }}
          >
            {skill.name}
          </h1>
          <p
            className="max-w-2xl leading-relaxed"
            style={{ fontSize: 16, color: "var(--bp-text-1)" }}
          >
            {skill.description}
          </p>
        </section>

        {/* Capabilities (auto-extracted; empty → hidden) */}
        <section className="container-site">
          <SkillCapabilities summary={summary} />
        </section>

        {/* Related skills (with Mini Graph toggle) */}
        <section className="container-site">
          <SkillRelated skillId={skillId} />
        </section>

        {/* Body: TOC + markdown */}
        <section className="container-site py-6">
          <div className="flex gap-8">
            <article
              id="skill-prose"
              className="prose max-w-none flex-1 min-w-0"
              dangerouslySetInnerHTML={{ __html: html }}
            />
            <div className="hidden lg:block shrink-0">
              <SkillToc scopeSelector="#skill-prose" />
            </div>
          </div>
        </section>

        {/* References + Scripts */}
        {(skill.references.length > 0 || skill.scripts.length > 0) && (
          <section className="container-site py-8">
            <h3
              className="text-xs font-semibold tracking-widest uppercase mb-3"
              style={{ color: "var(--bp-text-2)" }}
            >
              References &amp; scripts
            </h3>
            <div className="grid gap-3 sm:grid-cols-2">
              {skill.references.map((r, i) => (
                <div
                  key={i}
                  className="rounded-lg border px-3 py-2 text-[12px] font-mono"
                  style={{
                    background: "var(--bp-surface-1)",
                    borderColor: "var(--bp-border-0)",
                    color: "var(--bp-text-2)",
                  }}
                >
                  {r}
                </div>
              ))}
              {skill.scripts.map((s, i) => (
                <div
                  key={i}
                  className="rounded-lg border px-3 py-2 text-[12px] font-mono"
                  style={{
                    background: "var(--bp-surface-1)",
                    borderColor: "var(--bp-border-0)",
                    color: "var(--bp-text-2)",
                  }}
                >
                  {s}
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
      <Footer />
    </>
  );
}
