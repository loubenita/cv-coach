> **Bundled skill: `benchmark`** — reference doc for the cv-generator agent pipeline.
>
> Scores CV bullets and structure against industry standards for the target role and seniority. Returns a competitiveness score and specific improvements. Called by the cv-generator agent after content improvement.

# benchmark

Score the CV against what a competitive candidate at this seniority level typically presents. Return a competitiveness score and a prioritised list of improvements.

## Input

```json
{
  "cv": {},
  "role": "",
  "seniority": ""
}
```

## Checks

### Bullet strength

For each bullet, score on:
- **Action verb**: strong and specific (Delivered, Reduced, Architected) vs weak (Helped, Worked on, Assisted)
- **Impact**: measurable outcome present, implied, or absent
- **Context**: enough information to understand scope and relevance

### Structure

- Correct number of bullets per role (3-5 for recent roles, 1-2 for older ones)
- No bullet exceeds two lines
- Skills section is grouped logically, not a flat dump

### Seniority alignment

- Bullets demonstrate ownership and decision-making appropriate for the target level
- Leadership signals present where expected (Senior and above)
- No junior-sounding language for a senior target role

### Confidence scoring

For each bullet, assign a confidence level based on how defensible it would be in an interview:

| Level | Meaning |
|-------|---------|
| `high` | Claim is specific, measurable, and verifiable (real metric, concrete project, public artefact) |
| `medium` | Claim is specific and concrete but lacks a measurable outcome |
| `low` | Claim is vague, uses filler language, or would crumble under questioning |

### Suggested rewrite policy

Not every bullet gets a rewrite. Offer one only when it's actionable:

- **Low bullets always get a rewrite.** This is the primary fix; return it populated, never empty.
- **Medium bullets get a rewrite when the upgrade path is clear** — a bounded number, a named flow, or a measurable outcome that would lift the rating to High. If the Medium bullet is simply short but defensible, leave `suggested_rewrite` empty rather than padding.
- **High bullets rarely get a rewrite.** Only when a single small addition (usually one honest numeric outcome) would move the bullet to the strongest on the CV. Use sparingly; the point of the rewrite field is to fix weakness, not polish already-strong bullets.

Every rewrite uses placeholder brackets where the real number is unknown (`[X% lift in Y]`, `[named flow]`, `[N endpoints consolidated]`). Never invent a metric to fill the rewrite.

### Tense consistency check

Before returning `bullet_scores`, scan every bullet within a single role and confirm verb tense is uniform. The convention on professional CVs is **simple past for every bullet in every role, including the current one** ("Delivered", "Shipped", "Led"). A mix of present-tense ("Take", "Lead") and past-tense bullets inside the same role reads as careless and is noticeable in a 6-second scan.

When a mismatch is found, flag it on the offending bullet using the `issues` array with the exact tag `tense_inconsistent`, and populate `suggested_rewrite` with the past-tense version of the bullet text (no other changes). The `tense_inconsistent` tag tells downstream sections (dashboard bullet audit, cv-tailor) to render the rewrite as a "Tense fix only" rather than a content change.

## Output

```json
{
  "competitiveness_score": 0,
  "bullet_scores": [
    {
      "bullet": "",
      "score": 0,
      "confidence": "high | medium | low",
      "issues": [],
      "suggested_rewrite": ""
    }
  ],
  "structure_issues": [],
  "seniority_alignment": "",
  "section_confidence": {
    "experience": "high | medium | low",
    "skills": "high | medium | low",
    "projects": "high | medium | low"
  }
}
```

## Rules

- Score each bullet 0-100.
- Apply the **Suggested rewrite policy** above: rewrites are mandatory for Low bullets, conditional for Medium, rare for High. Never invent a metric to fill a rewrite — use placeholder brackets for unknown numbers.
- Run the **Tense consistency check** above before finalising. Add `tense_inconsistent` to the `issues` array of any offending bullet and populate `suggested_rewrite` with the past-tense rewrite.
- `competitiveness_score` is the average bullet score, weighted by role recency.
- `seniority_alignment` should be one of: "strong", "adequate", "weak", with a one-line explanation.
- `section_confidence` summarises the weakest link. A single `low` bullet drops the whole section to `low`.
- Standard `issues` tags include: `no_metric`, `weak_verb`, `unclear_scope`, `filler_language`, `wrong_tense`, `tense_inconsistent`, `unverifiable_claim`, `duplicate_of_role_above`. Add others as needed but prefer these for downstream parseability.
