# VALIDATION-MEMORY.md

> **Persistent memory for uiao-validation-targets Copilot/Comet agents.**
> FedRAMP Moderate Rev 5 live validation target.
> **Update after EVERY run. All agents MUST read this file first.**

---

## Correction Log

| Date | Task | Outcome | Issue/Error Summary | Correction Rule |
|------|------|---------|---------------------|-----------------|
| 2026-03-24 | python-multipart vuln | FIXED | `python-multipart <0.0.22` shipped in requirements | ALWAYS run `pip-audit` before any deploy; never ship `python-multipart <0.0.22` |
| 2026-03-24 | Bootstrap | SUCCESS | PR #1 (+1200 lines, 13 files, python-multipart vuln fixed) | Always bump vulnerable deps before deploy; use pinned versions `>=0.0.22` |

*(Most recent entries at the top. Append new rows after every PR.)*

---

## Quick Reference Rules

1. **CI Gate** — Every change MUST pass the `validate-endpoint.yml` workflow before merge.
2. **OSCAL Evidence** — All OSCAL evidence MUST validate against `validation/oscal-1.3.0-schema/` before being committed.
3. **Telemetry Baseline** — Telemetry output MUST match the FedRAMP Rev 5 baseline; diff against baseline before opening a PR.
4. **Merge Gate** — Never merge without **Grill Master** approval (see `AGENT-RULES.md` Rule 6).
5. **Dependency Security** — Run `pip-audit` (and equivalent for other ecosystems) on every dependency change; block on any HIGH/CRITICAL finding.
6. **Pinned Versions** — Use pinned, exact versions for all dependencies in `requirements.txt` / lock files.
