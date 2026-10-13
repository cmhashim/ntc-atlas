// Public URL prefix for hand-written links to files in public/ (data, README, favicon).
// Empty when the site is served from a domain root (Cloudflare Pages, local dev).
// Set NEXT_PUBLIC_BASE_PATH=/sub-path at build time to host under a sub-path instead.
export const basePath = (process.env.NEXT_PUBLIC_BASE_PATH ?? '').replace(/\/$/, '');
export const withBase = (path: string) => `${basePath}${path}`;
