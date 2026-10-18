'use client';
import { useMemo,useRef,useState,useEffect } from 'react';
import { CartesianGrid,ScatterChart,Scatter,XAxis,YAxis,Tooltip,ReferenceArea } from 'recharts';
import { ChartContainer } from '@/components/ui/chart';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { ChevronLeft,ChevronRight,Minus,Plus,RotateCcw } from 'lucide-react';
import { families,colors,familyGroup,color } from '@/lib/corpus';
import type { Filters } from '@/lib/corpus';
import type { Paper } from '@/lib/schema';

export function UnitSymbol({unit,size=14}:{unit:string;size?:number}){const burst=/burst/i.test(unit),packet=/packet/i.test(unit)&&!/flow/i.test(unit),session=/session|trace|host/i.test(unit);return <svg width={size} height={size} viewBox="-8 -8 16 16" aria-hidden>{burst?<path d="M0 -7L7 0L0 7L-7 0Z" fill="currentColor"/>:packet?<rect x="-5" y="-5" width="10" height="10" rx="1" fill="currentColor"/>:session?<path d="M0 -7L7 6L-7 6Z" fill="currentColor"/>:<circle r="5" fill="currentColor"/>}</svg>;}
export const timelineDefault:[number,number]=[2016,2026];
// The visible year window is separate from the year filter, so the other views keep every paper.
export function Timeline({papers:all,filters,setFilters,win,setWin,onOpen}:{papers:Paper[];filters:Filters;setFilters:(f:Filters)=>void;win:[number,number];setWin:(w:[number,number])=>void;onOpen:(id:string)=>void}){
 const [from,to]=win;const papers=useMemo(()=>all.filter(p=>p.year>=from&&p.year<=to),[all,from,to]);const outside=all.length-papers.length;
 const start=useRef<number|null>(null);const container=useRef<HTMLDivElement>(null);const [width,setWidth]=useState(1000);
 useEffect(()=>{if(!container.current)return;const observer=new ResizeObserver(entries=>setWidth(entries[0].contentRect.width));observer.observe(container.current);return()=>observer.disconnect();},[]);
 const rows=useMemo(()=>families.filter(f=>papers.some(p=>familyGroup(p)===f)),[papers]);
 // Pack actual label intervals into lanes; never suppress a point's name merely by year.
 const layout=useMemo(()=>{
  const plotWidth=Math.max(640,width-160),span=to-from+.9;let top=24;
  const data:(Paper&{x:number;y:number;labelLeft:boolean})[]=[];const ticks:{y:number;family:string}[]=[];
  for(const family of rows){
   const lanes:{left:number;right:number}[][]=[];
   for(const p of papers.filter(p=>familyGroup(p)===family).sort((a,b)=>a.year-b.year||a.short.localeCompare(b.short))){
    const x=(p.year-from+.35)/span*plotWidth;const labelWidth=Math.min(p.short.length,30)*7.4+20;
    const labelLeft=x+labelWidth>plotWidth;const left=labelLeft?x-labelWidth:x-9;const right=labelLeft?x+9:x+labelWidth;
    let lane=lanes.findIndex(items=>items.every(b=>right+10<b.left||left>b.right+10));if(lane<0){lane=lanes.length;lanes.push([]);}lanes[lane].push({left,right});
    data.push({...p,x:p.year,y:top+lane*30,labelLeft});
   }
   ticks.push({y:top+Math.max(0,lanes.length-1)*15,family});top+=Math.max(64,lanes.length*30+24);
  }
  return {data,ticks,height:Math.max(250,top)};
 },[papers,rows,from,to,width]);
 function range(a:number,b:number){const width=Math.max(1,b-a);const left=Math.max(2004,Math.min(2026-width,a));setWin([Math.round(left),Math.round(Math.min(2026,left+width))]);}
 function zoom(delta:number){const width=Math.max(2,Math.min(22,to-from+delta));const mid=(from+to)/2;range(mid-width/2,mid+width/2);}
 const shortLabel=(name:string)=>name==='Rules & statistics'?'Rules / statistics':name==='Evaluation & surveys'?'Evaluation':name==='Masked autoencoder'?'Autoencoders':name;
 return <section className="panel timeline-panel" aria-label="Publication timeline">
  <div className="panel-heading"><div><span className="eyebrow">01 / CHRONOLOGY</span><h2>Follow the field’s evolution</h2></div><label className="inline-control"><Switch checked={filters.seminal} onCheckedChange={seminal=>setFilters({...filters,seminal})} aria-label="Seminal papers only"/>Seminal papers</label></div>
  <div className="timeline-toolbar"><span className="mono">{from} — {to}</span><span className="muted micro grow">Publication year · select a mark to inspect evidence{outside>0&&<> · {outside} {outside===1?'paper':'papers'} outside this window</>}</span><Button variant="ghost" size="icon" aria-label="Pan timeline earlier" onClick={()=>range(from-2,to-2)}><ChevronLeft/></Button><Button variant="ghost" size="icon" aria-label="Pan timeline later" onClick={()=>range(from+2,to+2)}><ChevronRight/></Button><Button variant="outline" size="icon" aria-label="Zoom timeline in" onClick={()=>zoom(-6)}><Plus/></Button><Button variant="outline" size="icon" aria-label="Zoom timeline out" onClick={()=>zoom(6)}><Minus/></Button><Button variant="ghost" size="icon" aria-label="Reset timeline range" onClick={()=>setWin(timelineDefault)}><RotateCcw size={15}/></Button></div>
  <div ref={container} className="timeline-scroll" onPointerDown={e=>{if(!(e.target as Element).closest('[role=button]'))start.current=e.clientX;}} onPointerUp={e=>{if(start.current!==null&&Math.abs(e.clientX-start.current)>70){const delta=Math.round((start.current-e.clientX)/80);range(from+delta,to+delta);}start.current=null;}}>
   <ChartContainer config={Object.fromEntries(families.map((f,i)=>['f'+i,{label:f,color:colors[f]}]))} className="timeline-chart" style={{height:layout.height+50}}>
    <ScatterChart margin={{top:23,right:28,bottom:8,left:6}} accessibilityLayer>
     <CartesianGrid horizontal={true} vertical={true} stroke="var(--border)" strokeDasharray="3 6"/>
     <XAxis type="number" dataKey="x" domain={[from-.35,to+.55]} ticks={Array.from({length:to-from+1},(_,i)=>from+i).filter((v,i)=>to-from<10||i%2===0)} tick={{fontSize:12}} tickLine={false} axisLine={false}/>
     <YAxis type="number" dataKey="y" domain={[0,layout.height]} ticks={layout.ticks.map(t=>t.y)} tickFormatter={v=>shortLabel(layout.ticks.find(t=>t.y===v)?.family||'')} reversed width={126} tick={{fontSize:12}} tickLine={false} axisLine={false}/>
     <ReferenceArea x1={2022} x2={Math.min(to+.55,2026.55)} fill="#45d6c3" fillOpacity={.025}/>
     <Tooltip cursor={false} content={({active,payload})=>{const p=payload?.[0]?.payload as Paper|undefined;return active&&p?<div className="chart-tooltip"><b>{p.short} · {p.year}</b><span>{p.venue}</span><span>{p.unit} · {p.family}</span></div>:null;}}/>
     <Scatter data={layout.data} isAnimationActive={false} shape={(props:unknown)=>{const {cx,cy,payload}=props as {cx:number;cy:number;payload:Paper&{labelLeft:boolean}};return <g role="button" aria-label={`Open ${payload.short}, ${payload.year}`} tabIndex={0} onClick={()=>onOpen(payload.id)} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onOpen(payload.id);}}} className="timeline-mark" transform={`translate(${cx},${cy})`}><rect x={payload.labelLeft?-Math.min(payload.short.length,30)*7.4-20:-13} y="-18" width={Math.min(payload.short.length,30)*7.4+33} height="28" fill="transparent" pointerEvents="all"/><circle r="13" fill="transparent"/><g transform="translate(-7,-7)" style={{color:color(payload)}}><UnitSymbol unit={payload.unit}/></g><text x={payload.labelLeft?-12:12} textAnchor={payload.labelLeft?'end':'start'} y={4} fill="var(--foreground)" fontSize="13" fontWeight={payload.seminal?600:400}>{payload.short.length>30?payload.short.slice(0,29)+'…':payload.short}</text></g>;}}/>
    </ScatterChart>
   </ChartContainer>
  </div>
  <div className="range-control"><span className="micro">2004</span><Slider aria-label="Publication year range" min={2004} max={2026} step={1} minStepsBetweenThumbs={1} value={[from,to]} onValueChange={v=>setWin([v[0],v[1]])}/><span className="micro">2026</span></div>
  <div className="legend"><span className="micro muted">INPUT UNIT</span>{['Packet','Burst','Flow','Session / trace / host'].map(v=><span key={v}><UnitSymbol unit={v}/>{v}</span>)}<span className="micro muted">Mixed packet / flow uses a circle. Colour = model family.</span></div>
 </section>;
}
