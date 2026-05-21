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
