/** @type {import('next').NextConfig} */
const nextConfig = {
  // ── Legacy URL redirects (Streamlit → Next.js parity) ─────────────────────
  // These preserve shared links that used the old ?page=… / ?go=home query
  // params from the Streamlit version. All redirects are permanent (308) so
  // search engines and bookmarks update automatically.
  async redirects() {
    return [
      // ?go=home → /
      {
        source: "/",
        has: [{ type: "query", key: "go", value: "home" }],
        destination: "/",
        permanent: true,
      },
      // ?page=landing → /
      {
        source: "/",
        has: [{ type: "query", key: "page", value: "landing" }],
        destination: "/",
        permanent: true,
      },
      // ?page=requirements → /projectrequirements
      {
        source: "/",
        has: [{ type: "query", key: "page", value: "requirements" }],
        destination: "/projectrequirements",
        permanent: true,
      },
      // ?page=learn → /learning-hub (section/sub forwarded automatically
      // because Next.js preserves unmatched query params in `has` redirects)
      {
        source: "/",
        has: [{ type: "query", key: "page", value: "learn" }],
        destination: "/learning-hub",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
