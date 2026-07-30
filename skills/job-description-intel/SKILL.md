> **Bundled skill: `job-description-intel`** - reference doc for the cv-generator agent pipeline.
>
> Parses a job description and extracts must-have vs nice-to-have requirements, hidden signals (seniority, ownership level, culture), and red flags. Called by the cv-generator agent when a job description is provided.

# job-description-intel

Break down a job description into structured signal so the CV can be tailored effectively.

## Input

```json
{
  "job_description": ""
}
```

## Extraction

### Hard requirements

Split the requirements list into:
- **Must-have**: explicitly required (verbs like "required", "must have", "essential")
- **Nice-to-have**: preferred but not blocking ("preferred", "plus", "bonus", "ideally")

### Hidden signals

Read between the lines:
- **Actual seniority**: language like "lead the team", "own the roadmap", "mentor others" implies senior+ regardless of title
- **Autonomy level**: "work closely with" vs "define the direction" indicate very different expectations
- **Culture cues**: "move fast", "scrappy", "process-light" vs "rigorous", "well-documented", "careful"
- **Stage of company**: scale-up vs enterprise language
- **Real reporting line**: who the person reports to or works with

### Red flags

Flag anything that suggests the role may be misrepresented:
- Title says "Senior" but responsibilities read Mid
- "Must know 15 technologies" cover-all lists
- Unclear scope
- Unrealistic experience bands ("10+ years in a 5-year-old technology")

## Output

```json
{
  "must_have": [],
  "nice_to_have": [],
  "hidden_signals": {
    "actual_seniority": "",
    "autonomy_level": "",
    "culture_cues": [],
    "company_stage": "",
    "reporting_context": ""
  },
  "red_flags": [],
  "keyword_priority": {
    "critical": [],
    "helpful": [],
    "cosmetic": []
  }
}
```

## Rules

- `keyword_priority.critical` → must appear in the CV or it fails the first filter.
- `keyword_priority.helpful` → appear if the candidate honestly has it.
- `keyword_priority.cosmetic` → ignore unless the candidate trivially has it.
- Do not invent signals. If you cannot infer something, leave it blank rather than guessing.
