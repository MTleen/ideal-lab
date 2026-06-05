import { getAllPlugins } from "@/lib/plugins";
import { graphNodes, graphEdges } from "@/lib/graph";
import { getAllTasks } from "@/lib/tasks";
import { getAllCategories } from "@/lib/utils";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import HomeClient from "./HomeClient";

export default function HomePage() {
  const plugins = getAllPlugins();
  const pluginSlugs = plugins.map((p) => p.slug);
  const categories = getAllCategories();
  const taskCount = getAllTasks().length;

  return (
    <>
      <Nav />
      <main className="flex-1 pt-14">
        <HomeClient
          categories={categories}
          pluginSlugs={pluginSlugs}
        />
      </main>
      <Footer />
    </>
  );
}
