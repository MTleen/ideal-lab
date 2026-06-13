import { getAllPlugins } from "@/lib/plugins";
import { getAllCategories, detectCategory } from "@/lib/utils";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import HomeClient from "./HomeClient";

export default function HomePage() {
  const plugins = getAllPlugins();
  /* Pass only the lightweight fields the homepage needs — not the full
   * SKILL.md content, which would bloat the client bundle. */
  const pluginSummaries = plugins.map((p) => ({
    slug: p.slug,
    name: p.meta.name,
    description: p.meta.description,
    skillCount: p.skillCount,
    category: detectCategory(p),
  }));
  const categories = getAllCategories();

  return (
    <>
      <Nav />
      <main className="flex-1 pt-14">
        <HomeClient categories={categories} plugins={pluginSummaries} />
      </main>
      <Footer />
    </>
  );
}
