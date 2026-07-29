# CV Generator: Guided Intake, Compaction-Proof Evidence Store, Change Report

## Context

The `/cv` command currently gathers intake in one batched message, and pasted evidence (performance reviews, metrics) lives only in conversation context, so compaction can silently lose it. The pipeline also produces gap/weakness data (Steps 2b, 12, 14b) but never assembles a single "what your CV lacked, what evidence filled it, what changed" view.

This change delivers three things the user asked for:
1. A **guided intake questionnaire** (series of question rounds: LinkedIn? GitHub? Portfolio? existing CV? metrics? perf review 6/12/24 months? **job to tailor for + JD/link?**).
2. A **durable evidence store** so metrics and reviews are written to disk verbatim the moment they arrive and always recoverable after compaction. Entries are unique and timestamped: a different CV next month, or a new JD per application, each becomes its own immutable entry, never an overwrite.
3. A **change report** mapping original-CV weaknesses → evidence that filled them (or "still missing, ask next time") → the change applied, as a markdown file and a dashboard section.

User decisions captured: guided rounds (not one batched ask); existing workspace files (`Sam_Rivera_Resume.pdf`, highlight notes) get *registered* as referenced evidence entries, but each run asks which CV is the source of truth for *this* run; JD-tailoring is an explicit intake question.

All edits target the authoritative bundle (`~/.claude/agents/cv-generator/` + `~/.claude/commands/cv.md`). The dev source at `~/Development/cv-generator/...` has diverged **behind** the bundle; do not edit it (README notes this).

---

## New persisted artifacts (extend existing memory layer)

Under `~/.cv-generator/<user>/`:

```
├── intake.json        ← questionnaire answers + evidence pointers, per-run history
├── evidence/          ← raw pasted docs, verbatim, immutable, timestamped
│   ├── 2026-07-16-perf-review-2026H1.md
│   ├── 2026-07-16-existing-cv.md
│   └── index.json     ← provenance index
```

### `intake.json` schema
```json
{
  "schema_version": 1,
  "user_slug": "sam-rivera",
  "last_intake_at": "2026-07-16T09:30:00Z",
  "answers": {
    "target_role_title": "Senior iOS Engineer",
    "seniority": "Senior",
    "trajectory": "same_role|promotion|pivot",
    "geography": ["UK"],
    "desired_outputs": ["canonical_cv", "tailored_variants", "linkedin", "pdf"],
    "has_existing_cv": { "value": true, "detail": "<path or evidence id>" },
    "has_linkedin":    { "value": true, "detail": "<url>", "surface_in_cv": true },
    "has_github":      { "value": true, "detail": "<url>" },
    "has_portfolio":   { "value": false, "detail": "" },
    "has_metrics":     { "value": true, "detail": "see evidence index" },
    "has_perf_review": { "value": true, "window": "0-6m|6-12m|12-24m" },
    "has_jd":          { "value": true, "detail": "see evidence index" }
  },
  "runs": [
    { "date": "2026-07-16", "source_cv": "ev-2026-07-16-existing-cv",
      "jds": ["ev-2026-07-16-jd-monzo-senior-ios"] }
  ],
  "evidence_pointers": ["ev-2026-07-16-perf-review-2026H1"],
  "declined": ["portfolio"],
  "do_not_ask_again": []
}
```
The `runs[]` array is what makes "later I might have a different CV / tailor per JD" work: each run records which CV evidence item was source of truth and which JD items it tailored to. Saved `answers` are defaults for the next run, not immutable truth.

### `evidence/index.json` schema
```json
{
  "schema_version": 1,
  "items": [{
    "id": "ev-2026-07-16-perf-review-2026H1",
    "type": "performance_review",
    "file": "evidence/2026-07-16-perf-review-2026H1.md",
    "received_at": "2026-07-16T09:31:00Z",
    "received_via": "orchestrator_intake|checkpoint_answer|workspace_seed",
    "coverage_period": "2026-H1",
    "source_label": "performance-review-2026-H1",
    "confidentiality": "unscreened|screened_public_safe|contains_confidential",
    "used_for": ["step-2b", "step-6", "step-7"],
    "claims_promoted": 4
  }]
}
```
`type` enum: `performance_review | metrics | brag_doc | jd | linkedin_paste | github_paste | portfolio_paste | existing_cv | okr | promo_packet | other`.
`source_label` reuses the provenance tag convention already in Step 2b (`"source": "performance-review-2026-H1"` in base.json), so every promoted claim joins back to a stored file.

---

## File 1: `~/.claude/commands/cv.md` (orchestrator; largest change)

### 1a. Replace Phase 1 with the guided questionnaire
- Resolve user first: list `~/.cv-generator/*/intake.json`; if a match exists → Phase 1R (returning user). Otherwise:
- **Round A, anchor (AskUserQuestion, up to 4):** target seniority; trajectory (same role / promotion / pivot); geography (multiSelect UK/US/EU/remote); desired outputs (multiSelect).
- **Round B, assets (AskUserQuestion, up to 4):** existing CV I can look at? (yes-paste/path / no); LinkedIn? (yes-paste / have-but-skip / no); GitHub or portfolio? (yes / no); **job(s) to tailor for? (yes, will paste JD or link / no, general CV)**.
- **Round C, evidence (AskUserQuestion, only still-unknown items, up to 4):** performance review recency (last 6 months / 6-12 / 12-24 / none); shareable performance metrics? (yes / no); brag doc, OKR outcomes, promo packet? (yes / no); anything else (free text via Other).
- Merge Rounds B and C into one call when 4 or fewer items remain unknown; skip anything `$ARGUMENTS` already supplied. Never exceed 4 questions per call.
- **Round D, documents (single plain-text ask):** target role title, plus the full paste or absolute path for every "yes": CV, JD(s) or posting links, LinkedIn content, GitHub/portfolio, perf review text, metrics, brag doc. State explicitly that pastes are saved verbatim to disk before the run starts. "Just run with what I gave you" → proceed.

### 1b. Add Phase 1R, returning user (deltas only)
- Load latest `intake.json` + `target.json`. One AskUserQuestion: "Last time: <role, seniority, geo>; on file: <CV, LinkedIn, evidence with coverage periods>. What changed?" (multiSelect: nothing / target / geography / links / **new CV to use** / **new JD to tailor for** / new evidence).
- Re-ask only flagged items. Honour `declined` and `do_not_ask_again`. For evidence, ask only for material newer than the latest `coverage_period` on file. A new CV or JD becomes a **new** evidence entry; nothing is overwritten.

### 1c. Insert Phase 1.5, persist on receipt (the durability rule)
As each document arrives, before anything else and before launching the agent:
1. Resolve slug (existing dir → CV name line → `_inbox/<timestamp>/` fallback, reconciled by the agent at Step 1).
2. Write each paste **verbatim, untrimmed** to `evidence/<date>-<type>-<coverage>.md`.
3. Append to `evidence/index.json`; update `intake.json` (answers + `runs[]` entry).
4. Phase 2 launch bundle passes **both** absolute paths and full content, stating evidence is already filed.

### 1d. Phase 2 addition
One line: agent treats `intake.json` as the confirmed Step 0 anchor (writes `target.json`, `confirmed_by_user: true`) and index entries as already-filed; does not re-request them.

### 1e. Phase 3 addition
If a checkpoint answer contains a pasted document, the orchestrator files it per Phase 1.5 **before** relaying via SendMessage (reply carries the new path + content).

---

## File 2: `~/.claude/agents/cv-generator/cv-generator.md` (five surgical edits, keep terse)

- **2a. Memory layer:** add `intake.json` + `evidence/` + `index.json` to the tree. Three new rules: evidence files are immutable once written (agent files mid-run arrivals before continuing); `source_label` in the index is the exact provenance tag used in base.json; **on resume after compaction, re-read intake.json, the index, and evidence files from disk — never trust context memory for metrics or review text**.
- **2b. Step 0:** when launched by `/cv`, read `intake.json` as the confirmed anchor (mirrors the existing intake fast path in the checkpoint protocol).
- **2c. Step 2b:** new first item in the evidence-handling list: *persist before parsing* — any evidence arriving mid-run that is not yet on disk gets written to `evidence/` + indexed before analysis. After mining, update the entry's `used_for` and `claims_promoted`; confidentiality screen outcome writes back to the index `confidentiality` field.
- **2d. New Step 14c, Change Report** (after 14b): assembly only, no new analysis. Joins: evidence inventory (index) + original-CV weaknesses (Step 12 run against the as-received CV + Step 14b `gaps[]`) + filled-by links (weakness → promoted claim `source` → index `source_label`) + still-missing (unanswered `evidence_needed` → "ask for X next time", also logged in `blockers[]`) + changes applied (Step 6/7 before/after + `changes_from_base`). Writes `versions/<timestamp>-<slug>-change-report.md`, feeds Step 16, added to `files_written`.
- **2e. Guardrail bullet:** "Evidence is captured before it is used: every metric or review is written verbatim to `evidence/` on receipt so nothing survives only in context; every promoted claim's `source` matches an index item."

### Change-report file format
```
# Change Report: <name>, <target role>, <date>
## 1. Evidence inventory (what you have done)        ← table, one row per index item
## 2. What your original CV was lacking              ← Step 12 + 14b findings
## 3. Weakness -> evidence -> change (core map)      ← table: weakness (cv_quote) | filled by <source_label> OR STILL MISSING | before -> after | rationale
## 4. Still missing (ask for next time)              ← gap + best source to close it
## 5. Full change ledger                             ← all rewrites + changes_from_base, each with provenance
```

No em dashes in any text added to these pipeline files (existing guardrail).

---

## File 3: `skills/dashboard/SKILL.md`

- Add `change_report` and `evidence_index` to the `pipeline_outputs` input block.
- New **Section 3c, Change report and evidence ledger** (reuses the Section 3b gap-table visual pattern): evidence inventory strip (chip per item: type, coverage, claims used); weakness→evidence→change table (filled rows first, still-missing last, green/red chips); amber "ask next time" callout cross-linked to blockers. Add `<section class="change-report">` to the HTML skeleton; graceful "Not run" note when absent.

## File 4: `README.md`

- Update the intake paragraph: guided questionnaire rounds; returning users get deltas only.
- New "Evidence store" subsection: paths, verbatim-on-receipt rule, compaction resilience, uniqueness of entries across runs.
- Note the change-report output and dashboard section.
- Note the dev source is behind the bundle and intentionally not updated.

## One-time seeding (after edits)

Register the existing workspace files for `sam-rivera` as evidence entries with `received_via: "workspace_seed"`: `Sam_Rivera_Resume.pdf` (type `existing_cv`), `sam_rivera_highlights.md` and `sam_rivera_additional_highlights.md` (type `brag_doc`). Files stay in `workspace/`; index entries point at their absolute paths. These are *referenced defaults*: every run still confirms which CV is the source of truth for that run.

---

## Verification (end-to-end dry run)

1. **New-user intake:** run `/cv` with no args → Round A, then B/C (merged when ≤4 unknowns, never >4 per call, JD question present), then Round D plain-text ask; optional items declinable in one pass.
2. **Immediate durability:** paste a fake perf review in Round D; before agent launch, `ls`/`cat` confirm `evidence/<date>-perf-review-*.md` verbatim + index + intake.json written.
3. **Compaction recovery:** simulate a mid-run checkpoint pasting metrics → agent writes to `evidence/` and indexes before continuing; a resumed run reads from disk, not context.
4. **Returning-user deltas:** re-run `/cv` for sam-rivera → single delta question, no re-asking of saved/declined items, evidence on file reused without re-paste; "new CV" answer creates a new entry without touching the old one.
5. **Provenance join:** every base.json claim added from evidence carries a `source` matching an index `source_label`.
6. **Change report:** `versions/<ts>-<slug>-change-report.md` exists; Section 3 maps ≥1 weakness to evidence and ≥1 to STILL MISSING; still-missing gaps also in `blockers[]`.
7. **Dashboard:** Section 3c renders; shows "Not run" gracefully when no evidence supplied.
8. **Guardrails:** zero em dashes in insertions; ≤2 checkpoints preserved; base.json untouched by tailored runs; cv-generator.md additions stay terse (~30 lines total).
