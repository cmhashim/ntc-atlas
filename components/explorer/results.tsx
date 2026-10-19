'use client';
import {useEffect,useMemo,useState} from 'react';
import {Switch} from '@/components/ui/switch';
import {Badge} from '@/components/ui/badge';
import {Table,TableHeader,TableHead,TableBody,TableRow,TableCell} from '@/components/ui/table';
import {Pick,Source} from './common';
import {datasetById,paperById} from '@/lib/corpus';
import {withBase} from '@/lib/base-path';
import {groupResults,type ResultGroup} from '@/lib/results';
import type {Paper,Result} from '@/lib/schema';

const METRICS=['F1','accuracy','precision','recall','AUROC'];
const fmt=(v:number)=>v.toFixed(2);

function GroupTable({group,onOpen}:{group:ResultGroup;onOpen:(id:string)=>void}){
 return <div className="results-table"><Table><TableHeader><TableRow><TableHead>Model</TableHead><TableHead>Paper</TableHead><TableHead className="results-value">Value</TableHead><TableHead>Split</TableHead><TableHead>Source</TableHead></TableRow></TableHeader>
 <TableBody>{group.rows.map(r=>{const p=paperById[r.paper];return <TableRow key={r.id}>
  <TableCell><span title={r.quote}>{r.model}</span>{r.role!=='own method'&&<Badge variant="outline" className="results-role">evaluated by</Badge>}{r.setting&&<div className="micro muted">{r.setting}</div>}</TableCell>
  <TableCell><button className="text-button" onClick={()=>onOpen(r.paper)}>{p.short} <span className="muted">{p.year}</span></button></TableCell>
  <TableCell className="results-value">{fmt(r.value)}</TableCell>
  <TableCell className="micro">{r.split??'not stated'}</TableCell>
  <TableCell><Source url={r.sourceUrl}>{r.locator}</Source></TableCell>
 </TableRow>;})}</TableBody></Table></div>;
}

function GroupHead({group}:{group:ResultGroup}){
 const setting=group.settingClass.replace(/^specific: /,'');
 return <><h3>{group.tasks.join(' / ')}</h3><p className="micro muted">{group.classes} classes · {group.splitUnit} split · {group.metric}{group.averaging?` (${group.averaging})`:''} · {setting} · {group.papers} {group.papers===1?'paper':'papers'}</p></>;
}

export function ResultsView({papers,onOpen}:{papers:Paper[];onOpen:(id:string)=>void}){
 const [rows,setRows]=useState<Result[]|null>(null);const [error,setError]=useState(false);
 const [dataset,setDataset]=useState('iscxvpn');const [metric,setMetric]=useState('F1');const [ownOnly,setOwnOnly]=useState(false);
 useEffect(()=>{let live=true;fetch(withBase('/data/results.json')).then(r=>{if(!r.ok)throw new Error(String(r.status));return r.json();}).then(d=>{if(live)setRows(d);}).catch(()=>{if(live)setError(true);});return()=>{live=false;};},[]);
 const visible=useMemo(()=>{const ids=new Set(papers.map(p=>p.id));return (rows??[]).filter(r=>ids.has(r.paper)&&(!ownOnly||r.role==='own method'));},[rows,papers,ownOnly]);
 const datasetItems=useMemo(()=>{const n=new Map<string,number>();for(const r of visible)n.set(r.dataset,(n.get(r.dataset)??0)+1);return [...n.entries()].sort((a,b)=>b[1]-a[1]).map(([id,c])=>({value:id,label:`${datasetById[id]?.name??id} (${c})`}));},[visible]);
 const chosen=datasetItems.some(d=>d.value===dataset)?dataset:datasetItems[0]?.value;
 const {groups,apart}=useMemo(()=>groupResults(visible.filter(r=>r.dataset===chosen&&r.metric===metric)),[visible,chosen,metric]);
 const shared=groups.filter(g=>g.papers>1),single=groups.filter(g=>g.papers===1);
 return <section className="panel results-panel"><div className="panel-heading"><div><span className="eyebrow">COMPARABLE RESULTS</span><h2>Reported results that can be compared</h2>
  <p className="micro muted">Results are grouped only when dataset, class count, split unit, metric, averaging and setting all match. Values are as reported by each paper, not reproduced.</p></div>
  <div className="paper-table-controls">{datasetItems.length>0&&chosen&&<Pick label="Dataset" value={chosen} onChange={setDataset} items={datasetItems}/>}<Pick label="Metric" value={metric} onChange={setMetric} items={METRICS.map(m=>({value:m,label:m}))}/><label className="inline-control"><Switch checked={ownOnly} onCheckedChange={setOwnOnly}/>Own methods only</label></div></div>
  {error&&<p className="notice">The results file could not be loaded.</p>}
  {!rows&&!error&&<p className="muted">Loading results…</p>}
  {rows&&!error&&<>
   <p className="section-note">{shared.length} {shared.length===1?'group compares':'groups compare'} results from two or more papers; {single.length} {single.length===1?'group has':'groups have'} results from one paper; {apart.length} {apart.length===1?'result is':'results are'} not comparable.</p>
   {shared.length===0&&<p className="muted">No group with results from two or more papers for this dataset and metric.</p>}
   {shared.map(g=><article key={g.key} className="results-group"><GroupHead group={g}/><GroupTable group={g} onOpen={onOpen}/></article>)}
   {single.length>0&&<details className="results-more"><summary>Results from a single paper ({single.length} groups)</summary>{single.map(g=><article key={g.key} className="results-group"><GroupHead group={g}/><GroupTable group={g} onOpen={onOpen}/></article>)}</details>}
   {apart.length>0&&<details className="results-more"><summary>Not comparable ({apart.length})</summary><div className="results-table"><Table><TableHeader><TableRow><TableHead>Model</TableHead><TableHead>Paper</TableHead><TableHead>Task</TableHead><TableHead className="results-value">Value</TableHead><TableHead>Why</TableHead><TableHead>Source</TableHead></TableRow></TableHeader>
    <TableBody>{apart.map(({row:r,reasons})=><TableRow key={r.id}><TableCell><span title={r.quote}>{r.model}</span>{r.setting&&<div className="micro muted">{r.setting}</div>}</TableCell><TableCell><button className="text-button" onClick={()=>onOpen(r.paper)}>{paperById[r.paper].short}</button></TableCell><TableCell className="micro">{r.task}</TableCell><TableCell className="results-value">{fmt(r.value)}</TableCell><TableCell className="micro">{reasons.join('; ')}</TableCell><TableCell><Source url={r.sourceUrl}>{r.locator}</Source></TableCell></TableRow>)}</TableBody></Table></div></details>}
  </>}
 </section>;
}
