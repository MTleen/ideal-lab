import { getAllPlugins, loadPlugin } from "@/lib/plugins";
import type { SkillMeta } from "@/lib/types";
import { notFound } from "next/navigation";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import Link from "next/link";
import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkHtml from "remark-html";

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

  // Render markdown
  const rendered = await unified().use(remarkParse).use(remarkHtml).process(skill.content);
  const html = rendered.toString();

  return (
    <>
      <Nav />
      <main className="flex-1 pt-20">
        {/* Breadcrumb */}
        <div className="container-site mb-8">
          <div className="flex items-center gap-2 text-sm" style={{ color: "var(--bp-text-2)" }}>
            <Link
              href={`/`}
              className="transition-colors hover:text-[var(--bp-text-0)] no-underline"
              style={{ color: "inherit" }}
            >
              Home
            </Link>
            <span style={{ color: "var(--bp-text-3)" }}>/</span>
            <Link
              href={`/plugins/${pluginSlug}`}
              className="transition-colors hover:text-[var(--bp-text-0)] no-underline"
              style={{ color: "inherit" }}
            >
              {plugin.meta.name}
            </Link>
            <span style={{ color: "var(--bp-text-3)" }}>/</span>
            <span style={{ color: "var(--bp-text-0)" }}>{skill.name}</span>
          </div>
        </div>

        {/* Header */}
        <section className="container-site pb-10">
          <div className="flex flex-wrap items-start gap-3 mb-4">
            {skill.phase && (
              <span
                className="text-[11px] font-medium px-3 py-1 rounded-full"
                style={{
                  background: "var(--bp-brand-500)",
                  color: "#fff",
                }}
              >
                Phase {skill.phase}
              </span>
            )}
            <span
              className="text-[11px] font-medium px-3 py-1 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-text-2)",
              }}
            >
              {plugin.meta.name}
            </span>
          </div>
          <h1
            className="max-w-2xl font-bold leading-tight tracking-tight mb-4"
            style={{
              fontSize: "clamp(28px, 4vw, 48px)",
              color: "var(--bp-text-0)",
            }}
          >
            {skill.name}
          </h1>
          <p
            className="text-lg leading-relaxed max-w-xl"
            style={{ color: "var(--bp-text-1)" }}
          >
            {skill.description}
          </p>
        </section>

        {/* Content + Sidebar */}
        <section className="container-site pb-24">
          <div className="flex gap-12">
            {/* Main content */}
            <div className="flex-1 min-w-0">
              <article
                className="prose max-w-none"
                dangerouslySetInnerHTML={{ __html: html }}
              />
            </div>

            {/* Sidebar */}
            {(skill.references.length > 0 || skill.scripts.length > 0) && (
              <aside className="hidden lg:block w-56 shrink-0">
                <div className="sticky top-24">
                  {skill.references.length > 0 && (
                    <div className="mb-8">
                      <h4
                        className="text-xs font-semibold tracking-widest uppercase mb-3"
                        style={{ color: "var(--bp-text-2)" }}
                      >
                        References
                      </h4>
                      <ul className="space-y-1.5">
                        {skill.references.map((r, i) => (
                          <li
                            key={i}
                            className="text-[13px] leading-relaxed"
                            style={{ color: "var(--bp-text-2)" }}
                          >
                            <span
                              className="font-mono text-[11px] px-1.5 py-0.5 rounded mr-2"
                              style={{
                                background: "var(--bp-surface-2)",
                                color: "var(--bp-text-3)",
                              }}
                            >
                              {r.split(".").pop()}
                            </span>
                            {r}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {skill.scripts.length > 0 && (
                    <div>
                      <h4
                        className="text-xs font-semibold tracking-widest uppercase mb-3"
                        style={{ color: "var(--bp-text-2)" }}
                      >
                        Scripts
                      </h4>
                      <ul className="space-y-1.5">
                        {skill.scripts.map((s, i) => (
                          <li
                            key={i}
                            className="text-[13px] leading-relaxed font-mono"
                            style={{ color: "var(--bp-text-2)" }}
                          >
                            {s}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </aside>
            )}
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
