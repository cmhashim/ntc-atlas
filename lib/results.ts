// Comparable results: grouping rules for public/data/results.json.
// Two results are comparable only when dataset, class count, split unit, metric, averaging
// (for F1, precision and recall) and setting class all match. Anything else is listed apart, with the reason.
import type {Result} from './schema';

const averaged = (r: Result) => r.metric === 'F1' || r.metric === 'precision' || r.metric === 'recall';

export function missingFields(r: Result): string[] {
  const out: string[] = [];
  if (r.classes === null) out.push('class count not stated');
  if (r.splitUnit === null) out.push('split unit not stated');
  if (averaged(r) && r.averaging === null) out.push('averaging not stated');
  return out;
}

export function comparabilityKey(r: Result): string {
  return [r.dataset, r.classes, r.splitUnit, r.metric, averaged(r) ? r.averaging : '', r.settingClass].join('|');
}

export interface ResultGroup { key: string; rows: Result[]; papers: number; classes: number|null; splitUnit: string|null; metric: string; averaging: string|null; settingClass: string; tasks: string[]; }

export function groupResults(rows: Result[]): {groups: ResultGroup[]; apart: {row: Result; reasons: string[]}[]} {
  const byKey = new Map<string, Result[]>();
  const apart: {row: Result; reasons: string[]}[] = [];
  for (const r of rows) {
    const reasons = missingFields(r);
    if (reasons.length) { apart.push({row: r, reasons}); continue; }
    const k = comparabilityKey(r);
    byKey.set(k, [...(byKey.get(k) ?? []), r]);
  }
  const groups = [...byKey.entries()].map(([key, rs]) => {
    const r = rs[0];
    return {key, rows: [...rs].sort((a, b) => b.value - a.value), papers: new Set(rs.map(x => x.paper)).size,
      classes: r.classes, splitUnit: r.splitUnit, metric: r.metric, averaging: averaged(r) ? r.averaging : null,
      settingClass: r.settingClass, tasks: [...new Set(rs.map(x => x.task))]};
  });
  groups.sort((a, b) => b.papers - a.papers || b.rows.length - a.rows.length || a.key.localeCompare(b.key));
  return {groups, apart};
}
