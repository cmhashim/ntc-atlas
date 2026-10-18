import rawPapers from '@/public/data/papers.json';
import rawAuthors from '@/public/data/authors.json';
import rawDatasets from '@/public/data/datasets.json';
import rawEdges from '@/public/data/relationships.json';
import rawEvidence from '@/public/data/evidence.json';
import rawMeta from '@/public/data/meta.json';
import type { Paper, Author, Dataset, Relationship, Evidence } from './schema';

export const papers = rawPapers as Paper[];
export const authors = rawAuthors as Author[];
export const datasets = rawDatasets as Dataset[];
export const relationships = rawEdges as Relationship[];
export const evidence = rawEvidence as Evidence[];
export const meta = rawMeta;
export const paperById = Object.fromEntries(papers.map(p => [p.id,p]));
export const authorById = Object.fromEntries(authors.map(a => [a.id,a]));
export const datasetById = Object.fromEntries(datasets.map(d => [d.id,d]));
export const evidenceById = Object.fromEntries(evidence.map(e => [e.id,e]));
export const families = ['Rules & statistics','Classical ML','Deep learning','Transformer','Masked autoencoder','State space','Graph learning','Deployment','Evaluation & surveys'];
export const colors:Record<string,string> = Object.fromEntries(families.map((f,i)=>[f,`var(--fam-${i})`]));
export function familyGroup(p:Paper) {if(p.family==='Self-supervised')return p.techniques.includes('Masked autoencoding')?'Masked autoencoder':'Deep learning';return families.includes(p.family) ? p.family : /cnn|rnn|deep|multimodal/i.test(p.family) ? 'Deep learning' : /transform/i.test(p.family) ? 'Transformer' : /mask|autoencoder/i.test(p.family)?'Masked autoencoder':'Classical ML';}
export function color(p:Paper) {return colors[familyGroup(p)];}
export const filterKeys=['family','unit','venue','dataset','task','encrypted','payload','pretraining','openWorld','crossDataset','code','deployment','reproducibility','author','technique'] as const;
export type FilterKey=typeof filterKeys[number];
export type Filters={q:string;from:number;to:number;seminal:boolean}&Record<FilterKey,string>;
export const emptyFilters:Filters={q:'',from:2004,to:2026,seminal:false,...Object.fromEntries(filterKeys.map(k=>[k,'all']))} as Filters;
export const filterLabels:Record<FilterKey,string>={family:'Model family',unit:'Traffic unit',venue:'Venue',dataset:'Dataset',task:'Task',encrypted:'Encrypted traffic',payload:'Payload used',pretraining:'Pretraining',openWorld:'Open-world evaluation',crossDataset:'Cross-dataset evaluation',code:'Code availability',deployment:'Deployment evaluation',reproducibility:'Reproducibility',author:'Author',technique:'Technique'};
export function filterPapers(f:Filters,source=papers) {const q=f.q.trim().toLocaleLowerCase();return source.filter(p=>p.year>=f.from&&p.year<=f.to&&(!f.seminal||p.seminal)&&(!q||[p.short,p.title,...p.authors,p.venue,...p.techniques,...p.datasets.map(id=>datasetById[id]?.name||id)].join(' ').toLocaleLowerCase().includes(q))&&filterKeys.every(k=>f[k]==='all'||(k==='dataset'?p.datasets.includes(f[k]):k==='author'?p.authors.includes(authorById[f[k]]?.name):k==='technique'?p.techniques.includes(f[k]):k==='code'?(p.code?'Linked':'Needs verification')===f[k]:String(p[k])===f[k])));}
export function options(k:FilterKey):{value:string;label:string}[]{if(k==='dataset')return datasets.map(d=>({value:d.id,label:d.name}));if(k==='author')return authors.map(a=>({value:a.id,label:a.name}));if(k==='code')return ['Linked','Needs verification'].map(v=>({value:v,label:v}));const values=k==='technique'?papers.flatMap(p=>p.techniques):papers.map(p=>String(p[k]));return [...new Set(values)].sort().map(v=>({value:v,label:v}));}
export function parseFilters(params:URLSearchParams):Filters {const f={...emptyFilters};f.q=(params.get('q')||'').slice(0,300);const from=Number(params.get('from')||2004),to=Number(params.get('to')||2026);if(Number.isFinite(from)&&Number.isFinite(to)){f.from=Math.max(2004,Math.min(2026,from));f.to=Math.max(f.from,Math.min(2026,to));}f.seminal=params.get('seminal')==='1';for(const k of filterKeys){const value=params.get(k);if(value&&options(k).some(o=>o.value===value))f[k]=value;}return f;}
export function serializeFilters(f:Filters){const params=new URLSearchParams();if(f.q)params.set('q',f.q);if(f.from!==2004)params.set('from',String(f.from));if(f.to!==2026)params.set('to',String(f.to));if(f.seminal)params.set('seminal','1');for(const k of filterKeys)if(f[k]!=='all')params.set(k,f[k]);return params;}
export function bibtex(p:Paper){const esc=(s:string)=>s.replace(/\\/g,'\\textbackslash{}').replace(/([&%_$#])/g,'\\$1').replace(/[{}]/g,c=>c);return `@misc{${p.id}${p.year},\n  title = {{${esc(p.title)}}},\n  author = {${p.authors.map(esc).join(' and ')}},\n  year = {${p.year}},\n  howpublished = {${esc(p.venue)}},\n  url = {${p.url}},\n  note = {${esc(p.publicationStatus)}; accessed ${evidence.find(e=>e.paperId===p.id&&e.category==='Bibliography')?.accessed||meta.updated}}\n}`;}
export function csv(selected:Paper[]){const keys=['id','title','authors','year','venue','publicationStatus','url','code','family','unit','task','datasets','payload','pretraining','crossDataset','openWorld','reproducibility','reviewDepth'] as const;const details=Object.keys(papers[0].details);const cell=(v:unknown)=>'"'+String(Array.isArray(v)?v.join('; '):v??'').replace(/"/g,'""')+'"';return [[...keys,...details,...meta.gapColumns.map(g=>'Gap: '+g)].map(cell).join(','),...selected.map(p=>[...keys.map(k=>p[k]),...details.map(k=>p.details[k]),...meta.gapColumns.map(g=>p.gaps[g].state)].map(cell).join(','))].join('\r\n');}
export function download(selected:Paper[],format:'json'|'csv'|'bib'){const content=format==='json'?JSON.stringify({updated:meta.updated,scope:meta.scope,papers:selected,authors:authors.filter(a=>selected.some(p=>p.authors.includes(a.name))),datasets:datasets.filter(d=>selected.some(p=>p.datasets.includes(d.id))),evidence:evidence.filter(e=>selected.some(p=>p.id===e.paperId)),relationships:relationships.filter(r=>selected.some(p=>p.id===r.source)&&selected.some(p=>p.id===r.target))},null,2):format==='csv'?csv(selected):selected.map(bibtex).join('\n\n');const blob=new Blob([content],{type:format==='json'?'application/json':format==='csv'?'text/csv;charset=utf-8':'text/plain;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`ntc-atlas-${selected.length}.${format}`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),30000);}
