> **Bundled skill: `trend-lookup`** - reference doc for the cv-generator agent pipeline.
>
> Looks up current hiring trends, in-demand keywords, and role expectations for a given role and seniority level. Called by the cv-generator agent during the pipeline to ensure the CV reflects the current market.

# trend-lookup

Given a role and seniority level, research the current job market and return structured data the cv-generator agent can act on.

## Input

```json
{
  "role": "",
  "seniority": "",
  "industry": ""
}
```

## Steps

1. Search for recent job postings for this role and seniority (last 90 days where possible).
2. Identify the top 10–15 keywords appearing most frequently across postings.
3. Identify any technologies or practices that appear to be declining in demand.
4. Identify any skills the candidate already has (from the extracted CV) that are high-demand but under-represented.

## Output

```json
{
  "high_demand_keywords": [],
  "declining_keywords": [],
  "underrepresented_strengths": [],
  "market_notes": ""
}
```

## Rules

- Only return signals from real, recent sources. Do not fabricate trends.
- Flag if data is limited or inconclusive rather than guessing.
- `market_notes` should be 1–2 sentences summarising the current landscape for this role.
