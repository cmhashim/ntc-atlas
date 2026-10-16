import type {Evidence,Relationship} from './schema';

const inverseLabels:Record<string,string>={'Compares against':'Compared against by','Uses dataset from':'Dataset used by','Uses preprocessing of':'Preprocessing reused by','Uses implementation of':'Implementation reused by','Reproduces':'Reproduced by','Extends':'Extended by','Builds on':'Built on by','Diagnoses':'Diagnosed by','Criticises':'Criticised by','Audits label provenance':'Label provenance audited by','Follows':'Followed by','Cites methodological evidence':'Cited as methodological evidence by','Related representation':'Related representation','Complementary approach':'Complementary approach'};
const critiqueTypes=new Set(['Criticises','Diagnoses','Audits label provenance']);
interface EvidenceLineGroup {items:Evidence[];paperIds:string[];}
interface EvidenceRow {key:string;label:string|null;lines:EvidenceLineGroup[];}
interface EvidenceSection {id:string;title:string;rows:EvidenceRow[];}

// Keep all source records in merged lines so counts and verification stay accurate.
export function groupPaperEvidence(paperId:string,records:Evidence[],relations:Relationship[]){
 const byId=new Map(records.map(e=>[e.id,e]));
 const relationshipIds=new Set(relations.map(r=>r.evidenceId));
 const own=records.filter(e=>e.paperId===paperId&&!relationshipIds.has(e.id));
 const sections:EvidenceSection[]=[];
 function addRecords(id:string,title:string,categories:string[]){
  const items=categories.flatMap(category=>own.filter(e=>e.category===category));
  if(items.length)sections.push({id,title,rows:[{key:id,label:null,lines:items.map(item=>({items:[item],paperIds:[]}))}]});
 }
 function addLinks(id:string,title:string,criticism:boolean){
  const rows=new Map<string,EvidenceRow>();
  for(const relation of relations){
   if(relation.source!==paperId&&relation.target!==paperId)continue;
   const item=byId.get(relation.evidenceId);
   const outgoing=relation.source===paperId;
   // Criticism received goes to its own section; a critic's own audits stay with its links.
   if(!item||item.category==='Bibliography'||(!outgoing&&critiqueTypes.has(relation.type))!==criticism)continue;
   const key=JSON.stringify([outgoing,relation.type]);
   let row=rows.get(key);
   if(!row){row={key,label:outgoing?relation.type:inverseLabels[relation.type]||relation.type,lines:[]};rows.set(key,row);}
   let line=row.lines.find(line=>line.items[0].text===item.text&&line.items[0].sourceUrl===item.sourceUrl&&line.items[0].locator===item.locator);
   if(!line){line={items:[],paperIds:[]};row.lines.push(line);}
   if(!line.items.some(e=>e.id===item.id))line.items.push(item);
   const otherId=outgoing?relation.target:relation.source;
   if(!line.paperIds.includes(otherId))line.paperIds.push(otherId);
  }
  const existing=sections.find(section=>section.id===id);
  if(existing)existing.rows.push(...rows.values());
  else if(rows.size)sections.push({id,title,rows:[...rows.values()]});
 }
 addRecords('reports','What the paper reports',['Author-reported result','Paper claim']);
 addLinks('links','Links to other papers',false);
 addRecords('criticism','Later criticism',['Later criticism']);
 addLinks('criticism','Later criticism',true);
 addRecords('artifacts','Artifacts and datasets',['Artifact availability','Dataset documentation']);
 addRecords('curator','Curator’s interpretation',['Curator interpretation']);
 const shown=new Map(sections.flatMap(s=>s.rows.flatMap(r=>r.lines.flatMap(l=>l.items.map(e=>[e.id,e] as const)))));
 return {sections,total:shown.size,verified:[...shown.values()].filter(e=>e.status==='Verified').length,needsVerification:[...shown.values()].filter(e=>e.status==='Needs verification').length};
}
