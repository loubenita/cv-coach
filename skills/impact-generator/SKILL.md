> **Bundled skill: `impact-generator`** - reference doc for the cv-generator agent pipeline.
>
> Suggests safe, honest impact ranges for bullets that lack measurable outcomes. Never fabricates numbers. Called by the cv-generator agent after content improvement when bullets are flagged as missing impact.

# impact-generator

When a bullet describes work but has no measurable impact, suggest a realistic range based on the work's nature, clearly labelled as an estimate for the candidate to confirm. Never ship a number without explicit user confirmation.

## Input

```json
{
  "bullet": "",
  "role": "",
  "seniority": "",
  "context": ""
}
```

## Safe-mode rules

1. **Never fabricate a specific number.** "Improved performance by 27%" is off-limits unless the user provided it.
2. **Ranges are allowed, clearly flagged.** "Likely improved performance by 10–30%" with a `user_confirm_required: true` flag is allowed.
3. **Qualitative impact is always allowed.** "Reduced support load from users hitting the bug" is factual and safe.
4. **When in doubt, ask the candidate.** Return a question for the user to answer rather than a guess.

## Output

For each bullet, return one of three treatments:

```json
{
  "bullet": "",
  "treatment": "range | qualitative | ask_user",
  "suggested": "",
  "user_confirm_required": true,
  "rationale": ""
}
```

### Range treatment

Use when there's an industry-typical range for the work:

```json
{
  "treatment": "range",
  "suggested": "improved cold-start time (typical range: 15–40% on similar iOS migrations)",
  "user_confirm_required": true,
  "rationale": "Moving from Combine to async/await on typical codebases yields this range."
}
```

### Qualitative treatment

Use when a factual outcome can be stated without numbers:

```json
{
  "treatment": "qualitative",
  "suggested": "Reduced pipeline maintenance burden for the team and removed the manual build trigger.",
  "user_confirm_required": false,
  "rationale": "These are directly stated outcomes from the original bullet."
}
```

### Ask user

Use when you cannot safely suggest anything:

```json
{
  "treatment": "ask_user",
  "suggested": "",
  "user_confirm_required": true,
  "rationale": "Need the user to provide: scope of impact, which team/users benefited, any metrics they tracked."
}
```

## Guardrails

- Every `range` suggestion MUST include `user_confirm_required: true`.
- Never promote a range to a specific number.
- If the candidate cannot confirm, the CV must fall back to qualitative language. No number goes on the page.
