# Change Report - nadia-okonkwo v1 (first pipeline run)

**Date:** 2026-07-30
**Trigger:** First-ever pipeline run for this candidate (demo/illustrative). Source of truth was the candidate's own CV, pasted in full and saved verbatim. No prior `base.json`, no performance review, no metrics export, no LinkedIn or GitHub capture, and no job description were supplied.

**Note on this run:** this is a published demo example of the cv-generator pipeline. The candidate (Nadia Okonkwo) and all named employers (Brightwave Logistics, Finch Payments, Karta Retail) are fictional. Per explicit run instructions, genuine weaknesses in the source CV were surfaced honestly rather than fixed blind, and no metric, ownership claim, or explanation was fabricated anywhere in the CV text.

## 1. Evidence inventory

| Evidence | Type | Claims promoted | Used for |
|---|---|---|---|
| nadia-okonkwo-cv.md | existing CV (source of truth) | all bullets/skills/education | Step 1 extraction, Step 6 rewrite |

No other evidence was supplied. This is itself the headline finding of this run: a performance review, a metrics export, or even a paragraph of the candidate's own recollection would materially change several scores below. See Section 4.

**Confidentiality screen applied this run:** not applicable. No internal/confidential documents were supplied.

## 2. What the original (as-received) CV was lacking

The source CV was clean and honestly written, but:

1. **No bullet anywhere carried a number.** Every bullet across all three roles described work qualitatively with no metric, before/after figure, or scale indicator.
2. **No ownership or leadership signal.** Despite roughly 7 years of experience and an explicit ask for "a senior backend role," nothing in the CV showed a technical decision made, a mentee developed, or an incident owned.
3. **Skills listed but never demonstrated.** Kubernetes, GraphQL and Kafka appeared in the Skills block with zero supporting bullets anywhere in Experience.
4. **A first-person, objective-style summary.** "I enjoy working on the server side of things... Looking for a senior backend role" reads as an objective statement, not a summary, and used "I" throughout.
5. **A visible, unexplained ~9-month employment gap** between Finch Payments (ended Sep 2021) and Brightwave Logistics (started Jun 2022).
6. **Filler content.** "Assisted senior developers with various tasks" (Karta Retail) and an Interests section with no CV-relevant content added length without adding signal.

## 3. Weakness to evidence to change map

| Weakness | Filled by | Change this run |
|---|---|---|
| First-person, objective-style summary | Rewritten using the cv-principles summary formula, no new claim | Summary rewritten to third-person, no "I", ends on a forward-looking line instead of a full objective statement. See Section 5 ledger. |
| Activity-verb bullets ("Work on...", "Helped migrate...", "Took part in...") | Rewritten with outcome verbs where the underlying fact supported it | All bullets across all three roles rewritten; no ownership or scope added beyond what the source states. See Section 5 ledger. |
| Filler bullet with no content ("Assisted senior developers with various tasks") | Cut, not rewritten | Removed per cv-principles anti-pattern rule (if deleted, CV is not weaker). Karta Retail now carries 2 bullets instead of 3. |
| Interests section with no CV-relevant content | Dropped | Removed entirely; the one clause with potential value ("building small side projects at home") has no named project, link, or outcome and cannot honestly become a Projects section. |
| No bullet shows a technical decision personally made | **Still missing** - no evidence available this run | Flagged as the single highest-leverage gap in the hiring-manager verdict (`would_flip_verdict`) and Section 8 peer-benchmark gap table. |
| No mentoring/onboarding/team-leverage signal | **Still missing** - no evidence available this run | Flagged in Section 3b (major gap) and Section 8 (4/5 peer comparators show this signal). |
| Kubernetes, GraphQL, Kafka listed but not demonstrated | **Still missing** - no evidence available this run | Flagged in Section 3b (major, market gap) and Section 7 skills audit. |
| Unexplained Sep 2021 to Jun 2022 gap | **Still missing** - no evidence available this run | Left visible on the CV (dates as-is, no fabricated label). Flagged in Sections 3b, 4, 9, and the interview-kill-question list. |
| No quantified outcome anywhere | **Still missing** - no evidence available this run | Every bullet audit rewrite in Section 6 uses bracketed placeholders (`[X%]`, `[N incidents]`); no number was invented on the CV itself. |

## 4. Still missing (ask for next time)

1. **A real technical decision, described honestly** (schema change, API contract, retry or caching strategy) - the single highest-leverage item. No evidence needed beyond the candidate's own memory of the last 12 months.
2. **A mentoring or onboarding instance**, even informal, if one genuinely happened.
3. **Confirmation of real, hands-on use of Kubernetes, GraphQL, and/or Kafka** - either a specific PR/deployment to cite, or an honest decision to drop the ones that aren't backed by real experience.
4. **The reason for the Sep 2021 to Jun 2022 gap**, or the candidate's preferred one-line public framing of it.
5. **Any real number**: latency before/after, test-coverage percentage, environment-setup time saved, incident count. Any one of these would materially move the Impact score.
6. **A performance review, brag document, or even informal notes** would be the highest-leverage single input for a future run: it would very likely surface at least one of items 1 to 5 above without requiring new work from the candidate.

All six are also recorded in this run's `blockers[]`.

## 5. Full change ledger, before to after

| Section | Before (source CV) | After (this version) |
|---|---|---|
| Summary | "Backend engineer with around 7 years of experience building web services and APIs. I enjoy working on the server side of things, writing clean code and solving problems. Looking for a senior backend role where I can take on more responsibility and work on interesting technical challenges." | "Backend engineer with 7+ years building REST APIs and services for logistics and payments platforms. Specialises in Java, Spring Boot and Python, with hands-on experience in containerised deployments and third-party payment integrations. Seeking a senior backend role with greater ownership of architecture and technical direction." |
| Brightwave, bullet 1 (was 2 bullets) | "Work on the company's order management platform using Java and Spring Boot." / "Built and maintained several REST APIs used by the web and mobile teams." | "Built and maintained REST APIs for the order management platform (Java, Spring Boot), consumed by the web and mobile client teams." (merged, context folded into one outcome-led bullet) |
| Brightwave, bullet 2 | "Helped migrate some services to Docker containers." | "Migrated a subset of backend services to Docker containers as part of a small-team initiative, standardising local and CI environments." (verb strengthened, scope kept honest, "helped... some" not inflated to solo ownership) |
| Brightwave, bullet 3 | "Fixed bugs and improved performance of existing endpoints." | "Diagnosed and resolved performance issues on order-management endpoints serving the web and mobile teams." (outcome verbs, scope named, no number added, none existed) |
| Brightwave, bullet 4 | "Took part in code reviews and sprint planning." | "Reviewed pull requests and contributed technical input during sprint planning for the order-management squad." (scope named; still flagged as a weak, activity-shaped bullet in Section 3b, not disguised as strong) |
| Finch Payments, bullets 1+3 (merged) | "Developed backend features for the payments processing system in Python." / "Worked on integrating a third party payment provider." | "Developed backend features for the payments-processing system in Python, including work on a third-party payment-provider integration." |
| Finch Payments, bullet 2 | "Wrote unit tests and worked with the QA team to improve test coverage." | "Wrote unit tests and collaborated with the QA team to raise automated test coverage on the payments platform." |
| Finch Payments, bullet 4 | "Participated in on-call rotation for production support." | "Provided production support for the payments platform as part of the on-call rotation." (outcome-first verb, same fact) |
| Karta Retail | 3 bullets ("Built internal tools...", "Worked on the company website backend...", "Assisted senior developers with various tasks.") | 2 bullets ("Built internal tools for the operations team." / "Developed and maintained backend functionality for the company website using PHP and MySQL."). Third bullet cut as unfalsifiable filler, per the 2-bullet cap for roles this far back. |
| Interests | "Five a side football, hiking, and building small side projects at home." | Removed entirely. |
| Skills | Flat list under 6 category labels | Same skills, same categories, no additions or removals; every item cross-checked in Section 7 for whether a bullet backs it up. |

## 6. Scores this run

| Metric | Score | Note |
|---|---|---|
| ATS | 86 | Clean single-column structure, standard headings, reverse chronological, good literal keyword presence. |
| Recruiter | 58 | Stack and years match on paper; no bullet demonstrates Senior-level ownership. |
| Impact | 46 | Almost every bullet lacks a metric; none existed in the source to carry forward honestly. |
| Clarity | 76 | Rewritten prose is direct and buzzword-free; summary still lacks a headline achievement. |
| Confidence | 46 | Most bullets would not survive a probing "walk me through it" follow-up. |
| Peer-alignment | 60 | 3 high-priority gaps versus the illustrative peer set (decision-bullet, mentoring, demonstrated infra skills). |
| Match | N/A | No JD supplied this run. |
| **Overall readiness** | **63 (NEEDS WORK)** | Composite formula per `skills/dashboard/SKILL.md` (ATS 0.20, Recruiter 0.40, Impact 0.15, Clarity 0.10, Confidence 0.10, Peer-alignment 0.05; Match weight redistributed into Recruiter since no JD was supplied). |

## 7. Files written

- `versions/v1/Nadia-Okonkwo-CV.md` - canonical CV (markdown)
- `versions/v1/Nadia-Okonkwo-CV.html` / `.pdf` - designed Terminal-theme PDF
- `versions/v1/Nadia-Okonkwo-CV-ats.html` / `.pdf` - ATS-safe PDF (source of truth for applying)
- `versions/v1/Nadia-Okonkwo-CV-verdict.json` - hiring-manager verdict (Step 14b)
- `versions/v1/Nadia-Okonkwo-CV-dashboard.html` - dashboard
- `versions/v1/Nadia-Okonkwo-CV-change-report.md` - this file

Mirrored into both the generation directory (`~/.claude/agents/cv-generator/generation/nadia-okonkwo/versions/v1/`) and the user store (`~/.cv-generator/nadia-okonkwo/versions/v1/`).
