// Keep the README counts table in sync with public/data.
//   node scripts/readme-counts.mjs          rewrite the table
//   node scripts/readme-counts.mjs --check  fail if the table is stale
import fs from 'node:fs';

const read = (n) => JSON.parse(fs.readFileSync(new URL(`../public/data/${n}.json`, import.meta.url)));
const n = (name) => read(name).length;
const table = [
  '| Papers | Authors | Datasets | Relationships | Evidence records |',
  '| ---: | ---: | ---: | ---: | ---: |',
  `| ${n('papers')} | ${n('authors')} | ${n('datasets')} | ${n('relationships')} | ${n('evidence')} |`,
].join('\n');

const readmeUrl = new URL('../README.md', import.meta.url);
const readme = fs.readFileSync(readmeUrl, 'utf8');
const block = /(<!-- corpus-counts:start[^>]*-->\n)[\s\S]*?(\n<!-- corpus-counts:end -->)/;
if (!block.test(readme)) throw new Error('README.md is missing the corpus-counts markers.');
const updated = readme.replace(block, `$1${table}$2`);

if (process.argv.includes('--check')) {
  if (updated !== readme) {
    console.error('README corpus counts are stale. Run `pnpm counts`.');
    process.exit(1);
  }
  console.log('README corpus counts match public/data.');
} else {
  fs.writeFileSync(readmeUrl, updated);
  console.log('README corpus counts updated.');
}
