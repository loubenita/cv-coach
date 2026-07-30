> **Bundled skill: `linkedin-optimiser`** - reference doc for the cv-generator agent pipeline.
>
> Converts a finalised CV into LinkedIn profile content, keeping the two consistent. Generates headline, About section, per-role descriptions, skills list, and featured section suggestions. Called by the cv-generator agent when the user wants their LinkedIn to mirror their CV.

# linkedin-optimiser

Turn the CV into LinkedIn profile content optimised for LinkedIn's search and recruiter filters, while keeping the content factually consistent with the CV.

## Input

```json
{
  "cv": {},
  "target_role": "",
  "target_seniority": ""
}
```

## Sections produced

### Headline (≤220 chars)

Formula: `{Role} @ {Company} | {Primary expertise} | {Differentiator}`

Example: `iOS Engineer @ Northwind Fitness | Swift, SwiftUI, Clean Architecture | Shipping at e-commerce scale`

### About section

3-4 short paragraphs:
1. What you do and for whom (1-2 sentences)
2. Core competencies (bulleted or prose)
3. What you care about / how you work (culture-fit signal)
4. Optional: what you're interested in next

Keep it in first person. LinkedIn's algorithm weights the first 3 lines heavily. Lead with the strongest signal.

### Experience entries

For each role:
- **Title and company**: identical to CV
- **Description**: expanded from CV bullets into flowing prose or a mix of prose + bullets
- **Skills tagged**: LinkedIn allows skill tags per role; surface the 5-8 most relevant

LinkedIn descriptions can be longer than CV bullets. Use this space for context the CV trims.

### Skills list

Order skills by:
1. Target-role relevance
2. Depth of experience
3. LinkedIn market signal (pull from trend-lookup if available)

Cap at 50, LinkedIn's practical limit for the top list.

### Featured section suggestions

Recommend 3-5 items based on the CV's projects, publications, or notable achievements:
- Shipped apps / projects with links
- OSS repos
- Talks / articles
- Certifications

## Output

```json
{
  "headline": "",
  "about": "",
  "experience": [
    {
      "company": "",
      "title": "",
      "description": "",
      "skills_tagged": []
    }
  ],
  "skills": [],
  "featured_suggestions": [
    {
      "type": "link | media | certification",
      "title": "",
      "description": "",
      "url": ""
    }
  ],
  "consistency_check": {
    "matches_cv": true,
    "discrepancies": []
  }
}
```

## Rules

- Every claim in the LinkedIn output must be traceable to a claim in the input CV.
- No new metrics, titles, or achievements.
- First-person on LinkedIn; CV can be implicit-subject or third-person. Mind the voice shift.
- If the CV and LinkedIn drift (e.g. user already has a LinkedIn), flag discrepancies rather than silently overwriting.
