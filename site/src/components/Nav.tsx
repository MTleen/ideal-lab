"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Sun, Moon, GithubLogo } from "@phosphor-icons/react";

export default function Nav() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    setDark(document.documentElement.classList.contains("dark"));
  }, []);

  function toggleTheme() {
    const next = !dark;
    setDark(next);
    document.documentElement.classList.toggle("dark", next);
    localStorage.setItem("theme", next ? "dark" : "light");
  }

  return (
    <nav
      className="fixed top-0 inset-x-0 h-14 flex items-center backdrop-blur-md border-b"
      style={{
        background: "var(--bp-nav-bg)",
        borderColor: "var(--bp-border-0)",
        zIndex: "var(--bp-z-nav)" as unknown as number,
      }}
    >
      <div className="container-site flex items-center justify-between w-full">
        <Link
          href="/"
          className="text-sm font-semibold tracking-tight no-underline"
          style={{ color: "var(--bp-text-0)" }}
        >
          <span style={{ color: "var(--bp-brand-500)" }}>Ideal</span> Best Practices
        </Link>
        <div className="flex items-center gap-3">
          <a
            href="https://github.com/MTleen/ideal-lab"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs font-medium px-3 py-1.5 rounded-full transition-colors hover:bg-[var(--bp-surface-2)] inline-flex items-center gap-1.5"
            style={{ color: "var(--bp-text-2)" }}
          >
            <GithubLogo size={14} weight="regular" />
            GitHub
          </a>
          <button
            onClick={toggleTheme}
            aria-label="Toggle theme"
            className="w-8 h-8 flex items-center justify-center rounded-full transition-colors hover:bg-[var(--bp-surface-2)]"
            style={{ color: "var(--bp-text-2)" }}
          >
            {dark ? (
              <Sun size={16} weight="regular" />
            ) : (
              <Moon size={16} weight="regular" />
            )}
          </button>
        </div>
      </div>
    </nav>
  );
}
