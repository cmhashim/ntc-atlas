// The Methodology view offers README.md as a download; ship the canonical copy, not a duplicate in git.
import fs from 'node:fs';
fs.copyFileSync(new URL('../README.md', import.meta.url), new URL('../public/README.md', import.meta.url));
