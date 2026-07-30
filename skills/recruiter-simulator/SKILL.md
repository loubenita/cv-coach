> **Bundled skill: `recruiter-simulator`** - reference doc for the cv-generator agent pipeline.
>
> Simulates recruiter behaviour at three depths: 6-second scan, 30-second skim, and hiring-manager deep-read. Produces a shortlist decision with specific reasons. Called by the cv-generator agent near the end of the pipeline.

# recruiter-simulator

Real recruiters do not read CVs. They scan them. This skill models three realistic read depths and predicts what each would take away.

## Input

```json
{
  "cv": {},
  "target_role": "",
  "target_seniority": "",
  "jd_intel_output": {}
}
```

## Reader models

### 6-second scan (initial filter)

What a recruiter looks at in 6 seconds:
- Name, current role, current company
- Most recent job title
- Years of experience (inferred from dates)
- 2-3 keyword matches against the JD

Scoring criteria:
- **Keyword presence**: do the critical keywords appear in positions the eye lands on (top, bold, job titles)?
- **Seniority signal**: does the current title match the target seniority?
- **Gap visibility**: are there unexplained gaps in the first visible section?

### 30-second skim (recruiter qualification)

Reads the first bullet of each recent role and the skills section.

Scoring:
- **Bullet 1 strength**: the first bullet of each role is the one that actually gets read. Is it a strong outcome?
- **Skills coverage**: does the skills section hit the JD's must-haves?
- **Coherence**: does the narrative (junior → mid → senior) make sense?

### Hiring-manager deep-read

Full read. Goes through every bullet. Scrutinises:
- **Impact claims**: are they specific or vague?
- **Technical depth**: do the bullets demonstrate real understanding, or recite buzzwords?
- **Consistency**: does the CV tell a believable story?
- **Red flags**: job-hopping, unexplained gaps, responsibility jumps

## Output

```json
{
  "six_second_scan": {
    "keywords_caught": [],
    "keywords_missed": [],
    "seniority_signal": "strong | mixed | weak",
    "takeaway": "",
    "pass": true
  },
  "thirty_second_skim": {
    "bullet_one_scores": [],
    "skills_coverage": 0,
    "narrative_coherence": "strong | acceptable | broken",
    "pass": true
  },
  "hiring_manager_read": {
    "impact_specificity_score": 0,
    "technical_depth_score": 0,
    "red_flags": [],
    "standout_bullets": [],
    "weak_bullets": []
  },
  "shortlist_decision": "shortlist | maybe | reject",
  "reasons": [],
  "highest_leverage_fixes": []
}
```

## Rules

- All three reads must run. A CV that passes the 6-second scan can still fail the deep read, and vice versa.
- `highest_leverage_fixes` should be the top 3 changes ranked by expected impact on outcome, not a list of every possible improvement.
- Shortlist decision must be traceable to specific reasons. Never return a decision with an empty `reasons[]`.
