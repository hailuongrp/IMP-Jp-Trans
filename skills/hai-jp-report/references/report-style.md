# Japanese style for IMP/EE

Use the user's approved template first. Otherwise use restrained professional report prose, normally である体, with consistent terminology and natural Japanese collocations. Make the actor, object and consequence easy to identify without inventing missing actors.

Keep approved headings and section order. Within a paragraph, clarify the argument using information already present. Do not add an executive summary, a new recommendation, a new rationale or a new example merely to make the document look complete. A translation request is not authorization to redesign the report.

Break overloaded sentences where useful; retain every condition, exception and causal qualification. Do not shorten solely to meet a character target. Prefer ordinary clear words to unexplained katakana and chains of abstract nouns. Preserve technical precision and established legal names rather than forcing all terminology into casual Japanese.

A negative business recommendation should remain clear. Do not turn it into diplomatic optimism. Conversely, a limited evidence gap should not become an absolute rejection. Headings and tables must keep the same degree of certainty as the body, not rely on a buried footnote to repair an overstatement.

## Glossary handling

Load a user-approved project glossary when supplied. Otherwise use context-consistent translations and keep a working glossary for this run. `glossary-seed.tsv` contains PROPOSED suggestions only; it is not a set of user-approved business labels. Keep distinct concepts distinct and do not blindly replace substrings.

Preserve IMP, EE, product names, source identifiers and machine statuses unless an approved mapping is given. A reader-facing Japanese explanation may accompany a code only when its meaning is established. Do not invent what IMP/EE or any internal acronym stands for.

## Artifact handling

For Markdown/text, retain section anchors, links, table alignment and note relationships. For HTML or structured files, translate reader-visible content only; do not rewrite IDs, class names, scripts, URLs, JSON keys or machine values. When images or PDF pages contain report text, inspect them with the host's document tools; do not pretend the text extractor covered them.

For Word/PDF/slide output use the host's appropriate format workflow and inspect the exported result when available. Ensure the requested report is complete, including tables and appendices. A plain-text screening script cannot certify page layout, comments, images or hidden metadata.

Keep operational diagnostics outside the report. Final report content contains only the report and its real sources, not the name of this skill, the upstream editor, its authors or its repository as a production credit.
