import { getAllPlugins, loadPlugin } from "@/lib/plugins";
import { getTasksByPlugin } from "@/lib/tasks";
import { graphEdges } from "@/lib/graph";
import { notFound } from "next/navigation";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import CodeBlock from "@/components/CodeBlock";
import Link from "next/link";
import PluginPainPointsSection from "@/components/plugin/PluginPainPointsSection";
import { CaretBackLink, CtaArrowLink } from "@/components/PluginPageLinks";

export function generateStaticParams() {
  const plugins = getAllPlugins();
  return plugins.map((p) => ({ plugin: p.slug }));
}

export default async function PluginPage({
  params,
}: {
  params: Promise<{ plugin: string }>;
}) {
  const { plugin: slug } = await params;
  const plugin = loadPlugin(slug);
  if (!plugin) notFound();

  const installCmd = [
    `claude plugin marketplace add https://github.com/MTleen/ideal-lab`,
    `claude plugin install ${plugin.meta.name}@ideal-lab`,
  ].join("\n");

  const tasks = getTasksByPlugin(slug);

  /* Metrics: skills, phases, relations involving this plugin */
  const phaseSet = new Set<string>();
  let relationsIn = 0;
  let relationsOut = 0;
  for (const skill of plugin.skills) {
    if (skill.phase) phaseSet.add(skill.phase);
    for (const e of graphEdges) {
      if (e.target === `${plugin.slug}/${skill.slug}`) relationsIn++;
      if (e.source === `${plugin.slug}/${skill.slug}`) relationsOut++;
    }
  }
  /* Check orchestrator (plugin-level, hardcoded — orchestrators are workflow meta-skills) */
  const ORCHESTRATOR_PLUGINS = new Set([
    "ideal-dev-workflow",
    "ideal-ppt-suite",
    "ideal-document-workflow",
    "ideal-knowledge-base",
    "ideal-graph-orchestrator",
  ]);
  const hasOrchestrator = ORCHESTRATOR_PLUGINS.has(slug);
  const totalRelations = relationsIn + relationsOut;

  return (
    <>
      <Nav />
      <main className="flex-1 pt-14">
        <div className="container-site py-6">
          <CaretBackLink href="/" label="All plugins" />
        </div>

        {/* Hero */}
        <section className="container-site pb-8">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <span
              className="text-[10px] font-medium tracking-widest uppercase px-2.5 py-1 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-brand-500)",
              }}
            >
              {plugin.meta.keywords?.[0] ?? "plugin"}
            </span>
            <span
              className="text-[10px] font-medium px-2.5 py-1 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-text-2)",
              }}
            >
              v{plugin.meta.version}
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
            {plugin.meta.name}
          </h1>
          <p
            className="max-w-2xl leading-relaxed mb-6"
            style={{ fontSize: 17, color: "var(--bp-text-1)" }}
          >
            {plugin.meta.description}
          </p>

          {/* Metrics */}
          <div
            className="grid gap-3 mb-6"
            style={{ gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))" }}
          >
            <Metric label="skills" value={plugin.skillCount} />
            <Metric label="phases" value={phaseSet.size} />
            <Metric label="relations" value={totalRelations} />
            <Metric label="orchestrator" value={hasOrchestrator ? "yes" : "no"} />
          </div>

          {/* Install */}
          <div className="mb-4">
            <CodeBlock code={installCmd} />
          </div>
        </section>

        {/* Pain points */}
        <PluginPainPointsSection plugin={plugin} />

        {/* Tasks using this plugin */}
        {tasks.length > 0 && (
          <section className="container-site py-12">
            <h2 className="text-xl font-bold mb-2" style={{ color: "var(--bp-text-0)" }}>
              Tasks using this plugin
            </h2>
            <p className="text-sm mb-4" style={{ color: "var(--bp-text-2)" }}>
              Highlighted on the homepage knowledge graph when selected.
            </p>
            <div className="grid gap-3" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}>
              {tasks.map((t) => (
                <Link
                  key={t.id}
                  href={`/?task=${t.id}`}
                  className="block rounded-lg border px-4 py-3 transition-all no-underline"
                  style={{
                    background: "var(--bp-surface-1)",
                    borderColor: "var(--bp-border-0)",
                    color: "inherit",
                  }}
                >
                  <h3 className="text-sm font-semibold mb-1" style={{ color: "var(--bp-text-0)" }}>
                    {t.title}
                  </h3>
                  <p className="text-xs" style={{ color: "var(--bp-text-2)" }}>
                    {t.skillIds.length} skills · {t.estimatedSteps} steps
                  </p>
                </Link>
              ))}
            </div>
          </section>
        )}

        {/* Skills list */}
        <section className="container-site py-12">
          <h2 className="text-xl font-bold mb-2" style={{ color: "var(--bp-text-0)" }}>
            Skills ({plugin.skillCount})
          </h2>
          <p className="text-sm mb-4" style={{ color: "var(--bp-text-2)" }}>
            Click any skill to see what it does, who uses it, and the full SKILL.md.
          </p>
          <div className="grid gap-2">
            {plugin.skills.map((s) => (
              <Link
                key={s.slug}
                href={`/plugins/${plugin.slug}/skills/${s.slug}/`}
                className="flex items-center gap-3 rounded-lg border px-4 py-3 transition-colors no-underline"
                style={{
                  background: "var(--bp-surface-1)",
                  borderColor: "var(--bp-border-0)",
                  color: "inherit",
                }}
              >
                {s.phase && (
                  <span
                    className="text-[10px] font-semibold w-10 shrink-0"
                    style={{ color: "var(--bp-brand-500)" }}
                  >
                    P{s.phase}
                  </span>
                )}
                <span
                  className="text-sm font-medium flex-1"
                  style={{ color: "var(--bp-text-0)" }}
                >
                  {s.name}
                </span>
                <span className="text-[11px] truncate max-w-md" style={{ color: "var(--bp-text-2)" }}>
                  {s.description}
                </span>
              </Link>
            ))}
          </div>
        </section>

        {/* CTA: view in graph */}
        <section className="container-site py-12 text-center">
          <CtaArrowLink
            href={`/?focus=${plugin.slug}`}
            label="Open in knowledge graph"
          />
        </section>
      </main>
      <Footer />
    </>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div
      className="rounded-lg border px-3 py-2"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
      }}
    >
      <div className="text-lg font-bold" style={{ color: "var(--bp-text-0)" }}>
        {value}
      </div>
      <div className="text-[11px] font-medium" style={{ color: "var(--bp-text-3)" }}>
        {label}
      </div>
    </div>
  );
}
