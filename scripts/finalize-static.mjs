// Assemble the deployable static site in out/ from vinext's dist/client.
// With NEXT_PUBLIC_BASE_PATH set, vinext writes hashed assets under dist/client/<base>/_next;
// the host already maps the site root to <base>, so those assets move up to out/_next.
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const client = path.join(root, 'dist', 'client');
const out = path.join(root, 'out');
const base = (process.env.NEXT_PUBLIC_BASE_PATH ?? '').replace(/^\/|\/$/g, '');

if (!fs.existsSync(path.join(client, 'index.html'))) {
  throw new Error('dist/client/index.html is missing: the static export did not prerender "/".');
}
fs.rmSync(out, { recursive: true, force: true });
fs.cpSync(client, out, { recursive: true });
if (base) {
  const nested = path.join(out, base);
  fs.cpSync(nested, out, { recursive: true });
  fs.rmSync(nested, { recursive: true, force: true });
}
// Build manifests are not site content.
for (const name of ['.vite', 'vinext-client-entry-manifest.json']) fs.rmSync(path.join(out, name), { recursive: true, force: true });
console.log(`Static site ready in out/ (base: ${base ? '/' + base + '/' : '/'})`);
await import('./seo-pages.mjs');
