import type { NextConfig } from "next";

// Fully static export: every view runs in the browser over the bundled JSON corpus.
// Assets are served from the domain root by default (Cloudflare Pages, local dev).
// For a sub-path host such as GitHub Pages, build with NEXT_PUBLIC_BASE_PATH=/repo-name.
const basePath = (process.env.NEXT_PUBLIC_BASE_PATH ?? "").replace(/\/$/, "");

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  // basePath breaks vinext 1.0.0-beta.5 prerendering ("RSC handler returned 404"),
  // so a sub-path only prefixes asset URLs; data links use lib/base-path.ts.
  ...(basePath ? { assetPrefix: basePath } : {}),
};

export default nextConfig;
