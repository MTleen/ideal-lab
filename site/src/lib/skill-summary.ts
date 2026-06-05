/* Extract H2/H3 structure + first sentence under each H2 from a SKILL.md body.
 * Used by SkillToc to build TOC from already-rendered DOM (no markdown re-parse).
 * Returns plain data that the DOM-walking SkillToc can also re-derive.
 */

import { remark } from "remark";
import remarkParse from "remark-parse";
import type { Root, Heading, Paragraph, Text } from "mdast";

export interface TocEntry {
  level: 2 | 3;
  text: string;
  slug: string;
  /** First sentence of body content under this heading. */
  firstSentence?: string;
}

export interface SkillSummary {
  /** Verbs / "what it does" — derived from H2 titles + first sentence. */
  capabilities: string[];
  /** TOC entries. */
  toc: TocEntry[];
}

function slugify(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^\p{Letter}\p{Number}\s-]/gu, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function firstSentenceOf(node: Paragraph | undefined): string | undefined {
  if (!node) return undefined;
  const texts: string[] = [];
  const walk = (n: any) => {
    if (n.type === "text") texts.push((n as Text).value);
    if (n.children) for (const c of n.children) walk(c);
  };
  walk(node);
  const text = texts.join(" ").trim();
  if (!text) return undefined;
  const m = text.match(/^[^。.!?！？\n]+[。.!?！？]/);
  return (m ? m[0] : text.split("\n")[0]).trim();
}

export function parseSkillSummary(content: string): SkillSummary {
  const tree = remark().use(remarkParse).parse(content) as Root;
  const toc: TocEntry[] = [];
  const capabilities: string[] = [];

  let i = 0;
  while (i < tree.children.length) {
    const node = tree.children[i];
    if (node.type === "heading" && (node.depth === 2 || node.depth === 3)) {
      const heading = node as Heading;
      const text = heading.children
        .map((c: any) => (c.type === "text" ? c.value : ""))
        .join("")
        .trim();
      if (text) {
        const next = tree.children[i + 1];
        const sentence = firstSentenceOf(
          next && next.type === "paragraph" ? (next as Paragraph) : undefined,
        );
        toc.push({ level: heading.depth as 2 | 3, text, slug: slugify(text), firstSentence: sentence });
        if (heading.depth === 2 && sentence) {
          capabilities.push(sentence);
        }
      }
    }
    i++;
  }

  return { capabilities: capabilities.slice(0, 5), toc };
}
