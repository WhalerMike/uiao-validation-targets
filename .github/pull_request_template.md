## PR Checklist

Before requesting review, confirm **every** item below. Replace `[ ]` with `[x]` when done.

### Agent Protocol
- [ ] Read `VALIDATION-MEMORY.md` in full before starting this task
- [ ] Applied all relevant Correction Rules from the VALIDATION-MEMORY.md log
- [ ] This PR appends a new row to the VALIDATION-MEMORY.md Correction Log

### Plan Mode (required for changes > 20 LOC)
- [ ] Plan Mode was followed (or task is ≤ 20 LOC — check one)
- [ ] Plan Mode summary is pasted in the section below

### CI & Validation
- [ ] `validate-endpoint.yml` CI workflow is **green**
- [ ] All OSCAL evidence artifacts validate against `validation/oscal-1.3.0-schema/`
- [ ] Telemetry output matches FedRAMP Rev 5 baseline (diff attached or N/A)
- [ ] `pip-audit` (or equivalent) returns **zero** HIGH/CRITICAL findings

### Grill Master Review
- [ ] Grill Master review has been completed (paste verdict comment link or inline below)

---

## Plan Mode Summary

<!-- If Plan Mode was used, paste the full plan output here. -->
<!-- If task was ≤ 20 LOC, write "N/A — change is ≤ 20 LOC" -->

```
<PASTE PLAN MODE OUTPUT HERE>
```

---

## Grill Master Verdict

<!-- Paste the Grill Master agent's APPROVED / REQUEST-CHANGES verdict here. -->

```
<PASTE GRILL MASTER OUTPUT HERE>
```
