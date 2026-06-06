"use client";

import Link from "next/link";
import { CaretLeft, ArrowRight } from "@phosphor-icons/react";

export function CaretBackLink({ href, label }: { href: string; label: string }) {
  return (
    <Link
      href={href}
      className="inline-flex items-center gap-1.5 text-sm font-medium transition-colors no-underline"
      style={{ color: "var(--bp-text-2)" }}
    >
      <CaretLeft size={12} weight="bold" />
      {label}
    </Link>
  );
}

export function CtaArrowLink({ href, label }: { href: string; label: string }) {
  return (
    <Link
      href={href}
      className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors no-underline"
      style={{
        background: "var(--bp-brand-500)",
        color: "#fff",
      }}
    >
      {label}
      <ArrowRight size={14} weight="bold" />
    </Link>
  );
}
