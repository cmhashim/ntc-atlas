'use client';
import {papers} from '@/lib/corpus';

// Placeholder for the subscriber research outlook, which is kept out of the public corpus.
export function ResearchBriefings(){
 return <section className="panel"><div className="panel-heading"><div><span className="eyebrow">RESEARCH BRIEFINGS</span><h2>Where the field is heading</h2></div></div>
 <p className="section-note">The atlas maps what {papers.length} papers report. Research briefings add the curator&apos;s analysis on top: which directions look saturated, which gaps still lack evidence, and which experiments would test them.</p>
 <p className="section-note">Briefings will be published as a newsletter with a weekly digest of new work. Watch the <a href="https://github.com/cmhashim/ntc-atlas" target="_blank" rel="noreferrer">GitHub repository</a> for the launch.</p>
 <p className="micro muted">Briefings are curator analysis. They are kept separate from the evidence records in this atlas.</p>
 </section>;
}
