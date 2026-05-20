"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

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
      className="fixed top-0 inset-x-0 z-50 h-14 flex items-center backdrop-blur-md border-b"
      style={{
        background: "oklch(0.99 0.001 270 / 0.8)",
        borderColor: "var(--bp-border-0)",
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
            className="text-xs font-medium px-3 py-1.5 rounded-full transition-colors hover:bg-[var(--bp-surface-2)]"
            style={{ color: "var(--bp-text-2)" }}
          >
            GitHub
          </a>
          <button
            onClick={toggleTheme}
            aria-label="Toggle theme"
            className="w-8 h-8 flex items-center justify-center rounded-full transition-colors hover:bg-[var(--bp-surface-2)]"
            style={{ color: "var(--bp-text-2)" }}
          >
            {dark ? (
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="8" cy="8" r="3" />
                <path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1M12.95 3.05l-1.06 1.06M4.11 11.89l-1.06 1.06M12.95 12.95l-1.06-1.06M4.11 4.11L3.05 3.05" />
              </svg>
            ) : (
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M13.5 9.5A5.5 5.5 0 016.5 2.5 5.5 5.5 0 108.5 13.5 5.5 5.5 0 0113.5 9.5z" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </nav>
  );
}
