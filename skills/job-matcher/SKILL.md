> **Bundled skill: `job-matcher`** - reference doc for the cv-generator agent pipeline.
>
> Semantically matches a CV against a job description. Returns a match score, gap analysis, and rewrite suggestions. Called by the cv-generator agent when a job description is provided.

# job-matcher

Compare the improved CV against the job description. Identify what aligns, what is missing, and what can be honestly rewritten to improve the match.

## Input

```json
{
  "cv": {},
  "job_description": ""
}
```

## Steps

1. Extract required skills, keywords, and responsibilities from the job description.
2. Map each requirement to the candidate's experience.
3. Score the overall match.
4. For gaps: determine if they can be closed with an honest rewrite, or if they represent a genuine skill gap.

## Output

```json
{
  "match_score": 0,
  "aligned_skills": [],
  "missing_keywords": [],
  "gaps": [
    {
      "requirement": "",
      "candidate_has": "",
      "closeable_with_rewrite": true,
      "suggested_rewrite": ""
    }
  ],
  "reorder_suggestions": []
}
```

## Rules

- Never fabricate experience to close a gap. Mark `closeable_with_rewrite: false` and leave it to the candidate.
- `reorder_suggestions` should surface the most relevant bullets and experience first, without changing their content.
- Match score is based on keyword coverage, experience alignment, and seniority fit. Explain any score below 60.
