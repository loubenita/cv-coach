> **Bundled skill: `cv-tailor`** — reference doc for the cv-generator agent pipeline.
>
> Generates multiple tailored CV variants for different jobs while keeping a canonical base CV intact. Called by the cv-generator agent when the user has multiple target roles or job applications.

# cv-tailor

Produce per-job tailored versions of the CV without modifying the canonical base. Each variant is a view into the same source of truth.

## Input

```json
{
  "base_cv": {},
  "target_jobs": [
    {
      "id": "",
      "job_description": "",
      "jd_intel_output": {}
    }
  ]
}
```

## Method

For each target job:

1. **Start from base.** Never mutate `base_cv`.
2. **Reorder bullets**: surface the most relevant experience first, based on `jd_intel_output.keyword_priority`.
3. **Rewrite bullets selectively**: keep factual content identical; adjust phrasing and word choice to match the JD's vocabulary where honest.
4. **Prune irrelevant skills**: drop skills from the Skills section that add no value for this specific role (but never from the base).
5. **Emphasise specific achievements**: if the role cares about leadership, surface leadership bullets first.
6. **Summary rewrite**: if a summary section exists, adjust to match the role's tone and focus.

## Output

```json
{
  "variants": [
    {
      "job_id": "",
      "cv": {},
      "changes_from_base": [
        {
          "type": "reorder | rewrite | prune | emphasise | summary",
          "target": "",
          "before": "",
          "after": "",
          "rationale": ""
        }
      ]
    }
  ],
  "base_cv_unchanged": true
}
```

## Rules

- `base_cv` must be identical in memory before and after this skill runs. Assert `base_cv_unchanged: true` in the output.
- Every change must be explainable; the `changes_from_base` list is the audit trail.
- Never add experience that isn't in the base.
- If two jobs are >80% similar, consolidate into one variant rather than producing near-duplicates.
