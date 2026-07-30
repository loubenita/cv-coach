> **Bundled skill: `post-miner`** - reference doc for the cv-generator agent pipeline.
>
> Reads a candidate's public posts (LinkedIn, X/Twitter, personal blog) and extracts CV-worthy claims: deal values, project outcomes, events attended, talks given, awards, publications. Returns structured data with confidence levels and suggested CV bullet wording. Never promotes post content to the CV without explicit user confirmation. Called by the cv-generator agent when the candidate has a public activity feed worth mining.

# post-miner

Most candidates are worse at their CV than at their LinkedIn posts. Real deal values, concrete outcomes, talks given, events attended. These details often live in social posts but never make it onto the CV. This skill mines those posts into structured CV candidates, always surfacing them for user confirmation before they ship.

## Input

```json
{
  "profile_url": "",
  "scope": {
    "max_posts": 30,
    "max_age_months": 24
  }
}
```

## What counts as CV-worthy

A post is **CV-worthy** if it contains any of:

| Signal type | Example |
|-------------|---------|
| Quantified deal / project outcome | "£625k cross-charge completed in 48 hours" |
| Named client or partner | "Worked with Marks & Spencer on ETL pipeline" |
| Event participation (attended or spoke) | "At NACFB event today at stand C19" |
| Talk, publication, or award | "My paper on X published in Y journal" |
| Launch or release | "Just shipped v2.2 of RentLoop to the App Store" |
| Measurable team or company result | "Closed £300m in funding this year" |

A post is **not** CV-worthy if it is:

- Opinion / industry commentary
- Reposts of others' content (unless the candidate added a quoted contribution)
- Personal / non-professional content
- Marketing boilerplate with no specific, verifiable detail
- Jokes, memes, holiday greetings

## Extraction process

For each post in scope:

1. Classify: is it CV-worthy? If no, skip.
2. Extract the concrete data points (amounts, dates, parties, outcomes).
3. Assign a confidence level:
   - **high**: specific numbers, named parties, dated, publicly verifiable
   - **medium**: specific outcome but promotional tone, numbers may be rounded, some ambiguity
   - **low**: mentions work but without enough detail to verify, often a vague "we crushed it"
4. Suggest a CV bullet. Use the candidate's own language where it's honest; strip marketing spin.
5. Cite the source post URL.

## Output

```json
{
  "posts_scanned": 0,
  "posts_worth_mining": 0,
  "candidate_claims": [
    {
      "source_url": "",
      "post_date": "",
      "type": "deal | outcome | event | talk | launch | team_result",
      "extracted_data": {
        "value": "",
        "date": "",
        "parties": [],
        "outcome": ""
      },
      "confidence": "high | medium | low",
      "suggested_bullet": "",
      "target_role": "",
      "user_confirm_required": true,
      "notes": ""
    }
  ],
  "cv_discrepancies": [],
  "red_flags": []
}
```

### `cv_discrepancies`

If a post contradicts something on the candidate's CV (e.g. claimed "worked at X" but posts tag a different employer), surface it here.

### `red_flags`

If posts reveal things the candidate might not want on the CV (political content, customer dispute, embarrassing public exchange), flag them here so the candidate can decide on visibility and knows what a recruiter scanning their posts will see.

## Rules

- **Never** copy a post claim directly into the CV without returning `user_confirm_required: true`.
- **Never** invent a metric if the post is vague. Ask the user in `notes` instead.
- **Never** include opinion posts as CV content. These are personal brand signal, not work experience.
- Attribution matters: if the post is from the candidate's employer and they were part of the team, reflect that accurately ("team I was part of delivered X") rather than implying solo ownership.
- Reposts do not count unless the candidate added substantive original commentary.
- Respect privacy: if the post is older than `max_age_months`, drop it.
- If the candidate has no posts, return an empty `candidate_claims` array. Don't fabricate.

## Guardrails

- Marketing posts often inflate. A "48-hour miracle completion" post might actually have taken longer. The 48h may be the signed-to-legal timeline, not the full process. Record the exact phrasing the candidate used, and in `notes` flag any plausibility concern.
- Event attendance is CV-worthy only when the candidate was representing a company, speaking, or demonstrating. Just attending is networking, not an achievement.
- Team outcomes must be framed as team outcomes. "We closed £300m" becomes "Part of a team that deployed £300m in capital". Never write "I closed £300m" unless the candidate was genuinely sole.
