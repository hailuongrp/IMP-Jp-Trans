# Evaluation record — hai-jp-report v1

Date: 2026-10-17 (Asia/Tokyo). Inputs are synthetic and contain no customer data.

| Case | Observed result | Method and limits |
|---|---|---|
| VI → JP full report | Completed all sections and three table rows. Preserved proposal status, both pilot conditions, evidence attribution, uncertainty, quantitative units, source URLs, and no-exception scope. | Direct source comparison plus a fresh-context model reviewer found no meaning-changing discrepancy in this sample. Not a human/native review. |
| EN/JP review only | Identified 12 seeded discrepancies spanning decision, logic, approval, attribution, omissions, scenario, financial metric, percentage points, and manual-review requirement. Original files remained unchanged. | Model review against source; this does not measure recall across unseen reports. |
| JA-only editing and output branding | Simplified Japanese and removed the specifically requested tool credit. Kept unconfirmed willingness to pay, proposed investigation, and pending approval. | Self-review; correctly limited fidelity claims because no source-language original was provided. |

The two final JP samples contain no added tool/author credit, watermark text, or QA prose. File-based Office/PDF metadata and slide notes were not exercised by these Markdown cases; the skill requires checking them when those formats are used.

## Package validation

- Skill frontmatter and naming passed the skill validator.
- Vendor verification matched all 20 upstream files and the provenance manifest to the pinned commit.
- The vendor helper was tested for reproducible sync, checksum/manifest tampering, source drift, unexpected files, symlinks, and incorrect pins using temporary copies.
- The runtime morphology helpers could not complete because their dependencies were unavailable and the test environment could not download them. The documented manual fallback was exercised. No automated Japanese-lint pass is claimed.

See `evals.json` for prompts and acceptance criteria. These checks exercise workflow safeguards. They do not establish universal accuracy, improved translation quality over an unassisted model, or suitability of the default glossary for an approved company standard. Evaluate the skill on an approved real IMP/EE report before treating the style/terminology as a house standard.
