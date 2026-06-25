import Link from "next/link";

const FOOTER_LINKS = [
  { href: "/", label: "Home" },
  { href: "/projectrequirements", label: "Requirements" },
  { href: "/learning-hub", label: "Learning Hub" },
  { href: "/learning-hub?section=topic-suggestions", label: "Suggest a Topic" },
];

export default function SiteFooter() {
  return (
    <footer
      style={{
        borderTop: "1px solid var(--border)",
        marginTop: 64,
        paddingTop: 32,
        paddingBottom: 32,
      }}>
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        {/* Brand */}
        <div>
          <Link href="/" className="inline-flex items-center gap-2 no-underline mb-2"
            style={{ color: "var(--ink)", fontWeight: 800, fontSize: 14 }}>
            <span>🐼</span>
            <span>Learn It Here</span>
          </Link>
          <p style={{ fontSize: 12, color: "var(--muted)", maxWidth: 260, lineHeight: 1.6, marginTop: 4 }}>
            Know your stack before you build. Curated guides for .NET developers.
          </p>
        </div>

        {/* Links */}
        <nav className="flex flex-wrap gap-x-6 gap-y-2" aria-label="Footer">
          {FOOTER_LINKS.map(({ href, label }) => (
            <Link key={href} href={href}
              className="no-underline hover:underline"
              style={{ fontSize: 12, color: "var(--muted)" }}>
              {label}
            </Link>
          ))}
        </nav>
      </div>

      <div
        className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mt-6 pt-5"
        style={{ borderTop: "1px solid var(--border)", fontSize: 11, color: "var(--muted)" }}>
        <span>© 2026 Learn It Here. Open-source — free to adapt.</span>
        <span>Built with Next.js 14, Tailwind CSS &amp; Neon DB</span>
      </div>
    </footer>
  );
}
