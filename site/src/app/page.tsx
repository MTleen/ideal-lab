import { getAllPlugins } from "@/lib/plugins";
import { getAllCategories } from "@/lib/utils";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import HomeClient from "./HomeClient";

export default function HomePage() {
  const plugins = getAllPlugins();
  const categories = getAllCategories();

  return (
    <>
      <Nav />
      <main className="flex-1">
        {/* Hero */}
        <section className="relative overflow-hidden pt-24 pb-20 sm:pt-32 sm:pb-28">
          {/* Decorative radial gradients */}
          <div
            className="absolute top-0 right-0 w-[600px] h-[600px] pointer-events-none opacity-20"
            style={{
              background:
                "radial-gradient(circle at 70% 30%, var(--bp-brand-400), transparent 70%)",
            }}
          />
          <div
            className="absolute bottom-0 left-0 w-[400px] h-[400px] pointer-events-none opacity-15"
            style={{
              background:
                "radial-gradient(circle at 30% 70%, var(--bp-brand-300), transparent 70%)",
            }}
          />

          <div className="container-site relative">
            <div
              className="inline-block text-[11px] font-medium tracking-widest uppercase mb-6 px-3 py-1 rounded-full"
              style={{
                background: "var(--bp-surface-2)",
                color: "var(--bp-brand-500)",
              }}
            >
              Best Practices
            </div>
            <h1
              className="max-w-3xl font-black leading-[1.08] tracking-[-0.03em] mb-6"
              style={{
                fontSize: "clamp(42px, 8vw, 88px)",
                color: "var(--bp-text-0)",
              }}
            >
              将 Claude Code 工程方法论
              <br />
              <span style={{ color: "var(--bp-brand-500)" }}>
                沉淀为可分发的最佳实践
              </span>
            </h1>
            <p
              className="max-w-xl text-lg sm:text-xl leading-relaxed mb-8"
              style={{ color: "var(--bp-text-1)" }}
            >
              从需求分析到代码交付的完整开发链路，每一个 Plugin
              都是经过实战验证的 AI 工程方法论。
              浏览、安装、复用——把可靠的工作流带给你的团队。
            </p>
            <div className="flex items-center gap-4">
              <a
                href="#browse"
                className="inline-flex items-center h-12 px-6 rounded-xl text-sm font-semibold transition-all hover:brightness-110"
                style={{
                  background: "var(--bp-brand-500)",
                  color: "#fff",
                  boxShadow: "var(--bp-shadow-brand)",
                }}
              >
                Browse Plugins
              </a>
              <a
                href="https://github.com/MTleen/ideal-lab"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center h-12 px-6 rounded-xl text-sm font-semibold transition-colors border"
                style={{
                  borderColor: "var(--bp-border-0)",
                  color: "var(--bp-text-1)",
                  background: "var(--bp-surface-1)",
                }}
              >
                View on GitHub
              </a>
            </div>
          </div>
        </section>

        {/* Browse section */}
        <section id="browse" className="pb-24">
          <HomeClient
            plugins={JSON.parse(JSON.stringify(plugins))}
            categories={categories}
          />
        </section>
      </main>
      <Footer />
    </>
  );
}
