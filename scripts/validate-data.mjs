import fs from 'node:fs';
import assert from 'node:assert/strict';
const read=n=>JSON.parse(fs.readFileSync(new URL(`../public/data/${n}.json`,import.meta.url)));
const papers=read('papers'),authors=read('authors'),datasets=read('datasets'),evidence=read('evidence'),edges=read('relationships'),meta=read('meta');
const unique=(arr,key)=>{assert.equal(new Set(arr.map(x=>x[key])).size,arr.length,`Duplicate ${key}`);};
for(const arr of [papers,authors,datasets,evidence,edges])unique(arr,'id');
unique(papers,'url');unique(papers,'title');unique(authors,'name');
const ids=new Set(papers.map(p=>p.id)),eids=new Set(evidence.map(e=>e.id)),dids=new Set(datasets.map(d=>d.id));
for(const p of papers){
 assert(p.year>=2004&&p.year<=2026);assert(p.authors.length);assert(/^https:\/\//.test(p.url));
 assert.equal(Object.keys(p.gaps).length,16);assert(p.evidenceIds.length>=3);
 for(const id of p.datasets)assert(dids.has(id),`Unknown dataset ${id}`);
 for(const id of p.evidenceIds)assert(eids.has(id));
 for(const [field,id] of Object.entries(p.fieldEvidence||{})){assert(field in p.details);assert(eids.has(id));}
 for(const g of Object.values(p.gaps)){assert(['Addressed','Partially addressed','Not addressed/not reported'].includes(g.state));assert(g.note);assert(g.evidence.length);for(const id of g.evidence)assert(eids.has(id));}
 for(const name of p.authors)assert(authors.some(a=>a.name===name&&a.papers.includes(p.id)),`Missing author ${name}`);
}
for(const a of authors){assert(a.papers.length,`Author without a relevant publication: ${a.name}`);for(const id of a.papers)assert(papers.some(p=>p.id===id&&p.authors.includes(a.name)),`Unsupported authorship: ${a.name}`);}
for(const d of datasets)for(const id of d.papers){assert(ids.has(id));assert(papers.find(p=>p.id===id).datasets.includes(d.id));}
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
const synthetic=Array.from({length:200},(_,i)=>({...papers[i%papers.length],id:`qa-only-${i}`}));
const start=performance.now();for(let i=0;i<100;i++)synthetic.filter(p=>p.year>=2020&&p.techniques.includes('Transformers')).sort((a,b)=>a.year-b.year);
console.log(JSON.stringify({result:'PASS',papers:papers.length,datasets:datasets.length,authors:authors.length,resolvedAffiliations:authors.filter(a=>a.status==='Verified').length,relationships:edges.length,evidence:evidence.length,stressRecords:200,filterSort100RunsMs:Math.round(performance.now()-start)},null,2));
