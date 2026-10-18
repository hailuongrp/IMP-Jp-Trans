# Tests and evaluation limits

Run mechanical regression tests from the repository root:

```bash
python3 -m unittest discover -s skills/hai-jp-report/tests -v
```

The initial implementation's 18 unit tests were run in an isolated build workspace and passed. They exercise the dependency-free text checker, not an LLM, native skill discovery or the Japanese editing dependency. They use synthetic text only; no confidential IMP/EE report is included.

A successful checker result only means no supported mechanical pattern was flagged. Numerical notation conversions are intentionally flagged for review; the checker cannot establish semantic equivalence. Citation matching is heuristic. It does not inspect PDF/Word metadata or certify the absence of every conceivable watermark.

Not yet verified for this package: end-to-end invocation in the user's Codex installation; upstream uv scripts in the user's environment; independent human Japanese review; blind translation-quality comparison on a locked IMP/EE report. Do not describe these as completed.

Before approving translation quality, compare baseline GPT, wrapper without editing, and the complete wrapper under the same model/settings/source/glossary. Use blinded bilingual reviewers, inspect the entire original and final Japanese, and prioritize critical/major meaning errors, completeness, naturalness and correction time. Include negation, uncertainty, two simultaneous conditions, unconfirmed customer willingness, numeric units, table notes, evidence appendices, actor ambiguity and newly added tool credit. Keep real client reports outside this public repository unless the owner explicitly authorizes their publication.

## Offline dependency integrity

`test_vendor_bundle.py` adds ten checks for default read-only verification, tampered bytes or manifest, source drift, unexpected entries, symlinks, explicit pin acknowledgement, repeatable repair, lock drift, missing files and permission changes. These tests require a repository checkout containing `dev/sync_hai_jp_vendor.py` and the pinned Git objects; they copy the source and bundle into disposable local repositories and do not call a vendor or modify the checkout's dependency files.

Run the suite with `PYTHONDONTWRITEBYTECODE=1`. The eight historical synthetic evaluation files under `evals/hai-jp-report/` are preserved from the original PR head; their recorded model observations have not been replayed by these mechanical tests.
