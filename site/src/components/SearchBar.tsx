"use client";

import { useRef, useEffect } from "react";

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export default function SearchBar({ value, onChange }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  return (
    <div className="relative max-w-md w-full">
      <svg
        className="absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.5"
        style={{ color: "var(--bp-text-3)" }}
      >
        <circle cx="7" cy="7" r="4.5" />
        <path d="M10.5 10.5L14 14" />
      </svg>
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search plugins and skills..."
        className="w-full h-12 pl-11 pr-16 text-base rounded-2xl border outline-none transition-colors focus:border-[var(--bp-brand-500)] focus:ring-0"
        style={{
          background: "var(--bp-surface-1)",
          borderColor: value ? "var(--bp-brand-400)" : "var(--bp-border-0)",
          color: "var(--bp-text-0)",
        }}
      />
      <kbd
        className="absolute right-3 top-1/2 -translate-y-1/2 text-[11px] font-medium px-1.5 py-0.5 rounded"
        style={{
          background: "var(--bp-surface-2)",
          color: "var(--bp-text-3)",
          border: "1px solid var(--bp-border-0)",
        }}
      >
        ⌘K
      </kbd>
    </div>
  );
}
