import type { SkillSummary } from "@/lib/skill-summary";

interface Props {
  summary: SkillSummary;
}

export default function SkillCapabilities({ summary }: Props) {
  if (summary.capabilities.length === 0) return null;
  return (
    <section
      className="rounded-xl border p-5 my-6"
      style={{
        background: "var(--bp-surface-1)",
        borderColor: "var(--bp-border-0)",
      }}
    >
      <h2 className="text-base font-semibold mb-3" style={{ color: "var(--bp-text-0)" }}>
        What it does
      </h2>
      <ul className="space-y-2">
        {summary.capabilities.map((cap, i) => (
          <li key={i} className="flex items-start gap-2 text-sm" style={{ color: "var(--bp-text-1)" }}>
            <span
              className="shrink-0 w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-semibold mt-0.5"
              style={{ background: "var(--bp-success)", color: "#fff" }}
            >
              ✓
            </span>
            <span>{cap}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
