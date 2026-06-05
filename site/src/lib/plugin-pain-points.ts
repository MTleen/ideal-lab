import painPointsData from "../data/plugin-pain-points.json";
import { getAllPlugins } from "./plugins";
import type { PluginPainPoints, PluginPainPoint } from "./types";

const data = painPointsData as PluginPainPoints;

/* ── Build-time validation ── */

const knownPluginSlugs = new Set(getAllPlugins().map((p) => p.slug));
for (const slug of Object.keys(data)) {
  if (!knownPluginSlugs.has(slug)) {
    throw new Error(`plugin-pain-points.json: unknown plugin "${slug}"`);
  }
  for (const pp of data[slug]) {
    if (!pp.title) {
      throw new Error(`plugin-pain-points.json["${slug}"]: entry missing title`);
    }
  }
}

/* ── Public API ── */

export function getAllPluginPainPoints(): PluginPainPoints {
  return data;
}

export function getPluginPainPoints(slug: string): PluginPainPoint[] {
  return data[slug] ?? [];
}
