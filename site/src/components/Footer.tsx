export default function Footer() {
  return (
    <footer
      className="border-t py-8 mt-24"
      style={{ borderColor: "var(--bp-border-0)" }}
    >
      <div className="container-site flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-xs" style={{ color: "var(--bp-text-2)" }}>
          Built with{" "}
          <a
            href="https://nextjs.org"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "var(--bp-brand-500)" }}
          >
            Next.js
          </a>{" "}
          {"·"} Powered by{" "}
          <a
            href="https://github.com/MTleen/ideal-lab"
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: "var(--bp-brand-500)" }}
          >
            ideal-lab
          </a>
        </div>
        <div className="text-xs" style={{ color: "var(--bp-text-3)" }}>
          MIT License
        </div>
      </div>
    </footer>
  );
}
