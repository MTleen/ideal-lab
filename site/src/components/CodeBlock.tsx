"use client";

import { useState } from "react";
import { Check, Copy } from "@phosphor-icons/react";

export default function CodeBlock({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);

  function copy() {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  return (
    <div className="code-block group">
      <button
        onClick={copy}
        className="absolute top-3 right-3 flex items-center gap-1.5 text-xs font-medium transition-colors px-2 py-1 rounded-md"
        style={{
          background: "var(--bp-surface-3)",
          color: copied ? "var(--bp-success)" : "var(--bp-text-2)",
        }}
      >
        {copied ? (
          <>
            <Check size={12} weight="bold" />
            Copied
          </>
        ) : (
          <>
            <Copy size={12} weight="regular" />
            Copy
          </>
        )}
      </button>
      <pre className="text-sm leading-relaxed" style={{ color: "var(--bp-text-1)" }}>
        {code.split("\n").map((line, i) => (
          <div key={i} className="flex">
            <span
              className="select-none w-8 shrink-0 text-right mr-4 text-xs"
              style={{ color: "var(--bp-text-3)" }}
            >
              {i + 1}
            </span>
            <span>{line || " "}</span>
          </div>
        ))}
      </pre>
    </div>
  );
}
