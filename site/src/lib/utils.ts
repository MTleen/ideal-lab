import type { CategoryInfo, PluginData } from "./types";

const CATEGORIES: Record<string, CategoryInfo> = {
  development: { slug: "development", label: "开发", color: "#7b5cea" },
  content: { slug: "content", label: "内容", color: "#0ea5a0" },
  research: { slug: "research", label: "研究", color: "#d98b0a" },
  knowledge: { slug: "knowledge", label: "知识", color: "#8ba60a" },
  tooling: { slug: "tooling", label: "工具", color: "#9b6cea" },
};

const CATEGORY_FALLBACK: CategoryInfo = {
  slug: "other",
  label: "其他",
  color: "#6e6e82",
};

export function getAllCategories(): CategoryInfo[] {
  return Object.values(CATEGORIES);
}

export function getCategory(slug: string): CategoryInfo {
  return CATEGORIES[slug] ?? CATEGORY_FALLBACK;
}

export function detectCategory(p: PluginData): string {
  const kw = (p.meta.keywords ?? []).join(" ");
  if (/workflow|development|requirement|testing|review/.test(kw))
    return "development";
  if (/content|ppt|presentation|document|writing/.test(kw)) return "content";
  if (/research|analysis|deep/.test(kw)) return "research";
  if (/knowledge|wiki/.test(kw)) return "knowledge";
  if (/tooling|maintainer|ralph/.test(kw)) return "tooling";
  return "other";
}

export function formatDate(iso: string): string {
  if (!iso) return "";
  const d = new Date(iso);
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  if (days === 0) return "今天";
  if (days === 1) return "昨天";
  if (days < 7) return `${days} 天前`;
  if (days < 30) return `${Math.floor(days / 7)} 周前`;
  return d.toLocaleDateString("zh-CN");
}
