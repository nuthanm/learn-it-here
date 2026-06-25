import type { Metadata } from "next";
import "./globals.css";
import SiteHeader from "@/components/SiteHeader";
import SiteFooter from "@/components/SiteFooter";

export const metadata: Metadata = {
  title: "Learn It Here 🐼 — Know your stack before you build",
  description:
    "A 2-minute requirements questionnaire plus curated, opinionated guides for .NET, GIT, Blazor, EF Core and more. Export your answers as a PDF. Free forever.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased" style={{ background: "var(--surface)", minHeight: "100vh" }}>
        <SiteHeader />
        <div className="mx-auto px-6" style={{ maxWidth: 1200, paddingTop: 32, paddingBottom: 8 }}>
          <main>{children}</main>
          <SiteFooter />
        </div>
      </body>
    </html>
  );
}
