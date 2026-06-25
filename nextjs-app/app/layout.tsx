import type { Metadata } from "next";
import "./globals.css";
import SiteHeader from "@/components/SiteHeader";
import SiteFooter from "@/components/SiteFooter";

export const metadata: Metadata = {
  title: "Learn It Here 🐼",
  description:
    "Know your stack before you build. A 2-minute questionnaire plus curated guides for .NET, GIT, Blazor, EF Core and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased" style={{ background: "var(--surface)" }}>
        <div className="mx-auto px-6" style={{ maxWidth: 1200 }}>
          <SiteHeader />
          <main>{children}</main>
          <SiteFooter />
        </div>
      </body>
    </html>
  );
}
