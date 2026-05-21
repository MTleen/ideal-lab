import Link from "next/link";
import Nav from "@/components/Nav";

export default function NotFound() {
  const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  return (
    <>
      <Nav />
      <main className="flex-1 flex items-center justify-center pt-14">
        <div className="text-center px-6">
          <div
            className="w-20 h-20 mx-auto mb-8 rounded-full flex items-center justify-center"
            style={{ background: "var(--bp-surface-2)" }}
          >
            <svg
              width="32"
              height="32"
              viewBox="0 0 16 16"
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              style={{ color: "var(--bp-text-3)" }}
            >
              <circle cx="8" cy="8" r="1" />
              <path d="M3 8a5 5 0 0110 0" />
              <path d="M4 5a4 4 0 018 0" />
            </svg>
          </div>
          <h1
            className="text-2xl font-bold mb-3"
            style={{ color: "var(--bp-text-0)" }}
          >
            Page not found
          </h1>
          <p className="text-sm mb-6" style={{ color: "var(--bp-text-2)" }}>
            The page you are looking for does not exist.
          </p>
          <Link
            href={`${base}/`}
            className="inline-flex items-center h-10 px-5 rounded-xl text-sm font-semibold transition-all no-underline"
            style={{
              background: "var(--bp-brand-500)",
              color: "#fff",
            }}
          >
            Back to Home
          </Link>
        </div>
      </main>
    </>
  );
}
