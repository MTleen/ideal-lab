export interface PluginMeta {
  name: string;
  version: string;
  description: string;
  author: { name: string };
  skills: string;
  keywords: string[];
}

export interface SkillMeta {
  name: string;
  description: string;
  phase?: string;
  plugin: string;
  slug: string;
  content: string;
  references: string[];
  scripts: string[];
}

export interface PluginData {
  slug: string;
  meta: PluginMeta;
  skills: SkillMeta[];
  skillCount: number;
  updatedAt: string;
}

export interface CategoryInfo {
  slug: string;
  label: string;
  color: string;
}

export interface SearchEntry {
  type: "plugin" | "skill";
  pluginSlug: string;
  skillSlug?: string;
  name: string;
  description: string;
  keywords: string[];
  category?: string;
}

/* ── Skills Graph (knowledge graph data layer) ── */

export type Relation = "enhancement" | "prerequisite" | "embeds" | "produces_for" | "alternative";
export type Category = "development" | "content" | "research" | "knowledge" | "tooling" | "other";

export interface GraphNode {
  id: string;            // "plugin/skill-slug"
  name: string;
  plugin: string;
  category: Category;
  description: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  relation: Relation;
}

export interface SkillsGraph {
  metadata: {
    generated_at: string;
    total_skills: number;
    total_edges: number;
  };
  nodes: GraphNode[];
  edges: GraphEdge[];
}

/* ── Tasks (user-facing task panel) ── */

export type TaskScope = "lead" | "support" | "infra";

export interface Task {
  id: string;
  title: string;
  problem: string;
  outcome: string;
  scope: TaskScope;
  skillIds: string[];
  relatedPluginSlugs: string[];
  estimatedSteps: number;
}

/* ── Plugin Pain Points ── */

export interface PluginPainPoint {
  title: string;
  detail: string;
}

export type PluginPainPoints = Record<string, PluginPainPoint[]>;
