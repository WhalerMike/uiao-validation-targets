# AGENT-RULES.md

> Formal rules for all Claude Code Team / Copilot / Comet agents working in the
> **uiao-validation-targets** repository.
> These rules adapt the 10 Claude Code Team whiteboard tips to this repo's
> FedRAMP Moderate Rev 5 validation context.

---

## Rule 1 — Concurrency Limit

**Maximum 4 concurrent agents at any time.**

Running more than 4 agents simultaneously creates conflicting file edits,
race conditions in CI, and makes the Correction Log unmanageable.
Never spawn a fifth agent until one of the active four has completed and logged its outcome.

---

## Rule 2 — Plan Mode for Changes > 20 LOC

Any task estimated at more than **20 lines of change** MUST begin with a Plan Mode session
before touching any file.

### Plan Mode Prompt Template

```
You are working on the uiao-validation-targets FedRAMP Rev 5 validation repo.

Task: <DESCRIBE TASK HERE>

Before writing any code:
1. List every file you will touch and why.
2. Identify any OSCAL schema, telemetry baseline, or validate-endpoint.yml constraint
   that applies to this change.
3. Produce a numbered checklist of steps (max 10). Each step must be ≤ 5 LOC of
   estimated change.
4. Flag any step that requires Grill Master review before proceeding.

Output ONLY the plan. Do not write code yet.
```

Paste the generated plan into the PR under the **Plan Mode Summary** section.

---

## Rule 3 — Memory-First Protocol

**On every run:**

1. Read `VALIDATION-MEMORY.md` in full before taking any action.
2. Check the Correction Log for rules that apply to the current task.
3. After every merged PR, append a new row to the Correction Log
   (date, task, outcome, issue/error summary, correction rule).

Failure to follow memory-first is grounds for the Grill Master to block the PR.

---

## Rule 4 — Custom Skills

Four skills are defined for this repo. Agents MUST use the appropriate skill
rather than implementing ad-hoc logic.

| Skill | Trigger | What It Does |
|-------|---------|--------------|
| **Endpoint Validation** | Any change to `app/` or `Dockerfile` | Runs `validate-endpoint.yml` locally via `act` or in CI; fails fast on non-2xx or schema mismatch |
| **OSCAL Evidence Ingestion** | Any new evidence artifact added to `validation/` | Validates artifact against `validation/oscal-1.3.0-schema/`; records provenance in evidence index |
| **Telemetry Generation** | Any change to `telemetry/` | Regenerates telemetry baseline diff; fails if output deviates from FedRAMP Rev 5 baseline |
| **FedRAMP Baseline Sync** | Quarterly or when NIST/FedRAMP publishes updates | Pulls latest Rev 5 profiles, re-validates all controls, updates baseline snapshot |

---

## Rule 5 — Autonomous Bug Fixing

When a CI run fails, follow this exact protocol:

1. Copy the full CI log output.
2. Open a new agent session with this prompt:

```
CI failure in uiao-validation-targets.

Logs:
<PASTE FULL CI LOG HERE>

Fix using VALIDATION-MEMORY.md correction rules. Steps:
1. Identify the root cause from the log.
2. Check VALIDATION-MEMORY.md for an existing correction rule.
3. If a rule exists, apply it exactly.
4. If no rule exists, propose a fix AND a new correction rule to add to VALIDATION-MEMORY.md.
5. Output a minimal diff. Do not change files outside the failure scope.
```

3. Apply the proposed diff, re-run CI, and append the outcome to the Correction Log.

---

## Rule 6 — Grill Master Review (Required Before Merge)

**No PR may be merged without a Grill Master review.**

The Grill Master is a dedicated adversarial review agent whose sole job is to find
problems the author missed.

### Grill Master Prompt

```
You are the Grill Master for uiao-validation-targets.
Your job is adversarial review. Be skeptical. Find problems.

PR Title: <PR TITLE>
PR Diff:
<PASTE FULL DIFF HERE>

Review checklist (answer YES / NO / NEEDS-FIX for each):
1. Does every changed file in app/ pass Endpoint Validation skill?
2. Does every new OSCAL artifact validate against oscal-1.3.0-schema/?
3. Does telemetry output match the FedRAMP Rev 5 baseline?
4. Are all dependencies pinned and free of HIGH/CRITICAL CVEs (pip-audit clean)?
5. Is VALIDATION-MEMORY.md updated with a new Correction Log entry?
6. Does the PR description include a Plan Mode Summary?
7. Is validate-endpoint.yml CI green?
8. Are there any secrets, credentials, or PII accidentally included?
9. Does this change break any existing OSCAL control mappings?
10. Is there any logic that could cause a compliance gap under FedRAMP Rev 5?

For every NEEDS-FIX item, provide the exact change required before approval.
Output a final verdict: APPROVED / REQUEST-CHANGES.
```

The Grill Master verdict must be pasted into the PR as a comment before merge.

---

## Rule 7 — Terminal & Tooling Setup

Maintain a consistent terminal environment across all agents:

- Python virtual environment activated at repo root (`.venv/`).
- `pip-audit`, `act`, and `yamllint` installed in the venv.
- Pre-commit hooks enabled (`pre-commit install`) to catch issues locally.
- Environment variable `FEDRAMP_ENV=validation` set in all CI runs.

---

## Rule 8 — Subagent Composition

When a task spans multiple skills (e.g., a change that touches both `app/` and `telemetry/`):

- Decompose into one subagent per skill.
- Each subagent reports its outcome independently to the Correction Log.
- The orchestrating agent waits for all subagents to complete before opening the PR.
- Total concurrent subagents counts toward the Rule 1 limit of 4.

---

## Rule 9 — Analytics & Observability

Track the following metrics in the Correction Log over time:

- PR success rate (SUCCESS vs. FAILURE outcomes).
- Most common error categories (dependency, schema, telemetry, CI).
- Mean time to green CI after a failure.

Use these trends to prioritize which Correction Rules to strengthen.

---

## Rule 10 — Continuous Learning

After every 5 merged PRs, review the Correction Log and:

1. Identify the top 3 recurring error patterns.
2. Promote each pattern into a dedicated Quick Reference Rule in `VALIDATION-MEMORY.md`.
3. Update the relevant Custom Skill (Rule 4) to prevent the pattern automatically.
4. Schedule a FedRAMP Baseline Sync skill run if any control mappings were affected.

Learning is secondary to delivery — never block a PR solely to wait for a learning review.
