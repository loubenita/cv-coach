> **Bundled skill: `feedback-loop`** — reference doc for the cv-generator agent pipeline.
>
> Ingests application outcomes (rejection, screening, interview, offer) and adjusts CV wording, structure, and keyword strategy based on what's working. Called by the cv-generator agent when the user wants to iterate on an existing CV after real-world use.

# feedback-loop

Use real application outcomes as signal. If a CV gets 10 rejections and 0 screening calls, something is failing the first filter. Change strategy.

## Input

```json
{
  "cv": {},
  "applications": [
    {
      "job_id": "",
      "job_description": "",
      "submitted_at": "",
      "outcome": "rejected | screening_call | interview | offer | no_response",
      "rejection_reason": "",
      "notes": ""
    }
  ]
}
```

## Analysis

Compute:
- **Response rate**: % of applications that got any reply
- **Screening rate**: % that reached a recruiter screen
- **Interview rate**: % that reached a hiring-manager conversation
- **Outcome by role type**: pattern across similar roles
- **Common rejection signals**: patterns in stated rejection reasons

## Adjustments

Based on patterns:

| Pattern | Likely cause | Adjustment |
|---------|--------------|------------|
| High rejection / low screening | ATS or recruiter filter failing | Strengthen keyword coverage, simplify structure, bold key skills |
| Low rejection / low screening | Not being noticed | Improve positioning, strengthen first-bullet impact per role |
| Good screening / low interview | Pitch mismatch at recruiter level | Rewrite summary, clarify seniority signal |
| Good interview / no offer | Not a CV issue. Flag to user | No CV changes. Suggest interview prep |

## Output

```json
{
  "metrics": {
    "response_rate": 0,
    "screening_rate": 0,
    "interview_rate": 0,
    "offer_rate": 0
  },
  "patterns": [],
  "recommended_adjustments": [
    {
      "target": "summary | bullet | skills | structure",
      "change": "",
      "rationale": "",
      "based_on": []
    }
  ],
  "no_change_needed": false
}
```

## Rules

- Require at least 5 applications before suggesting structural changes. Below that, the sample is too small.
- If `interview_rate > 20%`, flag `no_change_needed: true` for CV-level changes. The CV is working.
- Every recommendation must cite `based_on`, specifying which applications or patterns drove it.
- Never speculate about a rejection reason when the data doesn't support it.
