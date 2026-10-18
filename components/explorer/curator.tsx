'use client';
import {useState} from 'react';
import {GraduationCap,Quote,Copy,Check} from 'lucide-react';
import {Button} from '@/components/ui/button';
import {Tooltip,TooltipTrigger,TooltipContent} from '@/components/ui/tooltip';
import {Dialog,DialogContent,DialogDescription,DialogHeader,DialogTitle,DialogTrigger} from '@/components/ui/dialog';

const GITHUB='https://github.com/cmhashim';
const LINKEDIN='https://www.linkedin.com/in/cmhashim/';
const CHALMERS='https://www.chalmers.se/en/persons/hashimm';
const YEAR='2026';
const TITLE='NTC Atlas: an interactive, evidence-backed atlas of network traffic classification research';
const citations:[string,string][]=[
 ['APA',`Changrampadi, M. H. (${YEAR}). ${TITLE} [Data set]. https://ntc-atlas.pages.dev`],
 ['BibTeX',`@misc{changrampadi${YEAR}ntcatlas,\n  author       = {Changrampadi, Mohamed Hashim},\n  title        = {{NTC Atlas}: an interactive, evidence-backed atlas of network traffic classification research},\n  year         = {${YEAR}},\n  howpublished = {\\url{https://ntc-atlas.pages.dev}},\n  note         = {Code and data: \\url{https://github.com/cmhashim/ntc-atlas}}\n}`],
];

function GithubMark(){return <svg viewBox="0 0 24 24" width={17} height={17} fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>;}
function LinkedinMark(){return <svg viewBox="0 0 24 24" width={16} height={16} fill="currentColor" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.064 2.064 0 1 1 0-4.128 2.064 2.064 0 0 1 0 4.128zM7.119 20.452H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>;}

function IconLink({href,label,children}:{href:string;label:string;children:React.ReactNode}){return <Tooltip><TooltipTrigger asChild><Button asChild variant="ghost" size="icon"><a href={href} target="_blank" rel="noreferrer" aria-label={label}>{children}</a></Button></TooltipTrigger><TooltipContent>{label}</TooltipContent></Tooltip>;}

function CitationBlock({label,text}:{label:string;text:string}){const [copied,setCopied]=useState(false);
 async function copy(){try{await navigator.clipboard.writeText(text);setCopied(true);setTimeout(()=>setCopied(false),2000);}catch{window.prompt(`Copy the ${label} citation`,text);}}
 return <div className="cite-block"><div className="between"><strong>{label}</strong><Button variant="outline" size="sm" onClick={copy} aria-label={`Copy ${label} citation`}>{copied?<Check size={14}/>:<Copy size={14}/>}<span>{copied?'Copied':'Copy'}</span></Button></div><pre className="bibtex">{text}</pre></div>;}

export function CuratorLinks(){return <>
 <IconLink href={GITHUB} label="GitHub"><GithubMark/></IconLink>
 {LINKEDIN&&<IconLink href={LINKEDIN} label="LinkedIn"><LinkedinMark/></IconLink>}
 <IconLink href={CHALMERS} label="Chalmers profile"><GraduationCap size={18}/></IconLink>
 <Dialog><Tooltip><TooltipTrigger asChild><DialogTrigger asChild><Button variant="ghost" size="icon" aria-label="Cite NTC Atlas"><Quote size={17}/></Button></DialogTrigger></TooltipTrigger><TooltipContent>Cite</TooltipContent></Tooltip>
  <DialogContent className="cite-dialog"><DialogHeader><DialogTitle>Cite NTC Atlas</DialogTitle><DialogDescription>If you use the atlas or its data, please cite it. Please also cite the original papers for any result you take from the atlas.</DialogDescription></DialogHeader>{citations.map(([l,t])=><CitationBlock key={l} label={l} text={t}/>)}</DialogContent></Dialog>
</>;}
