import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

const root=path.resolve(import.meta.dirname,'..'),out=path.join(root,'out'),origin='https://ntc-atlas.pages.dev';
const read=name=>JSON.parse(fs.readFileSync(path.join(root,'public/data',`${name}.json`),'utf8'));
const papers=read('papers'),datasets=read('datasets'),authors=read('authors'),evidence=read('evidence'),relations=read('relationships'),meta=read('meta');
const cff=fs.readFileSync(path.join(root,'CITATION.cff'),'utf8');
const citation=key=>JSON.parse(cff.match(new RegExp(`^${key}: (".*")$`,'m'))[1]);
const abstract=citation('abstract'),citationTitle=citation('title');
const paperById=new Map(papers.map(p=>[p.id,p])),authorByName=new Map(authors.map(a=>[a.name,a])),evidenceById=new Map(evidence.map(e=>[e.id,e]));
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const json=value=>JSON.stringify(value).replace(/</g,'\\u003c').replace(/>/g,'\\u003e').replace(/&/g,'\\u0026');
const oneLine=value=>String(value??'').replace(/\s+/g,' ').trim();
const description=value=>{const s=oneLine(value);return s.length<=160?s:s.slice(0,161).replace(/\s+\S*$/,'').slice(0,160);};
const route=(type,id)=>`/${type}/${encodeURIComponent(id)}/`;
const link=(url,label)=>`<a href="${esc(url)}">${esc(label)}</a>`;
const list=items=>`<ul>${items.map(item=>`<li>${item}</li>`).join('')}</ul>`;
const section=(title,body,cls='')=>body?`<section${cls?` class="${cls}"`:''}><h2>${esc(title)}</h2>${body}</section>`:'';
const fields=entries=>`<dl>${entries.filter(([,v])=>v!==null&&v!==undefined&&v!=='').map(([k,v])=>`<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>`;
const paperLink=id=>{const p=paperById.get(id);assert(p,`Unknown paper ${id}`);return link(route('paper',id),`${p.short} (${p.year}) · ${p.title}`);};
const atlas={'@type':'Dataset','@id':`${origin}/#dataset`,name:'NTC Atlas',url:origin+'/',license:'https://creativecommons.org/licenses/by/4.0/'};
const style=`*{box-sizing:border-box}body{margin:0;background:#f4efe4;color:#1f2933;font:18px/1.65 "Source Sans 3",system-ui,sans-serif;overflow-wrap:anywhere}header,main,footer{max-width:792px;margin:auto;padding:20px 16px}header{display:flex;justify-content:space-between;gap:16px;border-bottom:1px solid #dbd1bd}main{padding-top:28px}h1,h2,h3{font-family:"Source Serif 4",Georgia,serif;line-height:1.2}h1{font-size:2rem}@media(max-width:600px){h1{font-size:1.45rem}}h2{font-size:1.5rem}h3{font-size:1.15rem}a{color:#23477a}section{background:#fbf8f1;border:1px solid #dbd1bd;padding:16px;margin:24px 0;border-radius:4px}dt{font-weight:600}dd{margin:0 0 12px}ul{padding-left:24px}li{margin:12px 0}.muted,footer{color:#665e50;font-size:1rem}.criticism{border-left:4px solid #9a3b2a}.criticism h2{color:#9a3b2a}.interactive{display:inline-block;padding:10px 14px;background:#fbf8f1;border:1px solid #23477a;border-radius:4px;font-weight:600}footer{border-top:1px solid #dbd1bd}`;
const written=['/'];
function writePage(url,title,summary,body,schema){
 const canonical=origin+url,desc=description(summary);
 const html=`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(title)} · NTC Atlas</title><meta name="description" content="${esc(desc)}"><link rel="canonical" href="${esc(canonical)}"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&amp;family=Source+Serif+4:wght@400;600&amp;display=swap"><meta property="og:title" content="${esc(title)} · NTC Atlas"><meta property="og:description" content="${esc(desc)}"><meta property="og:url" content="${esc(canonical)}"><meta property="og:site_name" content="NTC Atlas"><meta property="og:type" content="website"><meta property="og:image" content="${origin}/preview.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="${esc(title)} · NTC Atlas"><meta name="twitter:description" content="${esc(desc)}"><meta name="twitter:image" content="${origin}/preview.jpg"><style>${style}</style><script type="application/ld+json">${json({'@context':'https://schema.org',url:canonical,name:title,...schema})}</script></head><body><header>${link('/','NTC Atlas')}${link('/papers/','All papers')}</header><main>${body}</main><footer>Updated ${esc(meta.updated)} · ${link('https://github.com/cmhashim/ntc-atlas','Source repository')} · Code MIT · Data ${link('https://creativecommons.org/licenses/by/4.0/','CC BY 4.0')}</footer></body></html>\n`;
 const target=path.join(out,url,'index.html');fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,html);written.push(url);
}
const critiqueTypes=new Set(['Criticises','Diagnoses','Audits label provenance']);
const inverseLabels={'Compares against':'Compared against by','Uses dataset from':'Dataset used by','Uses preprocessing of':'Preprocessing reused by','Uses implementation of':'Implementation reused by','Reproduces':'Reproduced by','Extends':'Extended by','Builds on':'Built on by','Diagnoses':'Diagnosed by','Criticises':'Criticised by','Audits label provenance':'Label provenance audited by','Follows':'Followed by','Cites methodological evidence':'Cited as methodological evidence by','Related representation':'Related representation','Complementary approach':'Complementary approach'};
const evidenceItem=e=>`<p><strong>${esc(e.category)}</strong>: ${esc(e.text)}</p><p class="muted">${link(e.sourceUrl,e.sourceType)} · ${esc(e.locator)} · ${esc(e.status)} · Accessed ${esc(e.accessed)}</p>`;
// Mirror lib/evidence.ts: exclude relationship records from own evidence, merge identical
// relationship lines, and keep incoming criticism separate from a critic's outgoing links.
function paperEvidence(id){
 const relationshipIds=new Set(relations.map(r=>r.evidenceId)),own=evidence.filter(e=>e.paperId===id&&!relationshipIds.has(e.id));
 const records=categories=>categories.flatMap(c=>own.filter(e=>e.category===c));
 const recordList=items=>items.length?list(items.map(evidenceItem)):'';
 function links(criticism){
  const rows=new Map();
  for(const r of relations){
   if(r.source!==id&&r.target!==id)continue;
   const e=evidenceById.get(r.evidenceId),outgoing=r.source===id;
   if(!e||e.category==='Bibliography'||(!outgoing&&critiqueTypes.has(r.type))!==criticism)continue;
   const label=outgoing?r.type:inverseLabels[r.type]||r.type,key=JSON.stringify([outgoing,r.type]);
   if(!rows.has(key))rows.set(key,{label,lines:new Map()});
   const lines=rows.get(key).lines,lineKey=JSON.stringify([e.text,e.sourceUrl,e.locator]);
   if(!lines.has(lineKey))lines.set(lineKey,{e,ids:new Set()});
   lines.get(lineKey).ids.add(outgoing?r.target:r.source);
  }
  return [...rows.values()].map(row=>`<h3>${esc(row.label)}</h3>${list([...row.lines.values()].map(({e,ids})=>evidenceItem(e)+list([...ids].map(paperLink))))}`).join('');
 }
 return section('What the paper reports',recordList(records(['Author-reported result','Paper claim'])))+section('Links to other papers',links(false))+section('Later criticism',recordList(records(['Later criticism']))+links(true),'criticism')+section('Artifacts and datasets',recordList(records(['Artifact availability','Dataset documentation'])))+section('Curator’s interpretation',recordList(records(['Curator interpretation'])));
}
for(const p of papers){
 const people=p.authors.map(name=>{const a=authorByName.get(name);return a?link(route('author',a.id),name):esc(name);}).join(', ');
 const relationships=relations.filter(r=>r.source===p.id||r.target===p.id);
 const body=`<h1>${esc(p.title)}</h1><p>${esc(p.short)} (${esc(p.year)})</p><p>${people}</p><p class="interactive">${link(`/?paper=${encodeURIComponent(p.id)}`,'Open in the interactive atlas')}</p>${fields([['Year',p.year],['Venue',p.venue],['Publication status',p.publicationStatus],['Review depth',p.reviewDepth]])}<p>${link(p.url,'Original paper')}${p.code?` · ${link(p.code,'Code')}`:''}</p>`+section('Summary',`<p>${esc(p.summary)}</p>`)+section('Contribution',`<p>${esc(p.contribution)}</p>`)+section('Curator interpretation',`<p>${esc(p.limitation)}</p>`)+section('Open question',`<p>${esc(p.gap)}</p>`)+section('Comparison fields',fields(Object.entries(p.details).filter(([,v])=>!String(v).startsWith('NA'))))+section('Datasets',p.datasets.length?list(p.datasets.map(id=>link(route('dataset',id),datasets.find(d=>d.id===id).name))):'')+section('Relationships',relationships.length?list(relationships.map(r=>`${paperLink(r.source)} → <strong>${esc(r.type)}</strong> → ${paperLink(r.target)}<p>${esc(r.explanation)}</p>`)):'')+paperEvidence(p.id);
 writePage(route('paper',p.id),`${p.short} (${p.year})`,p.summary,body,{'@type':'WebPage',about:{'@type':'ScholarlyArticle',name:p.title,author:p.authors.map(name=>({'@type':'Person',name})),datePublished:String(p.year),url:p.url,sameAs:p.url,isPartOf:atlas}});
}
for(const d of datasets){
 const refs=[d.evidence,...(d.caveatEvidence||[])].filter(Boolean);
 const body=`<h1>${esc(d.name)}</h1><p class="interactive">${link(`/?view=datasets&collection=${encodeURIComponent(d.id)}`,'Open in the interactive atlas')}</p><p>${link(d.url,'Original dataset')}</p>${d.introducedBy?(()=>{const x=d.introducedBy,ev=evidenceById.get(x.evidence);return `<p>Introduced by ${x.paper?paperLink(x.paper):esc(x.citation)} (${link(ev.sourceUrl,ev.locator)})</p>`;})():''}`+section('Dataset fields',fields(['year','environment','classes','encrypted','units','size','labels','preprocessing','status'].map(k=>[k[0].toUpperCase()+k.slice(1),d[k]])))+section('Caveats',`<p>${esc(d.caveats)}</p>`)+section('Papers using this dataset',list(d.papers.map(paperLink)))+section('Evidence',refs.length?list([...new Set(refs)].map(id=>{assert(evidenceById.has(id));return evidenceItem(evidenceById.get(id));})): '');
 writePage(route('dataset',d.id),`${d.name} (${d.year})`,d.environment,body,{'@type':'WebPage',about:{'@type':'Dataset',name:d.name,description:d.environment,url:d.url,sameAs:d.url,datePublished:String(d.year)}});
}
for(const a of authors){
 const affiliation=a.status==='Verified'?a.affiliation:undefined;
 const body=`<h1>${esc(a.name)}</h1>${affiliation?`<p>${esc(affiliation)}</p>`:''}<p class="interactive">${link(`/?view=authors&person=${encodeURIComponent(a.id)}`,'Open in the interactive atlas')}</p>`+section('Papers',list(a.papers.map(paperLink)));
 writePage(route('author',a.id),a.name,a.contribution,body,{'@type':'ProfilePage',about:{'@type':'Person',name:a.name,...(affiliation?{affiliation:{'@type':'Organization',name:affiliation}}:{})}});
}
const years=[...new Set(papers.map(p=>p.year))].sort((a,b)=>b-a);
writePage('/papers/','All papers, datasets and authors',abstract,`<h1>All papers, datasets and authors</h1><p>${esc(meta.scope)}</p>`+years.map(year=>section(String(year),list(papers.filter(p=>p.year===year).map(p=>paperLink(p.id))))).join('')+section('Datasets',list(datasets.map(d=>link(route('dataset',d.id),d.name))))+section('Authors',list(authors.map(a=>link(route('author',a.id),a.name)))),{'@type':'CollectionPage',about:atlas});
const sitemap=`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${written.map(url=>`<url><loc>${esc(origin+url)}</loc><lastmod>${esc(meta.updated)}</lastmod></url>`).join('')}</urlset>\n`;
fs.writeFileSync(path.join(out,'sitemap.xml'),sitemap);
const dataNames=['papers','datasets','evidence','relationships','authors','meta'];
const md=value=>oneLine(value).replace(/[\\[\]<>]/g,'\\$&');
fs.writeFileSync(path.join(out,'llms.txt'),`# NTC Atlas\n\n> ${abstract} ${meta.scope}\n\n## Citation\n\n${citation('message')}\n\nMohamed Hashim Changrampadi. ${citationTitle}. Chalmers University of Technology. ${origin}/. ORCID: https://orcid.org/0000-0003-1852-0998.\n\n- [Citation metadata](https://github.com/cmhashim/ntc-atlas/blob/main/CITATION.cff)\n\n## Licence\n\nCode: MIT. Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).\n\n## Index\n\n- [All papers, datasets and authors](${origin}/papers/)\n\n## JSON data\n\n${dataNames.map(name=>`- [${name}.json](${origin}/data/${name}.json)`).join('\n')}\n\n## Papers\n\n${[...papers].sort((a,b)=>b.year-a.year).map(p=>`- [${md(p.short)} (${p.year})](${origin}${route('paper',p.id)}): ${md(p.summary)}`).join('\n')}\n`);
// Check the actual files (including vinext's home page), not just the page template.
for(const url of written){
 const html=fs.readFileSync(path.join(out,url,'index.html'),'utf8');
 const canonical=html.match(/<link\b[^>]*\brel="canonical"[^>]*>/g)||[];
 assert.equal(canonical.length,1,`Missing or duplicate canonical: ${url}`);
 assert(canonical[0].includes(`href="${origin+url}"`),`Incorrect canonical: ${url}`);
}
const sitemapUrls=[...fs.readFileSync(path.join(out,'sitemap.xml'),'utf8').matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>m[1]);
assert.equal(sitemapUrls.length,written.length,'Sitemap URL count differs from pages written');
assert.deepEqual(new Set(sitemapUrls),new Set(written.map(url=>origin+url)),'Sitemap URLs differ from pages written');
console.log(`SEO: generated ${written.length-1} HTML pages (${papers.length} papers, ${datasets.length} datasets, ${authors.length} authors, 1 index); validated ${written.length} canonicals and sitemap URLs.`);
