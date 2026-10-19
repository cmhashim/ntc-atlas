import { test, expect, type Page } from '@playwright/test';
import fs from 'node:fs';

const data = (name: string) => JSON.parse(fs.readFileSync(new URL(`../../public/data/${name}.json`, import.meta.url), 'utf8'));
const meta = data('meta');
const papers = data('papers') as { id: string; short: string; title: string }[];
const authors = data('authors') as { id: string; name: string; papers: string[] }[];
const etbert = papers.find((p) => p.id === 'etbert')!;
const libraryCount = (page: Page) => page.getByRole('heading', { name: /Paper library/ });
const countOf = async (page: Page) => Number(((await libraryCount(page).textContent()) ?? '').match(/\/\s*(\d+)/)![1]);

test('home loads with the corpus paper count', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Evolution of Network Traffic Classification');
  await expect(page.locator('.corpus-stats strong').first()).toHaveText(String(meta.paperCount));
  await expect(libraryCount(page)).toContainText(`/ ${meta.paperCount}`);
});

test('?paper=etbert opens the ET-BERT detail', async ({ page }) => {
  await page.goto('/?paper=etbert');
  const dialog = page.getByRole('dialog');
  await expect(dialog.getByRole('heading', { name: etbert.short })).toBeVisible();
  await expect(dialog).toContainText(etbert.title);
});

test('search filters the library', async ({ page }) => {
  await page.goto('/');
  await expect(libraryCount(page)).toContainText(`/ ${meta.paperCount}`);
  await page.getByLabel('Search papers').fill('ET-BERT');
  await expect.poll(() => countOf(page)).toBeLessThan(meta.paperCount);
  await expect(page.getByRole('button', { name: new RegExp(etbert.short) }).first()).toBeVisible();
});

test('a filter narrows the library and Reset restores it', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('combobox', { name: 'Model family' }).click();
  await page.getByRole('option').nth(1).click();
  await expect.poll(() => countOf(page)).toBeLessThan(meta.paperCount);
  await page.getByRole('button', { name: /Reset filters/ }).click();
  await expect(libraryCount(page)).toContainText(`/ ${meta.paperCount}`);
});

test('sorting and pagination work', async ({ page }) => {
  await page.goto('/');
  const firstRowYear = () => page.locator('.paper-table tbody tr').first().locator('.mono').textContent();
  const newest = await firstRowYear();
  await page.getByRole('button', { name: /^Year/ }).click();
  await expect.poll(firstRowYear).not.toBe(newest);
  await expect(page.getByText(/Page 1 of/)).toBeVisible();
  await page.getByRole('button', { name: 'Next paper page' }).click();
  await expect(page.getByText(/Page 2 of/)).toBeVisible();
  await page.getByRole('button', { name: 'Previous paper page' }).click();
  await expect(page.getByText(/Page 1 of/)).toBeVisible();
});

test('compare two papers', async ({ page }) => {
  await page.goto('/');
  const boxes = page.getByRole('checkbox', { name: /^Compare / });
  await boxes.nth(0).click();
  await boxes.nth(1).click();
  await expect(page.locator('.compare-tray .tray-count')).toHaveText('2/5');
  await page.locator('.compare-tray').getByRole('button', { name: /^Compare$/ }).click();
  await expect(page).toHaveURL(/view=compare/);
  await expect(page.getByRole('heading', { name: 'Compare methods and assumptions' })).toBeVisible();
  await expect(page.locator('.comparison-table thead th')).toHaveCount(3);
});

test('Claim vs evidence tab shows an Extracted fields fold', async ({ page }) => {
  await page.goto('/?paper=etbert');
  const dialog = page.getByRole('dialog');
  await dialog.getByRole('tab', { name: 'Claim vs evidence' }).click();
  await expect(dialog.getByText(/Extracted fields/).first()).toBeVisible();
});

test('the connections view renders a graph', async ({ page }) => {
  await page.goto('/?view=graph&focus=etbert');
  await expect(page.getByRole('heading', { name: 'Citations, comparisons and challenges' })).toBeVisible();
  await expect(page.locator('.graph-canvas .react-flow__node').first()).toBeVisible();
  expect(await page.locator('.graph-canvas svg').count()).toBeGreaterThan(0);
});

for (const [label, ext] of [['CSV', 'csv'], ['JSON', 'json'], ['BibTeX', 'bib']] as const) {
  test(`export ${label} triggers a download`, async ({ page }) => {
    await page.goto('/');
    const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: label, exact: true }).click()]);
    expect(download.suggestedFilename()).toMatch(new RegExp(`\\.${ext}$`));
  });
}

test('author view shows a profile link', async ({ page }) => {
  const author = authors[0];
  await page.goto(`/?view=authors&person=${author.id}`);
  await expect(page.getByRole('heading', { level: 2, name: author.name })).toBeVisible();
  await expect(page.getByRole('link', { name: /Google Scholar|Search on Google Scholar/ })).toHaveAttribute('href', /scholar\.google\.com/);
});

test('static SEO pages return 200', async ({ request }) => {
  for (const url of ['/paper/etbert/', `/author/${authors[0].id}/`, '/papers/']) {
    const res = await request.get(url);
    expect(res.status(), url).toBe(200);
  }
  expect(await (await request.get('/paper/etbert/')).text()).toContain(etbert.short);
});

test('mobile viewport has no horizontal page scroll', async ({ browser }) => {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const page = await context.newPage();
  await page.goto('/');
  await expect(libraryCount(page)).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(0);
  await context.close();
});
