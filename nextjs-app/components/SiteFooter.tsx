export default function SiteFooter() {
  return (
    <footer className="flex items-center justify-between py-6 mt-12 text-xs border-t"
      style={{ color: "var(--muted)", borderColor: "var(--border)" }}>
      <span>© 2026 Learn It Here</span>
      <span>Built with Next.js &amp; Neon DB</span>
    </footer>
  );
}
