import Link from "next/link";
import Nav from "@/components/Nav";
import NotFoundIcon from "@/components/NotFoundIcon";

export default function NotFound() {
  return (
    <>
      <Nav />
      <main className="flex-1 flex items-center justify-center pt-14">
        <div className="text-center px-6">
          <div
            className="w-20 h-20 mx-auto mb-8 rounded-full flex items-center justify-center"
            style={{ background: "var(--bp-surface-2)" }}
          >
            <NotFoundIcon />
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
            href={`/`}
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
