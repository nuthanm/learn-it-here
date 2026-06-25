"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/projectrequirements", label: "Requirements" },
  { href: "/learning-hub", label: "Learn" },
];

export default function SiteHeader() {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header
      style={{
        borderBottom: "1px solid var(--border)",
        marginBottom: 0,
        position: "sticky",
        top: 0,
        zIndex: 50,
        background: "rgba(249,250,251,0.92)",
        backdropFilter: "blur(10px)",
        WebkitBackdropFilter: "blur(10px)",
      }}>
      <div
        className="mx-auto px-6 flex items-center justify-between"
        style={{ maxWidth: 1200, height: 56 }}>
        {/* Logo */}
        <Link
          href="/"
          className="inline-flex items-center gap-2 no-underline"
          style={{ color: "var(--ink)", fontWeight: 800, fontSize: 15, letterSpacing: "-0.02em" }}>
          <span style={{ fontSize: 18 }}>🐼</span>
          <span>Learn It Here</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1" aria-label="Primary">
          {NAV_LINKS.map(({ href, label }) => {
            const isActive = href === "/" ? pathname === "/" : pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className="no-underline"
                style={{
                  padding: "6px 14px",
                  borderRadius: "var(--r-sm)",
                  fontSize: 13,
                  fontWeight: isActive ? 700 : 500,
                  color: isActive ? "var(--ink)" : "var(--muted)",
                  background: isActive ? "var(--accent-soft)" : "transparent",
                  transition: "background 120ms ease, color 120ms ease",
                }}>
                {label}
              </Link>
            );
          })}
          <Link href="/projectrequirements" className="btn-primary ml-3" style={{ fontSize: 12, padding: "6px 16px" }}>
            Start free →
          </Link>
        </nav>

        {/* Mobile menu toggle */}
        <button
          className="md:hidden flex flex-col gap-1 p-2"
          onClick={() => setMenuOpen((v) => !v)}
          aria-label="Toggle menu"
          style={{ background: "none", border: "none", cursor: "pointer" }}>
          <span style={{ display: "block", width: 20, height: 2, background: "var(--ink)", borderRadius: 2 }} />
          <span style={{ display: "block", width: 20, height: 2, background: "var(--ink)", borderRadius: 2 }} />
          <span style={{ display: "block", width: 20, height: 2, background: "var(--ink)", borderRadius: 2 }} />
        </button>
      </div>

      {/* Mobile dropdown */}
      {menuOpen && (
        <div
          style={{
            borderTop: "1px solid var(--border)",
            background: "var(--card)",
            padding: "8px 16px 16px",
          }}>
          {NAV_LINKS.map(({ href, label }) => {
            const isActive = href === "/" ? pathname === "/" : pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                onClick={() => setMenuOpen(false)}
                className="block no-underline"
                style={{
                  padding: "10px 12px",
                  fontSize: 14,
                  fontWeight: isActive ? 700 : 500,
                  color: isActive ? "var(--accent-hover)" : "var(--body)",
                  borderRadius: "var(--r-sm)",
                  background: isActive ? "var(--accent-soft)" : "transparent",
                }}>
                {label}
              </Link>
            );
          })}
          <Link
            href="/projectrequirements"
            onClick={() => setMenuOpen(false)}
            className="btn-primary mt-3"
            style={{ fontSize: 13, width: "100%", justifyContent: "center" }}>
            Start questionnaire →
          </Link>
        </div>
      )}
    </header>
  );
}
