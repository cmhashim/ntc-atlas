'use client';
import { ExternalLink } from 'lucide-react';
import { Select,SelectTrigger,SelectValue,SelectContent,SelectItem } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { color, paperById, relationships } from '@/lib/corpus';
const relationByEvidence=Object.fromEntries(relationships.map(r=>[r.evidenceId,r]));
import type {Paper,Evidence} from '@/lib/schema';
export function Pick({label,value,onChange,items}:{label:string;value:string;onChange:(v:string)=>void;items:{value:string;label:string}[]}){return <label className="pick"><span>{label}</span><Select value={value} onValueChange={onChange}><SelectTrigger aria-label={label}><SelectValue/></SelectTrigger><SelectContent>{items.map(i=><SelectItem key={i.value} value={i.value}>{i.label}</SelectItem>)}</SelectContent></Select></label>;}
export function Source({url,children}:{url:string;children:React.ReactNode}){return <a className="source-link" href={url} target="_blank" rel="noreferrer">{children}<ExternalLink size={13}/></a>;}
export function Family({paper}:{paper:Paper}){return <span className="family"><i style={{background:color(paper)}}/>{paper.family}</span>;}
export function PaperLinks({ids,onOpen}:{ids:string[];onOpen:(id:string)=>void}){return <div className="paper-links">{ids.map(id=>paperById[id]&&<Button key={id} variant="outline" size="sm" onClick={()=>onOpen(id)}>{paperById[id].short}<span className="muted">{paperById[id].year}</span></Button>)}</div>;}
export function EvidenceCard({item}:{item:Evidence}){return <article className="evidence-card"><div className="between"><span className={`eyebrow ${item.category==='Later criticism'?'amber':''}`}>{item.category}</span><span className="micro muted">{item.status}</span></div>{relationByEvidence[item.id]&&(r=>paperById[r.source]&&paperById[r.target]&&<p className="micro evidence-relation">Evidence for the link <strong>{paperById[r.source].short}</strong> {r.type.toLowerCase()} <strong>{paperById[r.target].short}</strong></p>)(relationByEvidence[item.id])}<p>{item.text}</p><Source url={item.sourceUrl}>{item.sourceType} · {item.locator}</Source><div className="micro muted">Checked {item.accessed}</div></article>;}
export function Empty({title='No papers match these filters.',onReset}:{title?:string;onReset?:()=>void}){return <div className="empty"><h3>{title}</h3><p>Try a wider year range or remove a filter.</p>{onReset&&<Button variant="outline" onClick={onReset}>Reset filters</Button>}</div>;}
