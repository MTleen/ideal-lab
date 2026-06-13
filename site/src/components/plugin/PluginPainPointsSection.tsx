import type { PluginData } from "@/lib/types";
import { getPluginPainPoints } from "@/lib/plugin-pain-points";

interface Props {
  plugin: PluginData;
}

export default function PluginPainPointsSection({ plugin }: Props) {
  const pp = getPluginPainPoints(plugin.slug);
  if (pp.length === 0) return null;
  return (
    <section className="container-site py-12">
      <h2
        className="text-xl font-bold mb-2"
        style={{ color: "var(--bp-text-0)" }}
      >
        解决什么问题
      </h2>
      <p className="text-sm mb-6" style={{ color: "var(--bp-text-2)" }}>
        以下痛点源自 {plugin.slug} 各 skill 的能力记录。
      </p>
      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}
      >
        {pp.map((p, i) => (
          <article
            key={i}
            className="rounded-xl border p-5"
            style={{
              background: "var(--bp-surface-1)",
              borderColor: "var(--bp-border-0)",
            }}
          >
            <h3
              className="text-base font-semibold mb-2"
              style={{ color: "var(--bp-text-0)" }}
            >
              {p.title}
            </h3>
            <p className="text-sm leading-relaxed" style={{ color: "var(--bp-text-2)" }}>
              {p.detail}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
