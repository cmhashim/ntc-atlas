import fs from 'node:fs';
import assert from 'node:assert/strict';
const read=n=>JSON.parse(fs.readFileSync(new URL(`../public/data/${n}.json`,import.meta.url)));
const papers=read('papers'),authors=read('authors'),datasets=read('datasets'),evidence=read('evidence'),edges=read('relationships'),meta=read('meta');
const unique=(arr,key)=>{assert.equal(new Set(arr.map(x=>x[key])).size,arr.length,`Duplicate ${key}`);};
for(const arr of [papers,authors,datasets,evidence,edges])unique(arr,'id');
unique(papers,'url');unique(papers,'title');unique(authors,'name');
const ids=new Set(papers.map(p=>p.id)),eids=new Set(evidence.map(e=>e.id)),dids=new Set(datasets.map(d=>d.id));
// Structured results (Comparable results view): known papers and datasets, closed vocabularies, 0-100 values.
const results=read('results');unique(results,'id');assert.equal(meta.resultCount,results.length,'meta.resultCount is stale');
for(const r of results){
 assert(ids.has(r.paper),`Result ${r.id}: unknown paper ${r.paper}`);assert(dids.has(r.dataset),`Result ${r.id}: unknown dataset ${r.dataset}`);
 assert(['accuracy','F1','precision','recall','AUROC'].includes(r.metric),`Result ${r.id}: metric ${r.metric}`);
 assert(r.averaging===null||['macro','weighted','micro'].includes(r.averaging),`Result ${r.id}: averaging ${r.averaging}`);
 assert(typeof r.value==='number'&&r.value>=0&&r.value<=100,`Result ${r.id}: value ${r.value}`);
 assert(r.locator&&r.quote,`Result ${r.id}: locator and quote required`);
}
for(const p of papers){
 assert(p.year>=2004&&p.year<=2026);assert(p.authors.length);assert(/^https:\/\//.test(p.url));
 assert.equal(Object.keys(p.gaps).length,16);assert(p.evidenceIds.length>=3);
 for(const id of p.datasets)assert(dids.has(id),`Unknown dataset ${id}`);
 for(const id of p.evidenceIds)assert(eids.has(id));
 for(const [field,id] of Object.entries(p.fieldEvidence||{})){assert(field in p.details);assert(eids.has(id));}
 for(const g of Object.values(p.gaps)){assert(['Addressed','Partially addressed','Not addressed/not reported'].includes(g.state));assert(g.note);assert(g.evidence.length);for(const id of g.evidence)assert(eids.has(id));}
 for(const name of p.authors)assert(authors.some(a=>a.name===name&&a.papers.includes(p.id)),`Missing author ${name}`);
}
const doiSeen=new Map(),arxivSeen=new Map();
for(const p of papers){
 assert(p.doi===null||typeof p.doi==='string',`doi must be a string or null: ${p.id}`);assert(p.arxivId===null||typeof p.arxivId==='string',`arxivId must be a string or null: ${p.id}`);
 if(p.doi!==null){assert(/^10\.\d{4,9}\/\S+$/.test(p.doi),`Malformed DOI: ${p.id}`);const k=p.doi.toLowerCase();assert(!doiSeen.has(k),`DOI shared by ${doiSeen.get(k)} and ${p.id}`);doiSeen.set(k,p.id);}
 if(p.arxivId!==null){assert(/^(\d{4}\.\d{4,5}|[a-z-]+(\.[A-Z]{2})?\/\d{7})$/.test(p.arxivId),`Malformed arXiv id (bare, no version): ${p.id}`);assert(!arxivSeen.has(p.arxivId),`arXiv id shared by ${arxivSeen.get(p.arxivId)} and ${p.id}`);arxivSeen.set(p.arxivId,p.id);}
}
for(const a of authors){assert(a.papers.length,`Author without a relevant publication: ${a.name}`);for(const id of a.papers)assert(papers.some(p=>p.id===id&&p.authors.includes(a.name)),`Unsupported authorship: ${a.name}`);}
for(const d of datasets)for(const id of d.papers){assert(ids.has(id));assert(papers.find(p=>p.id===id).datasets.includes(d.id));}
for(const d of datasets)if(d.introducedBy){const x=d.introducedBy;assert(eids.has(x.evidence),`Unknown introducer evidence ${d.id}`);assert(x.paper?ids.has(x.paper):x.citation,`Introducer of ${d.id} needs a known paper or a citation`);}
for(const r of edges){assert(ids.has(r.source)&&ids.has(r.target));assert(r.source!==r.target);assert(eids.has(r.evidenceId));assert(r.explanation);}
for(const e of evidence){assert(/^https:\/\//.test(e.sourceUrl));assert(e.locator&&e.text&&e.sourceType&&e.status&&e.accessed);assert(ids.has(e.paperId)||e.paperId.startsWith('dataset:'));}
assert.equal(meta.paperCount,papers.length);assert.equal(meta.authorCount,authors.length);assert.equal(meta.relationshipCount,edges.length);
assert.equal(papers.filter(p=>/deep packet/i.test(p.title)).length,1,'Deep Packet alias duplicated');
assert.notEqual(datasets.find(d=>d.id==='iscxvpn').url,datasets.find(d=>d.id==='iscxtor').url);
assert.equal(papers.find(p=>p.id==='netfound').details['Version notes'].includes('2026'),true);
assert(edges.some(r=>r.source==='netmambaplus'&&r.target==='netmamba'&&r.type==='Extends'));
for(const id of meta.authorExpansion.papers){const p=papers.find(p=>p.id===id);assert(p&&p.year>=2023);}
for(const id of ['lim','labelprovenance','ntcsurvey2026','ntfmsurvey2026'])assert(ids.has(id));
assert(authors.find(a=>a.name==='Nimesha Wickramasinghe').papers.includes('lim'));
const orcidOk=id=>{if(!/^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/.test(id))return false;const d=id.replace(/-/g,'');let t=0;for(const c of d.slice(0,15))t=(t+Number(c))*2;const r=(12-t%11)%11;return d[15]===(r===10?'X':String(r));};
const orcids=new Set(),scholars=new Set();
for(const a of authors){
 if(a.scholarUrl){const m=a.scholarUrl.match(/^https:\/\/scholar\.google\.com\/citations\?(?:.*&)?user=([A-Za-z0-9_-]{12})(?:&|$)/);assert(m,`Scholar link must be a direct https profile URL: ${a.name}`);assert(!scholars.has(m[1]),`Scholar profile used twice: ${a.name}`);scholars.add(m[1]);assert(a.scholarSource,`Scholar link without source: ${a.name}`);}
 if(a.orcid){assert(orcidOk(a.orcid),`Invalid ORCID iD: ${a.name}`);assert(!orcids.has(a.orcid),`ORCID used twice: ${a.name}`);orcids.add(a.orcid);assert(a.orcidSource,`ORCID without source: ${a.name}`);}
 if(a.homepageUrl){assert(/^https?:\/\//.test(a.homepageUrl),`Invalid homepage URL: ${a.name}`);assert(a.homepageSource,`Homepage without source: ${a.name}`);}
 if(a.scholarUrl||a.orcid||a.homepageUrl||a.publicationsUrl)assert(/^\d{4}-\d{2}-\d{2}$/.test(a.identityChecked??''),`Profile links without check date: ${a.name}`);
}
const zhuotao=authors.find(a=>a.name==='Zhuotao Liu');
assert.equal(zhuotao.status,'Verified');
assert(zhuotao.scholarUrl?.includes('F8gi4rcAAAAJ'));
assert(/^https:\/\/liuzhuotao\.github\.io\/publications\/$/.test(zhuotao.publicationsUrl));
const luming=authors.find(a=>a.name==='Luming Yang');
assert.equal(luming.status,'Verified');
assert(luming.scholarUrl?.includes('Xt7NczsAAAAJ'));
for(const id of ['evs2vec','expmd','unflows','robustnessmatters','semiaf','mm4flow'])assert(luming.papers.includes(id));
assert.equal(authors.find(a=>a.id==='dario-rossi').publicationsUrl,'https://nonsns.github.io/publications/date/');
const xiaohui=authors.find(a=>a.name==='Xiaohui Xie');
assert(xiaohui.scholarUrl?.includes('j0yTuxoAAAAJ'));
assert(xiaohui.publicationsUrl?.startsWith('https://thuxiexiaohui.github.io/'));
const provenance=read('label-provenance');assert(ids.has(provenance.paperId));
for(const row of provenance.datasets){assert(dids.has(row.id));assert(row.assignment&&row.evidence&&row.evidenceUnit&&row.semanticObject);}

// ---- Extended integrity checks -------------------------------------------------
// Each check returns a list of problem messages. A check listed in WARN_ONLY prints its
// problems as warnings and does not fail the build; every other check is fatal.
const WARN_ONLY=new Set(['verified-evidence-placeholders']); // real data problems found 2026-10-19 (e0178, e0230); promote to fatal once fixed
const problems=[];const warnings=[];
const check=(name,fn)=>{const found=fn();if(!found.length)return;(WARN_ONLY.has(name)?warnings:problems).push({name,found});};
const isHttpUrl=v=>{try{const u=new URL(v);return u.protocol==='https:'||u.protocol==='http:';}catch{return false;}};
const normTitle=t=>t.normalize('NFKD').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
const walkStrings=(v,pathStr,fn)=>{if(typeof v==='string')fn(v,pathStr);else if(Array.isArray(v))v.forEach((x,i)=>walkStrings(x,`${pathStr}[${i}]`,fn));else if(v&&typeof v==='object')for(const [k,x] of Object.entries(v))walkStrings(x,`${pathStr}.${k}`,fn);};

check('relationship-evidence-id',()=>edges.filter(r=>!r.evidenceId||!eids.has(r.evidenceId)).map(r=>`relationship ${r.id} (${r.source} -> ${r.target}) has missing or unknown evidenceId "${r.evidenceId}"`));

check('evidence-references',()=>{const out=[];const need=(owner,id)=>{if(!eids.has(id))out.push(`${owner} references unknown evidence id "${id}"`);};
 for(const p of papers){p.evidenceIds.forEach(id=>need(`paper ${p.id} evidenceIds`,id));for(const [f,id] of Object.entries(p.fieldEvidence||{}))need(`paper ${p.id} fieldEvidence.${f}`,id);for(const [g,v] of Object.entries(p.gaps))v.evidence.forEach(id=>need(`paper ${p.id} gap "${g}"`,id));}
 for(const r of edges)need(`relationship ${r.id}`,r.evidenceId);
 for(const d of datasets){if(d.introducedBy)need(`dataset ${d.id} introducedBy`,d.introducedBy.evidence);(d.caveatEvidence||[]).forEach(id=>need(`dataset ${d.id} caveatEvidence`,id));if(d.evidence)need(`dataset ${d.id} evidence`,d.evidence);}
 return out;});

check('qualified-NA',()=>{const out=[];const bad=v=>/^NA\b/.test(v.trim())&&!/^NA — \S/.test(v.trim());
 const scan=(owner,obj)=>walkStrings(obj,owner,(v,where)=>{if(bad(v))out.push(`${where}: unqualified NA "${v.length>60?v.slice(0,60)+'…':v}" (use "NA — <reason>")`);});
 for(const p of papers)scan(`paper ${p.id}`,{details:p.details,code:p.code,openWorld:p.openWorld,crossDataset:p.crossDataset,deployment:p.deployment,reproducibility:p.reproducibility,pretraining:p.pretraining,encrypted:p.encrypted,payload:p.payload});
 for(const d of datasets)scan(`dataset ${d.id}`,d);for(const a of authors)scan(`author ${a.id}`,a);return out;});

check('url-fields',()=>{const out=[];const test=(owner,field,v)=>{if(v!=null&&v!==''&&!isHttpUrl(v))out.push(`${owner}.${field} is not a valid http(s) URL: "${v}"`);};
 for(const p of papers){test(`paper ${p.id}`,'url',p.url);test(`paper ${p.id}`,'code',p.code);}
 for(const d of datasets)test(`dataset ${d.id}`,'url',d.url);
 for(const e of evidence)test(`evidence ${e.id}`,'sourceUrl',e.sourceUrl);
 for(const a of authors)for(const f of ['scholarUrl','homepageUrl','publicationsUrl','sourceUrl','profile'])test(`author ${a.id}`,f,a[f]);
 return out;});

check('duplicate-titles',()=>{const seen=new Map(),out=[];for(const p of papers){const k=normTitle(p.title);if(seen.has(k))out.push(`papers ${seen.get(k)} and ${p.id} have the same normalised title "${k}"`);else seen.set(k,p.id);}return out;});

check('author-paper-reciprocity',()=>{const out=[];const byName=new Map(authors.map(a=>[a.name,a]));
 for(const p of papers)for(const name of p.authors){const a=byName.get(name);if(!a)out.push(`paper ${p.id} lists author "${name}" who has no author record`);else if(!a.papers.includes(p.id))out.push(`paper ${p.id} lists "${name}" but author ${a.id}.papers does not list the paper`);}
 for(const a of authors)for(const id of a.papers){const p=papers.find(p=>p.id===id);if(!p)out.push(`author ${a.id} lists unknown paper ${id}`);else if(!p.authors.includes(a.name))out.push(`author ${a.id} lists paper ${id} whose byline does not include "${a.name}"`);}
 return out;});

check('dataset-paper-reciprocity',()=>{const out=[];
 for(const p of papers)for(const id of p.datasets){const d=datasets.find(d=>d.id===id);if(!d)out.push(`paper ${p.id} lists unknown dataset ${id}`);else if(!d.papers.includes(p.id))out.push(`paper ${p.id} lists dataset ${id} but dataset ${id}.papers does not list the paper`);}
 for(const d of datasets)for(const id of d.papers){const p=papers.find(p=>p.id===id);if(!p)out.push(`dataset ${d.id} lists unknown paper ${id}`);else if(!p.datasets.includes(d.id))out.push(`dataset ${d.id} lists paper ${id} but paper ${id}.datasets does not list the dataset`);}
 return out;});

check('verified-evidence-placeholders',()=>evidence.filter(e=>e.status==='Verified'&&/needs verification|\bTODO\b|\bpending\b/i.test(e.text)).map(e=>`evidence ${e.id} is Verified but its text contains placeholder wording ("${(e.text.match(/needs verification|\bTODO\b|\bpending\b/i)||[''])[0]}")`));

for(const w of warnings){console.warn(`WARN  [${w.name}] ${w.found.length} problem(s)`);for(const m of w.found.slice(0,10))console.warn(`  - ${m}`);if(w.found.length>10)console.warn(`  ... and ${w.found.length-10} more`);}
if(problems.length){for(const w of problems){console.error(`ERROR [${w.name}] ${w.found.length} problem(s)`);for(const m of w.found.slice(0,20))console.error(`  - ${m}`);if(w.found.length>20)console.error(`  ... and ${w.found.length-20} more`);}process.exit(1);}
const synthetic=Array.from({length:200},(_,i)=>({...papers[i%papers.length],id:`qa-only-${i}`}));
const start=performance.now();for(let i=0;i<100;i++)synthetic.filter(p=>p.year>=2020&&p.techniques.includes('Transformers')).sort((a,b)=>a.year-b.year);
console.log(JSON.stringify({result:'PASS',papers:papers.length,datasets:datasets.length,authors:authors.length,resolvedAffiliations:authors.filter(a=>a.status==='Verified').length,relationships:edges.length,evidence:evidence.length,stressRecords:200,filterSort100RunsMs:Math.round(performance.now()-start)},null,2));
