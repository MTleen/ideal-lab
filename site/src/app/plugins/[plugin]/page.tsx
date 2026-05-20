import { getAllPlugins, loadPlugin } from "@/lib/plugins";
import type { PluginData } from "@/lib/types";
import { getCategory, detectCategory } from "@/lib/utils";
import { notFound } from "next/navigation";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import CodeBlock from "@/components/CodeBlock";
import Link from "next/link";

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

  const cat = getCategory(detectCategory(plugin));
  const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const installCmd = [
    `claude plugin marketplace add https://github.com/MTleen/ideal-lab`,
    `claude plugin install ${plugin.meta.name}@ideal-lab`,
  ].join("\n");

  return (
    <>
      <Nav />
      <main className="flex-1 pt-20">
        {/* Back link */}
        <div className="container-site mb-8">
          <Link
            href={`${base}/`}
            className="inline-flex items-center gap-2 text-sm font-medium transition-colors no-underline"
            style={{ color: "var(--bp-text-2)" }}
          >
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M10 3L5 8l5 5" />
            </svg>
            All Plugins
          </Link>
        </div>

        {/* Hero */}
        <section className="container-site pb-16">
          <div className="flex flex-wrap items-start gap-4 mb-3">
            <span
              className="text-[11px] font-medium tracking-widest uppercase px-3 py-1 rounded-full"
              style={{ background: cat.color + "15", color: cat.color }}
            >
              {cat.label}
            </span>
            <span
              className="text-[11px] font-medium px-3 py-1 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-text-2)",
              }}
            >
              v{plugin.meta.version}
            </span>
          </div>

          <h1
            className="max-w-2xl font-bold leading-tight tracking-tight mb-4"
            style={{
              fontSize: "clamp(32px, 5vw, 56px)",
              color: "var(--bp-text-0)",
            }}
          >
            {plugin.meta.name}
          </h1>
          <p
            className="max-w-xl text-lg leading-relaxed mb-8"
            style={{ color: "var(--bp-text-1)" }}
          >
            {plugin.meta.description}
          </p>

          <div className="flex flex-wrap items-center gap-4 mb-10">
            <CodeBlock code={installCmd} />
          </div>

          {/* Meta bar */}
          <div className="flex flex-wrap items-center gap-2 text-xs" style={{ color: "var(--bp-text-3)" }}>
            {plugin.meta.keywords?.map((kw: string) => (
              <span
                key={kw}
                className="px-2 py-0.5 rounded-full"
                style={{
                  background: "var(--bp-surface-2)",
                  color: "var(--bp-text-2)",
                  border: "1px solid var(--bp-border-0)",
                }}
              >
                {kw}
              </span>
            ))}
          </div>
        </section>

        {/* Skills */}
        <section className="container-site pb-16">
          <h2
            className="text-xl sm:text-2xl font-bold mb-6"
            style={{ color: "var(--bp-text-0)" }}
          >
            Skills ({plugin.skillCount})
          </h2>
          <div className="grid gap-4">
            {plugin.skills.map((s) => (
              <Link
                key={s.slug}
                href={`${base}/plugins/${plugin.slug}/skills/${s.slug}`}
                className="group block rounded-xl border p-5 transition-all no-underline hover:shadow-md"
                style={{
                  background: "var(--bp-surface-1)",
                  borderColor: "var(--bp-border-0)",
                }}
              >
                <div className="flex items-start justify-between gap-4 mb-2">
                  <h3
                    className="text-base font-semibold"
                    style={{ color: "var(--bp-text-0)" }}
                  >
                    <span style={{ color: "var(--bp-brand-500)" }}>
                      {s.name}
                    </span>
                  </h3>
                  {s.phase && (
                    <span
                      className="text-[11px] font-medium px-2.5 py-0.5 rounded-full shrink-0"
                      style={{
                        background: "var(--bp-surface-2)",
                        color: "var(--bp-text-2)",
                      }}
                    >
                      Phase {s.phase}
                    </span>
                  )}
                </div>
                <p
                  className="text-sm leading-relaxed"
                  style={{ color: "var(--bp-text-2)" }}
                >
                  {s.description}
                </p>
                {(s.references.length > 0 || s.scripts.length > 0) && (
                  <div className="flex items-center gap-3 mt-3 text-[11px]" style={{ color: "var(--bp-text-3)" }}>
                    {s.references.length > 0 && (
                      <span>
                        {s.references.length} reference
                        {s.references.length > 1 ? "s" : ""}
                      </span>
                    )}
                    {s.scripts.length > 0 && (
                      <span>
                        {s.scripts.length} script
                        {s.scripts.length > 1 ? "s" : ""}
                      </span>
                    )}
                  </div>
                )}
              </Link>
            ))}
          </div>
        </section>

        {/* GitHub link */}
        <section className="container-site pb-24">
          <a
            href="https://github.com/MTleen/ideal-lab"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm font-medium transition-colors no-underline"
            style={{ color: "var(--bp-text-2)" }}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
            </svg>
            View on GitHub
          </a>
        </section>
      </main>
      <Footer />
    </>
  );
}

