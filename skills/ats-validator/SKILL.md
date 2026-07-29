> **Bundled skill: `ats-validator`** — reference doc for the cv-generator agent pipeline.
>
> Validates a CV against ATS compliance rules and rewrites structure where needed. Called by the cv-generator agent after role detection and trend lookup.

# ats-validator

Check the CV structure and content against ATS requirements. Return a compliance report and a clean, rewritten version ready for the content improvement step.

## Input

```json
{
  "cv": {},
  "trend_keywords": [],
  "job_description": ""
}
```

## Checks

| Rule | Pass condition |
|------|---------------|
| Single column | No multi-column layout |
| No tables or graphics | Plain text only |
| Standard headings | Experience, Skills, Education, Projects only |
| Reverse chronological | Most recent role first |
| Keyword coverage | Top trend keywords present naturally in the text |
| No special characters | No emojis, icons, or non-standard symbols |
| Contact info present | Name, email, location at minimum |
| Date format consistent | Same format throughout |

## Output

```json
{
  "ats_pass": true,
  "violations": [],
  "keyword_coverage": {
    "present": [],
    "missing": []
  },
  "rewritten_cv": {}
}
```

## Rules

- Do not rewrite content. Adjust structure and ordering only.
- Keywords must be woven in naturally. Never keyword-stuff.
- If a keyword cannot be added without fabricating experience, add it to `missing` only.
