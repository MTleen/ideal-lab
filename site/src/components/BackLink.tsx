"use client";

import { CaretLeft } from "@phosphor-icons/react";

interface Props {
  href: string;
  label: string;
}

export default function BackLink({ href, label }: Props) {
  return (
    <a
      href={href}
      className="inline-flex items-center gap-1.5 text-sm font-medium transition-colors no-underline"
      style={{ color: "var(--bp-text-2)" }}
    >
      <CaretLeft size={12} weight="bold" />
      {label}
    </a>
  );
}
