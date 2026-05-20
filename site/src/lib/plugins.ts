import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type { PluginMeta, SkillMeta, PluginData } from "./types";
import { detectCategory } from "./utils";

/* ── Path resolution ── */

function pluginsRoot(): string {
  return path.resolve(process.cwd(), "..", "plugins");
}

/* ── Load all plugins ── */

export function getAllPlugins(): PluginData[] {
  const root = pluginsRoot();
  if (!fs.existsSync(root)) return [];

  const dirs = fs
    .readdirSync(root, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  return dirs.map((slug) => loadPlugin(slug)).filter(Boolean) as PluginData[];
}

/* ── Load single plugin ── */

export function loadPlugin(slug: string): PluginData | null {
  const root = pluginsRoot();
  const pluginDir = path.join(root, slug);
  const pluginJsonPath = path.join(pluginDir, ".claude-plugin", "plugin.json");

  if (!fs.existsSync(pluginJsonPath)) return null;

  const raw = fs.readFileSync(pluginJsonPath, "utf-8");
  const meta: PluginMeta = JSON.parse(raw);
  const skills = loadSkills(slug, pluginDir);

  let updatedAt = "";
  try {
    const changelogPath = path.join(pluginDir, "CHANGELOG.md");
    if (fs.existsSync(changelogPath)) {
      const { mtime } = fs.statSync(changelogPath);
      updatedAt = mtime.toISOString();
    }
  } catch { /* ignore */ }
  if (!updatedAt) {
    try {
      const { mtime } = fs.statSync(pluginJsonPath);
      updatedAt = mtime.toISOString();
    } catch { updatedAt = ""; }
  }

  return {
    slug,
    meta,
    skills,
    skillCount: skills.length,
    updatedAt,
  };
}

/* ── Load skills for a plugin ── */

function loadSkills(pluginSlug: string, pluginDir: string): SkillMeta[] {
  const skillsDir = path.join(pluginDir, "skills");
  if (!fs.existsSync(skillsDir)) return [];

  const skillDirs = fs
    .readdirSync(skillsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  return skillDirs
    .map((skillSlug) => loadSkill(pluginSlug, skillSlug, skillsDir))
    .filter(Boolean) as SkillMeta[];
}

/* ── Load single skill ── */

function loadSkill(
  pluginSlug: string,
  skillSlug: string,
  skillsDir: string,
): SkillMeta | null {
  const skillMdPath = path.join(skillsDir, skillSlug, "SKILL.md");
  if (!fs.existsSync(skillMdPath)) return null;

  const raw = fs.readFileSync(skillMdPath, "utf-8");
  const { data, content } = matter(raw);

  const skillDir = path.join(skillsDir, skillSlug);
  const references: string[] = [];
  const scripts: string[] = [];

  const refsDir = path.join(skillDir, "references");
  if (fs.existsSync(refsDir)) walkDir(refsDir, refsDir, references);
  const scriptsDir = path.join(skillDir, "scripts");
  if (fs.existsSync(scriptsDir)) walkDir(scriptsDir, scriptsDir, scripts);

  return {
    name: data.name ?? skillSlug,
    description: data.description ?? "",
    phase: extractPhase(content),
    plugin: pluginSlug,
    slug: skillSlug,
    content,
    references,
    scripts,
  };
}

function walkDir(dir: string, baseDir: string, list: string[]) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walkDir(full, baseDir, list);
    else list.push(path.relative(baseDir, full));
  }
}

function extractPhase(content: string): string {
  const m = content.match(/[Pp]hase[:\s]+([Pp]?\d+)/);
  return m ? m[1] : "";
}

/* ── Search index (built at compile time, used client-side) ── */

import type { SearchEntry } from "./types";

export function buildSearchIndex(plugins: PluginData[]): SearchEntry[] {
  const entries: SearchEntry[] = [];
  for (const p of plugins) {
    entries.push({
      type: "plugin",
      pluginSlug: p.slug,
      name: p.meta.name,
      description: p.meta.description,
      keywords: p.meta.keywords ?? [],
      category: detectCategory(p),
    });
    for (const s of p.skills) {
      entries.push({
        type: "skill",
        pluginSlug: p.slug,
        skillSlug: s.slug,
        name: s.name,
        description: s.description,
        keywords: [],
      });
    }
  }
  return entries;
}
