"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/projectrequirements", label: "Requirements" },
  { href: "/learning-hub", label: "Learn" },
];

export default function SiteHeader() {
  const pathname = usePathname();

  return (
    <header className="flex items-center justify-between py-3 pb-4 border-b flex-wrap gap-3 mb-6"
      style={{ borderColor: "var(--border)" }}>
      <Link href="/" className="inline-flex items-center gap-2 font-bold text-base no-underline"
        style={{ color: "var(--ink)", letterSpacing: "-0.01em" }}>
        <span className="text-sm">🐼</span>
        <span>Learn It Here</span>
      </Link>
      <nav className="flex items-center gap-6" aria-label="Primary">
        {NAV_LINKS.map(({ href, label }) => {
          const isActive =
            href === "/"
              ? pathname === "/"
              : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className="text-sm font-semibold no-underline pb-0.5 border-b-2 transition-colors duration-150"
              style={{
                color: isActive ? "var(--ink)" : "var(--muted)",
                borderBottomColor: isActive ? "var(--accent)" : "transparent",
              }}>
              {label}
            </Link>
          );
        })}
      </nav>
    </header>
  );
}
