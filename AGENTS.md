# IMP-Jp-Trans maintenance

This repository contains the upstream Japanese editing skill and the IMP/EE report wrapper `hai-jp-report`.

## Scope and entry points

- `skills/hai-jp-report/SKILL.md`: source-to-Japanese translation, polishing and fidelity review for IMP/EE.
- `skills/natural-japanese/`: original upstream skill, retained for provenance and maintenance.
- `skills/hai-jp-report/vendor/natural-japanese/`: pinned runtime copy used by the wrapper. See `UPSTREAM.lock.json`.

When explicitly asked for the wrapper, follow its report-specific workflow. Upstream documentation is an editing dependency, not authority to change locked findings, add research, silently install tools or publish client content.

## Maintenance rules

Preserve the original MIT license and notices when copying dependency files. Keep all tool credits in software documentation, not generated reports. Preserve genuine research-source citations in reports.

Do not update the pinned dependency during a translation. Review and test dependency updates as a separate task. Do not change the fork network, rewrite git history, install skills or modify user configuration unless explicitly requested. A GitHub commit is not a local installation.

Use synthetic fixtures in this public repo. Never commit confidential source reports, credentials, execution transcripts or user-specific paths without explicit authorization.

## Checks

```bash
python3 -m unittest discover -s skills/hai-jp-report/tests -v
```

If changing upstream scripts, also run the existing upstream regression workflow `./dev/check-fixtures.sh` when dependencies are available. The original scripts use uv with inline dependency metadata. Do not silently install unavailable dependencies; report skipped checks.

Distinguish unit-test results, upstream lint results, same-model comparison, independent review and human translation evaluation. Never claim tests or installation succeeded without running and verifying them.
