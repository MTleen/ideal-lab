"use client";

import { useRef, useEffect } from "react";
import { MagnifyingGlass } from "@phosphor-icons/react";

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
      <MagnifyingGlass
        size={16}
        weight="regular"
        className="absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none"
        style={{ color: "var(--bp-text-3)" }}
      />
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
