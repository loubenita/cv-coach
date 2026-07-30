> **Bundled skill: `dashboard`** - reference doc for the cv-generator agent pipeline.
>
> Generates a comprehensive, self-contained HTML dashboard from all cv-generator pipeline outputs. Built to answer three questions for the candidate: "Am I ready to apply?", "What specifically should I focus on?", and "How much time do I need before I'm competitive?". Includes a readiness verdict, six score cards with current vs projected values, recruiter simulation, role fit analysis, JD match, bullet-by-bullet quality audit, skills audit, peer benchmark, experience timeline, market context, a tiered action plan (today / this week / this month / this quarter), interview defence prep, and application strategy. Designed to print cleanly to PDF across multiple pages. Called at the end of the cv-generator pipeline.

# dashboard

The dashboard is the candidate's decision tool. A CV tells a recruiter what the candidate has done. This dashboard tells the candidate whether they are competitive for the target role, what is holding them back, and what to do about it in descending order of impact.

It must answer three questions without ambiguity:

1. **Am I ready to apply right now?**
2. **If not, what specifically should I focus on?**
3. **How much time do I need before I'm genuinely competitive?**

Every section exists to support one of those three answers. If a data point is interesting but not actionable, it does not belong in the dashboard.

## Input

```json
{
  "candidate_name": "",
  "target_role": "",
  "target_seniority": "",
  "location": "",
  "generated_at": "",
  "has_job_description": false,
  "pipeline_outputs": {
    "extract": {},
    "role_detection": {},
    "trend_lookup": {},
    "ats_validator": {},
    "benchmark": {},
    "recruiter_simulator": {},
    "job_description_intel": {},
    "job_matcher": {},
    "peer_benchmark": {},
    "post_miner": {},
    "impact_generator": {},
    "feedback_loop": {},
    "linkedin_optimiser": {},
    "hiring_manager_verdict": {},
    "change_report": {},
    "evidence_index": {},
    "final_report": {}
  }
}
```

Every pipeline output is optional. If a step did not run, render its section with a one-line "Not run for this session" note rather than omitting it silently. The candidate should always see what was and wasn't assessed.

## Output

A single HTML file saved to `versions/<identity>/<identity>-dashboard.html`.

Requirements:
- Self-contained: all CSS inlined, no external fonts, no JavaScript
- Print-ready across multiple pages (A4, correct margins, explicit page-break rules)
- Works in any modern browser
- Professional, clean, high information density without feeling cramped

## Canonical template - start here, do NOT free-form the HTML

**The dashboard's structure is locked in `templates/dashboard.html` (i.e. `cv-generator/templates/dashboard.html`). Every run MUST start from that file and fill it in - never re-invent the layout, CSS, nav, or section set.** Free-forming the HTML each run is exactly what made past dashboards drift in structure and size; the template exists to stop that.

Fixed by the template (do not change per run):
- the entire inline `<style>` block - the visual system is locked;
- the **side nav**: four collapsible groups, in order - **(1) Overview & scores**, **(2) Findings**, **(3) Hiring manager**, **(4) Action plan** - each sub-link `href` matching a section `id`;
- the set, order, `id`s and headings of the `<section>`/`<h2>`/`<details>` blocks in `<main>`.

Filled per run:
- the `{{CANDIDATE_NAME}}` and `{{GENERATED_DATE}}` tokens (title, brand line, footer);
- the `{{CV_PDF_FANCY}}`, `{{CV_PDF_ATS}}`, `{{CV_MD}}` hrefs in the **Download CV** nav block - the three CV files for this identity (relative, same folder);
- the content inside each section, from the pipeline outputs. What is currently inside the template's sections is a worked example from a real run, kept to show the intended depth and formatting - replace it, keep the shells, repeat rows/cards as the data needs;
- if a step did not run, KEEP its section and render a one-line "Not run for this session" note rather than deleting it.

Save the filled copy to `versions/<identity>/<identity>-dashboard.html`.

> **Precedence:** where anything below in this document conflicts with `templates/dashboard.html`, the template wins - follow the template. In particular the template is a **single-nav-rail, two-column** layout; the older "two side rails" / three-column skeleton described further down is **superseded** by the template.

## Sections (in order)

### Two side rails (persistent, one each side of the main column)

> **⚠️ Superseded by `templates/dashboard.html`.** The locked template uses a single left **navigation** rail (the four collapsible groups), not the two content-rails described in this subsection. The *content* below - "Evidence used to build this CV" and "Hiring manager: what to add and how to get it" - is still valuable; render it inside the main column (within the Executive summary, Hiring-manager, and Action-plan sections) rather than as side rails, unless the template is later changed to reintroduce rails.

Two rails frame the main content, each with **as many collapsible subsections as the data needs**. On web they are sticky so the user can scan sources and actions alongside any section; on print they drop below the main content as full-width sections. These are the two panels the candidate asked for.

#### Side A (left rail) - "Evidence used to build this CV"

Every input that fed the CV, so the user sees exactly what it was built from. Driven by `evidence_index` and the Step 14c change report. One subsection per source, shown only when that source exists:

- **Existing CV** - the base document.
- **LinkedIn** - a sub-item per captured section that was used: Profile / About, Experience, Projects, Recommendations, Endorsed skills, Featured, Activity. For each, show what was pulled and which CV bullets it supported (e.g. "Projects: RentLoop full write-up + App Store link", "Recommendations: 4 verbatim", "Endorsed skills: 40-skill map").
- **Performance review / appraisal**, **Metrics**, **GitHub / portfolio**, **Job description(s)**, **Other evidence** - one subsection each when present.

Each item links to its `evidence/index.json` entry (type, coverage period, `claims_promoted`). Sources provided but not used appear greyed with a "provided, not yet used" note (mirrors `blockers[]`).

#### Side B (right rail) - "Hiring manager: what to add and how to get it"

The Step 14b adversarial verdict turned into an action list, with as many subsections as gap themes exist (e.g. Impact & metrics, Seniority & ownership, Modern stack for 2026, Thought leadership, Team leverage). Each gap card has four lines:

1. **What's missing** - the `cv_quote` or the absent signal.
2. **Why it matters now** - `why_it_matters_now`; items tagged `market_gap` get a "2026 expectation" chip.
3. **How to improve** - the `do_differently` / `how_to_improve`.
4. **How to get the data** - the `how_to_get_evidence`, verbatim and specific: speak to your manager in your next 1:1, pull GitHub PR/commit history, read Firebase Crashlytics crash-free rate, check analytics for conversion/retention, App Store Connect for downloads/ratings, incident postmortems / on-call logs, OKR or performance-review outcomes.

Sort `market_gap` and dealbreaker items to the top. This rail is the direct answer to "what would a hiring manager want more of, and exactly where do I find it."

### 1. Executive summary (page 1, above the fold)

The most important section. A recruiter would skim it, and so will the candidate. The layout depends on whether a job description was supplied:

#### Without a JD - single-score mode

Three blocks side by side:

**Readiness verdict block.** Large, unambiguous label:
- `READY` (green): apply now
- `ALMOST THERE` (amber): 2-5 quick fixes before applying
- `NEEDS WORK` (orange): 2-4 weeks of focused work first
- `EARLY STAGE` (red): significant gaps, longer plan needed

Below the label, a single-sentence verdict written in plain English (e.g. "Strong profile with two high-impact fixes that will unlock senior-level applications.").

**Overall readiness score block.** A single 0-100 number with colour band and a one-line definition. Must explicitly say what the number is measuring: "Overall readiness for Senior iOS Engineer (IC) at role level. Composite of ATS, recruiter, content, and peer-gap signals. 70+ is competitive for this role and seniority."

**Time-to-ready block.** Estimate in hours of effort (not calendar time), broken into tiers:
- Today: N hours of quick-win fixes
- This week: N hours of content improvement
- Longer: N hours of skill-building (if needed)

Below the three blocks, a "Top 3 next actions" strip: the three highest-leverage fixes pulled from the action plan, each shown as a small card with the action, the section of the CV it affects, and the expected score impact.

A **JD callout** must appear at the bottom of the hero in this mode, styled as a muted card: "No job description provided. Paste a JD or a role URL to unlock JD-specific match scoring." The callout links to Section 5 so the user sees where match analysis will appear once a JD is supplied.

The callout has two variants, distinguished by class:
- `.jd-callout-empty` - dashed border, muted background, greyscale icon. Used when no JD is supplied. Copy invites the user to paste a JD and explains what the dashboard will unlock.
- `.jd-callout-active` - solid border, green-soft background, tick icon. Used when a JD is supplied. Copy confirms the posting and shows a "Clear JD" affordance.

Both variants share the same internal structure (icon · title · short description · actions row) so the transition between states is visually continuous.

#### With a JD - two-score mode

The hero shows **two scores side by side**, clearly labelled so the user cannot confuse them:

- **Overall readiness** - same composite score as above, same formula, same colour band. Label: "How you read for Senior iOS Engineer (IC) at role level."
- **Role match** - the JD-specific score from `job-matcher`. Label: "How well you match THIS role: `{JD title}` at `{company}`." Shown in its own colour band (based on its own threshold, not the overall one).

Under the two scores, a **two-line read** explicitly reconciling them for the user:
- One line on the overall score and what it means in general (apply now / polish / fix structural).
- One line on the match score and how it compares to overall (e.g. "Strong overall but specific JD match is weaker because this role asks for SwiftData and Widgets, which are absent from your CV. See Section 5 for the gap table.").

Below the two scores, the time-to-ready block and top-3 next actions remain. Prioritise the top-3 actions toward closing the JD gap when in two-score mode.

A **JD provenance card** must appear above the scores in this mode, showing:
- JD source URL (clickable) or "Pasted text · {N} words"
- JD title + company
- Date captured
- A "Clear JD" affordance so the user knows they can return to single-score mode

This card is the answer to the user's "have a section for the job description provided (link or whatever)". It must be clearly branded so the rest of the dashboard is obviously in the context of this specific role.

### 2. Score breakdown

Six score cards in a row (wrap to two rows on print). Each card shows:
- Current score (0-100) with large number and colour band
- Projected score after completing the action plan's quick wins
- Benchmark for this role and seniority ("Typical competitive candidate: 78")
- Optional one-line note explaining the score or its change. **Colour each note by its sentiment, never one flat colour for all:**
  - improvement / positive ("Up 5: ambiguity resolved") → green
  - genuine caveat or at-risk signal (e.g. a score below 70, an unsupported claim) → amber
  - regression / score dropped → red
  - purely neutral / unchanged ("Unchanged: no keywords added") → muted grey
  Do not paint every note orange (a wall of warning colour under healthy green scores reads as if something is wrong) and do not paint every note grey (bland, and throws away the good/bad signal). Match the colour to whether the note is good, bad, or neutral.

Cards: **ATS**, **Recruiter**, **Impact**, **Clarity**, **Confidence**, **Match** (only if a JD was provided).

Colour bands:
- 80+: green
- 70-79: light green
- 60-69: amber
- 50-59: orange
- below 50: red

### 3. Recruiter simulation

Three panels side by side, one per read depth. Each panel shows:

- **Header**: "6-second scan" / "30-second skim" / "Hiring-manager read"
- **Verdict badge**: pass / maybe / reject
- **What they caught**: list of keywords and signals the recruiter picked up
- **What they missed**: gaps the recruiter did not see but should have
- **Red flags**: anything that would make them pause or reject
- **One-line takeaway in their own words** (rendered in a quote-style box): a plain-English summary of what this reader would say about the candidate

### 3b. The hiring manager's verdict (adversarial final read)

Renders the `hiring_manager_verdict` output (Step 14b): a veteran hiring manager who read the **final generated CV** with intent to reject. This section is deliberately uncomfortable; do not soften it in rendering.

- **Verdict banner**: the verdict (`strong_yes` / `interview` / `weak_maybe` / `no`) as a large badge with the `verdict_one_liner` beside it. Colour: green / blue / amber / red respectively.
- **The summary**, rendered as a quote block in the hiring manager's voice, verbatim from the skill output.
- **"What would flip the verdict"** callout card: the single `would_flip_verdict` item, visually prominent - this is the one thing to do next.
- **Gap table**, one row per `gaps[]` entry, sorted dealbreakers first: severity chip · the verbatim `cv_quote` (rendered in monospace so it is recognisably lifted from the CV) · `location` · the `objection` · **Do differently** (the concrete action) · **Evidence needed** (where the real number/proof comes from). This is the "pointing out from the generated CV what should be done differently" view: quote on the left, fix on the right.
- **Interview kill questions**: the `interview_kill_questions[]` as a checklist. Cross-link to Section 12 (interview defence prep), which must incorporate them.
- **What survived**: `strengths_that_survive[]` as a short muted list. If empty, render "Nothing survived the adversarial read unchallenged" rather than omitting.

If Step 14b did not run, show the standard "Not run for this session" note.

### 3c. Change report and evidence ledger

Renders the Step 14c change report. Reuses the Section 3b gap-table visual pattern (verbatim quote on the left, fix on the right) with one added middle column. Always open by default; this section is the payoff of the evidence-capture flow.

- **Evidence inventory strip.** One chip per `evidence_index.items[]` entry: type, `coverage_period`, `claims_promoted`, and `used_for`. This is the "what you have done and what I used" view. Items with `claims_promoted: 0` render muted with a note that nothing from them reached the CV.
- **Weakness to evidence to change table.** One row per mapped weakness. Columns: original weakness (`cv_quote` in monospace) · filled by (`source_label` chip, green-soft) OR "still missing" (red-soft chip) · change applied (before and after text) · rationale. Sort filled rows first, still-missing rows last.
- **"Ask for next time" callout.** An amber card listing each still-missing gap with the best source to close it (performance review, metrics export, OKR results, postmortem). Cross-link to the blockers in the final report so the two lists never diverge.

If Step 14c did not run, show the standard "Not run for this session" note.

### 4. Role fit analysis

A compact block answering four questions:

- **Seniority alignment**: appropriate / over-positioned / under-positioned, with a one-line explanation
- **Industry fit**: strong / adequate / weak
- **Career trajectory coherence**: linear / lateral / pivot (with a note on whether the pivot is explained)
- **Likely hiring-manager red flags**: bullet list, empty if none

### 5. JD match (only if a JD was provided)

Four sub-blocks:

- **Match score** (large number) with the target JD title
- **Must-haves**: checklist of each must-have requirement with one of three states: hit / missing / closeable-with-rewrite
- **Nice-to-haves**: compact checklist
- **Gap-to-rewrite table**: for each must-have marked closeable-with-rewrite, show the JD requirement, the candidate's closest existing bullet, and the suggested rewrite. This is the highest-ROI CV editing any candidate can do.

If no JD was provided, render the section with "Not run for this session. Provide a job description to see match analysis."

### 6. Bullet-by-bullet quality audit

A table with one row per bullet from the candidate's two most recent roles. Omit older roles to keep focus.

Columns:
- **Role**: company and title (only shown on the first row of each role, then collapsed)
- **Bullet**: the bullet text verbatim
- **Rating**: high / medium / low, colour-coded badge
- **Notes**: one sentence on what the bullet does well or what's missing. Avoid short tag-like text here - use complete sentences so the candidate can act on it without decoding shorthand.

**Suggested rewrite policy.** A `<div class="rewrite">` block sits inside the bullet cell when a rewrite is warranted:
- **Low** bullets always get a rewrite (this is the primary fix the candidate came here for).
- **Medium** bullets get a rewrite when the upgrade path is clear (e.g. a bounded number, named flow, or measurable outcome would lift it to High). Not every Medium needs one - only where the suggestion is concrete.
- **High** bullets get a rewrite only when a single small addition (usually a numeric outcome) would move them to the strongest bullet on the CV. Use sparingly.
- **Tense fixes** are also rendered as a rewrite block labelled `Tense fix only:` so the candidate sees it as a mechanical correction, not a content rewrite.

Every rewrite uses placeholder brackets (`[X% lift in Y]`, `[named flow]`) when the real number is not known. Never invent a metric.

**Tense consistency check.** Before rating bullets, scan all bullets within a single role and confirm tense is uniform. The convention on professional CVs is simple past for every bullet in every role, including the current one ("Delivered", "Shipped", "Led"). Flag any present-tense bullet inside an otherwise-past-tense role as a tense-fix row. This is cheap to fix and noticeable in the 6-second scan.

**Summary badge.** The `<details>` summary carries a pill showing the audit shape, formatted as `N bullets · M rewrites · K tense fixes` (omit any segment that's zero). This lets the candidate see the audit's scope before they expand the section.

Rows for low-rated bullets get a thin red left border. Rows for high-rated bullets get a thin green left border. Medium sit in between (amber). Use this pattern throughout the dashboard for visual consistency.

### 7. Skills audit

Four-column layout:

**Column 1: Validated skills.** Skills present in the candidate's skills section AND demonstrated by at least one bullet. These are the strongest claims.

**Column 2: Listed but not demonstrated.** Skills in the skills section with no supporting bullet. These look weak in an interview. Recommend either writing a bullet that demonstrates the skill, or removing the skill.

**Column 3: Missing critical skills.** Skills required by the JD or flagged by trend-lookup as high-demand, not currently in the CV. Flagged critical / helpful.

**Column 4: Rename opportunities.** Skills the candidate has but labels differently. Shows: current label, suggested label, why the rename matters (e.g. "recruiters search for the latter term, not the former"). These are 5-minute fixes with real impact.

Below the four columns, a small keyword density strip showing the top 10 in-demand keywords for the target role from trend-lookup, each with a tick or cross for presence in the CV.

### 8. Peer benchmark

Four sub-blocks that consume the full `peer-benchmark` output. Skip the whole section if peer-benchmark did not run.

**8a. Named comparator cards.** Five cards, one per comparator, shown in a vertical stack or two-up grid. Each card surfaces the real-person signal the candidate asked for:

- **Display name + current role + employer.** Use first name + last initial for privacy (e.g. "Tim M. · Senior iOS Engineer at Monzo"). Full name is not required, but initials are the minimum.
- **Profile link.** A `<a href>` back to the public LinkedIn profile. Small, in muted text.
- **Selection reason badge.** One of: `domain peer`, `prestige peer`, `one rung above`. Colour-code:
  - `domain peer` → green-soft background
  - `prestige peer` → blue-soft background
  - `one rung above` → amber-soft background
- **Tier tag.** Small pill showing `tier_1` / `tier_2` / `tier_3` so the candidate can see the brand weight at a glance.
- **Why they are in this peer set.** One line pulled from `why_included` (e.g. "Direct competitor to Northwind Fitness, same tier." or "Fintech at tier_2 brand, included for brand weight not domain match.").
- **What they have that you can learn from.** Bulleted list of 3-5 signals pulled from `differentiators`. These should be concrete (e.g. "Ships Live Activities for deliveries.", "Open-source library with 500+ stars.", "Published 2 engineering posts in the last 12 months."). Avoid generic phrases like "good communicator."
- **Lesson for the candidate.** One sentence. "Pattern to copy:" or "Consider mirroring:" or "Gap to close:".

**8b. Peer comparison matrix.** A table that makes the "you vs them" comparison visual and scannable.

- Columns: each comparator (using their display name), plus a `You` column. The `You` column is visually distinct (green-soft background) so the candidate can scan along any row and immediately see where they stand.
- Rows: the signals that matter for this role, typically 8-15 rows pulled from the union of `differentiators` across comparators. Rows are ordered by how many comparators show the signal (universal at the top, divergent at the bottom).
- Cells: `yes` / `partial` / `no`, colour-coded. A cell can optionally include one short phrase for context (e.g. "yes · 2 posts").
- Keep the matrix inside a horizontally scrollable container so it still prints legibly on A4.

This matrix is the centrepiece of the peer benchmark. It was added because the abstract "5 of 5 have X" framing was harder for candidates to act on than a named comparison.

**8c. Cross-profile patterns.** Four labelled rows pulled from `cross_profile_patterns`:
- **Universal** (5/5): table-stakes signals
- **Majority** (3-4/5): strong expectations
- **Divergent** (1-2/5): interesting but low priority
- **Candidate strengths** (0/5): things only the candidate has, marked as competitive advantages to emphasise

**8d. Gap table.** One row per entry in `candidate_gaps`. Columns: gap description, seen in N/5, gap_type badge (rename / surface_not_demonstrated / addable / long_term), effort badge (quick_win / medium / long_term), priority badge, the suggestion text, and `addable_now` as a yes/no column. Sort by priority then effort (quick wins at the top).

Render quick-wins with a thin green left border so the candidate can see what to fix in the next 10 minutes vs what's a longer-term investment.

#### Comparator selection badges (for 8a)

The candidate has explicitly asked for the peer set to be biased toward their current domain plus high-profile brands. The `selection_reason` returned by `peer-benchmark` should already follow this bias, but the dashboard surfaces it visually so the candidate can see why each comparator made the cut:

- **domain peer** - same industry/sub-sector as the candidate (e.g. iOS engineer at Depop or ASOS when the candidate is at Northwind Fitness). Shows the direct market.
- **prestige peer** - high-brand employer regardless of domain match (Apple, Google, Meta, Monzo, Revolut, Deliveroo). Shows the aspirational bar even when domain differs.
- **one rung above** - Staff/Principal/Lead at a peer company. Shows the next step on the ladder.

If the peer set skews too far in one direction (e.g. 4 prestige peers and no domain peer), flag that in the 8a intro line so the candidate knows to weight the signal accordingly.

### 9. Experience narrative

A horizontal timeline visualisation followed by a short analysis block.

**Timeline.** Each role rendered as a segment on a horizontal bar, proportional to duration. Colour-code each segment by bullet confidence average (green / amber / red). Label each segment with company, title, and dates. Show any unexplained gaps as grey slivers with a "?" marker.

**Narrative analysis.** Four short lines:
- Trajectory shape: linear progression / lateral / pivot / portfolio
- Promotion velocity: fast / typical / slow for this role
- Strongest role: company + what makes it strong
- Weakest role: company + what's dragging it down

### 10. Market context

A compact block with current market signal for this role, pulled from trend-lookup.

- **In demand**: top 8 keywords rising in postings, coloured green if the candidate has them, red if missing
- **Declining**: 3-4 keywords losing traction (with a note not to lead with these)
- **Seniority expectations**: one-paragraph description of what a strong candidate at this level is expected to have
- **Salary signal** (if available): typical range from recent postings

### 11. Action plan (the heart of the dashboard)

The most important section. Organised into four effort tiers, not by priority alone. Each tier is a distinct block.

**Today (under 1 hour).** 3-5 items. Pure quick-wins: rename a skill, delete a weak bullet, add a missing keyword, fix a date format, correct an email address. Each item shows: action, location in CV, expected score delta, estimated minutes.

**This week (under 10 hours).** 3-5 items. Bullet rewrites, adding measurable outcomes, restructuring the skills section, updating the summary. Each item shows: action, location, expected score delta, estimated hours.

**This month (under 40 hours).** 2-4 items. Writing a case-study bullet for a high-value project, getting a certification the candidate is close to, shipping a small OSS piece to close a peer gap. Each item shows: action, expected score delta, estimated time, and a note on addressability.

**This quarter (ongoing).** 1-3 items. Real skill building: learning a new framework, speaking at a meetup, publishing a piece. These are flagged as "bet items" because they take effort and the payoff is longer-term.

Each item has an expected score delta badge (e.g. "+4 ATS", "+3 Recruiter") so the candidate can see the quantitative impact of working through the plan.

**Visual pattern.** On wide screens the four tiers sit side-by-side in a grid (usually 3 tiers visible, with the quarter tier optionally wrapping below). Each tier is a **soft panel** (subtle background tint, rounded border, generous padding) containing flat white action-item cards. The key constraint: the tier panels must be **equal height** across the row regardless of how many action items each contains, so a tier with 3 items reads as aligned with a tier with 5. Empty space at the bottom of shorter tiers is intentional; it signals "nothing else to do in this tier" rather than "this column is ragged."

Implementation: force `align-items: stretch` on the grid, set each tier-block to `display: flex; flex-direction: column; height: 100%`, and let the action items stack naturally inside. Do not nest heavy card borders (tier panel + action item both with strong borders reads as double-card). Tier panel gets a soft fill, action items get a flat white fill with a thin coloured left border.

At the bottom of this section, a total projected score delta across all items. If the candidate does everything in Today + This Week, show the projected readiness score.

### 12. Interview defence prep

A short section preparing the candidate for questions they'll be asked. Three blocks:

**Claims that need evidence.** Every bullet the recruiter-simulator flagged as "specific but unverifiable" (typically measurable claims). Each shows: the claim, what an interviewer might ask, and what evidence the candidate should have ready.

**Stretch answers.** For each low-confidence bullet not yet rewritten, show a honest-but-strong way to talk about the work verbally, even if the CV text is weak.

**Kill questions.** The `interview_kill_questions[]` from the hiring-manager verdict (Section 3b) - the probing questions the final CV invites from a skeptical interviewer. Each shows the question and which CV line triggers it. The candidate must have answers to these before applying.

### 13. Application strategy

A compact block advising on application approach:

- **Apply now**: roles that match current readiness (the candidate's current profile wins)
- **Apply after quick wins**: roles that open up after the Today + This Week fixes
- **Stretch applications**: roles that match after This Month + This Quarter work
- **Volume recommendation**: how many applications per week makes sense given current readiness (too few = slow, too many = diluting signal)
- **Safe vs stretch ratio**: suggested mix (e.g. 60% safe, 40% stretch)

### 14. LinkedIn consistency check

One-line block:
- Green tick if `linkedin_optimiser` ran and produced `consistency_check.matches_cv: true`
- Amber if optimiser ran but there are discrepancies (list them)
- Grey "Not run" if optimiser did not run, with a suggestion to run it so LinkedIn matches the CV

## Design spec

```css
/* Palette */
--green:       #16a34a;
--green-soft:  #dcfce7;
--amber:       #d97706;
--amber-soft:  #fef3c7;
--orange:      #ea580c;
--red:         #dc2626;
--red-soft:    #fee2e2;
--text:        #1a1a1a;
--muted:       #6b7280;
--border:      #e5e7eb;
--bg-alt:      #f9fafb;

/* Type */
font-family: 'Helvetica Neue', Arial, sans-serif;
body font-size: 10pt;
line-height: 1.5;

/* Section headings */
font-size:      10pt;
font-weight:    700;
text-transform: uppercase;
letter-spacing: 0.07em;
border-bottom:  1px solid var(--border);
padding-bottom: 1.5mm;
margin:         8mm 0 3mm 0;

/* Score cards */
flex: 1 1 28mm; border: 1px solid var(--border); border-radius: 2mm; padding: 3mm 4mm;

/* Verdict block (section 1) */
The verdict label is 18pt, 700 weight. Background is the colour-band colour at 10% opacity.

/* Row borders */
Low-confidence rows: 2px solid var(--red) left border.
High-confidence rows: 2px solid var(--green) left border.
Quick-win action items: 2px solid var(--green) left border.
Long-term action items: 2px solid var(--muted) left border.

/* Tables */
font-size: 9.5pt; border-collapse: collapse;
th: text-transform: uppercase; font-size: 8.5pt; letter-spacing: 0.05em; color: var(--muted); padding: 1.5mm 2mm; border-bottom: 1px solid var(--border);
td: padding: 2mm; border-bottom: 1px solid var(--border); vertical-align: top;
```

## Print rules

```css
@page { size: A4; margin: 16mm 18mm; }

@media print {
  .page           { margin: 0; padding: 0; max-width: none; }
  .score-card,
  .sim-panel,
  .action-item,
  .comparator-card,
  tr              { page-break-inside: avoid; break-inside: avoid; }
  h2              { page-break-after: avoid; break-after: avoid; }

  /* Explicit page breaks for readable multi-page structure */
  .page-break-after { page-break-after: always; break-after: page; }
}
```

Hard page breaks to aim for:
- Section 1 + 2 fit on page 1
- Section 3 + 4 + 5 fit on page 2
- Section 6 on its own page (can run long)
- Section 7 on its own page
- Section 8 on its own page (long)
- Section 9 + 10 on the same page
- Section 11 on its own page (the action plan deserves its own space)
- Sections 12 + 13 + 14 on the last page

## Inline structure (skeleton)

Matches `templates/dashboard.html`. Two columns on web: a fixed left `nav.rail` (grouped section nav) + a fluid `main.content`. The four nav groups **categorise** the sections; they do **not** reorder them - content order in `<main>` is exactly as listed below (the template's order, kept from the v2 layout, including its numbering which skips a standalone "10").

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{CANDIDATE_NAME}}: CV Dashboard</title>
  <style>/* locked inline CSS - see templates/dashboard.html, do not regenerate */</style>
</head>
<body>
<div class="layout">                                   <!-- display:flex - 2 columns on web -->

  <nav class="rail">                                  <!-- single left rail: grouped section nav -->
    <div class="brand">{{CANDIDATE_NAME}}</div>
    <div class="brand-sub">CV Dashboard &middot; generated {{GENERATED_DATE}}</div>

    <div class="dlgroup">                             <!-- Download CV: 3 formats, relative paths -->
      <div class="dl-label">Download CV</div>
      <a class="dl dl-primary" href="{{CV_PDF_FANCY}}"><span class="dl-name">Designed PDF</span><span class="dl-tag">.pdf</span></a>
      <a class="dl" href="{{CV_PDF_ATS}}"><span class="dl-name">ATS PDF (basic)</span><span class="dl-tag">.pdf</span></a>
      <a class="dl" href="{{CV_MD}}"><span class="dl-name">Markdown source</span><span class="dl-tag">.md</span></a>
    </div>

    <details class="navgroup" open><summary>Overview &amp; scores</summary>
      <a href="#verdict">Executive summary</a>
      <a href="#scores">Score breakdown</a>
      <a href="#recruiter">Recruiter simulation</a>
    </details>
    <details class="navgroup" open><summary>Findings</summary>
      <a href="#rolefit">Role fit</a>
      <a href="#jdmatch">JD match</a>
      <a href="#bullets">Bullet audit</a>
      <a href="#skills">Skills audit</a>
      <a href="#peers">Peer benchmark</a>
      <a href="#timeline">Timeline &amp; market</a>
      <a href="#linkedin">LinkedIn check</a>
    </details>
    <details class="navgroup" open><summary>Hiring manager</summary>
      <a href="#hmverdict">Hiring-manager verdict</a>
      <a href="#interview">Interview prep</a>
    </details>
    <details class="navgroup" open><summary>Action plan</summary>
      <a href="#actionplan">Action plan</a>
      <a href="#strategy">Application strategy</a>
    </details>
  </nav>

  <main class="content">                              <!-- content order is fixed (v2 order) -->
    <h2 class="section-heading" id="verdict">1. Executive summary</h2>          <!-- grp 1 -->
    <h2 class="section-heading" id="scores">2. Score breakdown</h2>             <!-- grp 1 -->
    <h2 class="section-heading" id="recruiter">3. Recruiter simulation</h2>     <!-- grp 1 -->
    <h2 class="section-heading" id="hmverdict">3b. The hiring manager's verdict</h2> <!-- grp 3 -->
    <h2 class="section-heading" id="rolefit">4. Role fit analysis</h2>          <!-- grp 2 -->
    <h2 class="section-heading" id="jdmatch">5. JD match</h2>                   <!-- grp 2; "Not run" note if no JD -->
    <details open id="bullets"><summary>6. Bullet-by-bullet quality audit</summary>...</details>   <!-- grp 2 -->
    <details id="skills"><summary>7. Skills audit</summary>...</details>        <!-- grp 2 -->
    <details open id="peers"><summary>8. Peer benchmark</summary>...</details>  <!-- grp 2 -->
    <h2 class="section-heading page-break-before" id="timeline">9. Experience timeline &amp; market context</h2> <!-- grp 2 -->
    <h2 class="section-heading page-break-before" id="actionplan">11. Action plan</h2>  <!-- grp 4 -->
    <details id="interview"><summary>12. Interview defence prep</summary>...</details>  <!-- grp 3 -->
    <h2 class="section-heading" id="strategy">13. Application strategy</h2>     <!-- grp 4 -->
    <h2 class="section-heading" id="linkedin">14. LinkedIn consistency check</h2>       <!-- grp 2 -->
  </main>

</div>
</body>
</html>
```

Layout: `.layout` is `display:flex` - a fixed 200px `nav.rail` (sticky, full-height, dark `#111827`) + a fluid `main.content` (max-width 1760px). Nav groups are `<details class="navgroup" open>` so each collapses independently, no JavaScript. Below ~1100px the inner grids collapse to 2-up; in `@media print` the nav rail is hidden (`nav.rail{display:none}`) and content prints single-column across A4 pages via the `.page-break-before` hooks.

## How to compute the readiness verdict

The verdict in section 1 is a derived value, not a pipeline output. Compute it from the other signals:

```
readiness_score = weighted_average(
  ats_score        * 0.20,
  recruiter_score  * 0.25,
  impact_score     * 0.15,
  clarity_score    * 0.10,
  confidence_score * 0.10,
  match_score      * 0.15 if JD provided else 0,
  peer_alignment   * 0.05
)
```

`peer_alignment` is 100 minus (10 × number of high-priority peer gaps), floored at 0. If peer-benchmark did not run, redistribute its 5% to recruiter_score.

Verdict thresholds:
- 80+: `READY`
- 65-79: `ALMOST THERE`
- 50-64: `NEEDS WORK`
- below 50: `EARLY STAGE`

Projected readiness score is the readiness calculation re-run with the projected component scores from the action plan's Today + This Week tiers applied.

## How to compute time-to-ready

Sum the time estimates from the Today + This Week action items for the applicant's current verdict:

- If `READY`: 0 hours quick-wins, N hours optional polish
- If `ALMOST THERE`: total hours of quick wins to hit `READY`
- If `NEEDS WORK`: total hours of Today + This Week + relevant This Month items to hit `ALMOST THERE`, with a note that a further round of work gets to `READY`
- If `EARLY STAGE`: show all four tiers summed, with a clear note that the candidate should not apply yet

## Rules

- **Write for the candidate, not the pipeline. No process narration.** The dashboard is the candidate's decision tool, not a run log. It must read as a snapshot of where the CV stands *now* - never a diff against a previous version. Concretely, the rendered dashboard must NOT contain:
  - version-comparison narration ("up 1 from the stale v8 number", "unchanged this run", "carried forward, not re-fetched", "changed this run", "(updated in v8)", "regressed as of v7");
  - "how this was computed" preambles under section headings ("Freshly computed this run against the actual, current CV text", "Fresh adversarial read this run", "source: skills/benchmark");
  - an "update note" / "what triggered this run" block anywhere in the body.
  Provenance that genuinely matters (what did and didn't run, generation date, whether peer data is stale) lives in exactly one place: the footer note and the per-section "Not run for this session" line. Everywhere else, state the current fact plainly. If a score went up, the note says *why the CV is strong there now* ("Scope is unambiguous: 'defining the contracts, setting the architecture'"), not *what it used to say*.
- **Keep notes to one sentence.** Score-card notes, bullet-audit notes, and gap-table objections are one plain sentence each. If a point needs two sentences, it belongs in the action plan or the hiring-manager verdict, not in a note cell. Cut hedging clauses ("all true and useful, but", "not a red flag on its own", "worth being deliberate about") down to the claim.
- **Say each finding once.** The same gap must not be written out in full in more than one place. The interview kill questions live in Section 12 only; Section 3b references them by count and cross-links, it does not reprint the list. A gap named in the hiring-manager verdict (3b) is referenced from role fit (4), skills (7), and the action plan (11) as a short pointer ("see 3b"), never re-argued. When a bullet audit note and a gap-table row cover the same bullet, one carries the detail and the other points to it. Duplication is the main thing that makes this dashboard feel long; cut it.
- **The template example is deliberately over-written - do not match its length.** The worked-example prose inside `templates/dashboard.html` predates these concision rules and runs long (multi-sentence notes, "this run" phrasing, re-verification asides). Copy its *structure, classes, and section set*, not its word count or tone. Where its example text conflicts with the Concision rules here, the rules win: compress every note and preamble you fill in to the budgets below.
- **Length budget (hard caps per region).** Section-intro paragraphs: delete them unless a section literally did not run (then one "Not run" line). Score-card note: ≤ 20 words. Bullet-audit note: ≤ 25 words. Gap-table objection / do-differently / evidence cell: ≤ 25 words each. Role fit, market context, application strategy: ≤ 4 short lines total per block, no paragraph over 30 words. The hiring-manager quote block (3b) and the recruiter one-line takeaways are the *only* places longer prose is allowed, because that voice is the deliverable. Everywhere else, if it runs past the cap, cut it, don't wrap it.
- **Every data point must be actionable or contextual.** If a number or table row doesn't help the candidate decide, remove it.
- **No fabrication. No hallucinated scores.** Every score in the dashboard must trace back to a specific pipeline output or the documented composite formula above. If `recruiter_score` is missing from the pipeline, the Recruiter score card says "Not run" and does not display a number. The `readiness_score`, projected scores, and `time_to_ready` are the only derived values, and each derivation is defined in this document.
- **Every web-sourced claim must be cross-verified before appearing in the dashboard.** Peer signals, market salary ranges, trend keywords, and conference names all go through a second live-source check. If a claim cannot be confirmed by opening the URL or a second source, it is dropped, not hedged.
- **Two scores when a JD is provided.** The hero must show both the overall readiness score (role-level) and the JD match score (role-specific), clearly labelled. Without a JD, the hero shows the overall score only, and a muted "No JD provided" callout invites the user to add one. Never display a JD match score for a JD that does not exist.
- **Web-first layout, print-ready fallback.** The dashboard is used primarily in the browser. Use a sticky left-rail navigation, a wide content area (up to 1760px), multi-column grids (score cards 3 wide, action tiers 3 wide, verdict legend 4 wide, peer cards 2 wide), and generous whitespace. Keep the old single-column A4 layout available for `@media print` so PDF export still works.
- **Equal-height columns across every grid.** All grid layouts (`action-plan`, `strategy`, `peer-comparator`, `scores`, `skills`, `recruiter-sim`, `role-fit`, `verdict-legend`, `hero-checklist`) must use `align-items: stretch` so cards in the same row have identical height. Cards inside must be `display: flex; flex-direction: column; height: 100%` so their accent content (lesson, takeaway, meta, delta, note) pins to the bottom via `margin-top: auto`. Ragged-bottom columns are a bug, not an accepted constraint.
- **Consistent card padding, no double-card nesting.** Every "card" container on web uses the same inner padding (16-18px horizontal, 14-18px vertical). Inside `<details>` panels, the `dash-details-body` provides the outer padding; inner cards (sim panels, peer cards, skills columns) sit on top with their own padding and a flat background. Do not nest heavy-border cards inside heavy-border containers - pick one layer of visible framing per region. Tier panels (action plan) are soft-fill to distinguish them from the flat-white action items inside.
- **Progressive disclosure.** Always-visible sections are the verdict, the score breakdown (with formula), role fit, action plan, and strategy. Deeper audits (recruiter sim, JD match, bullets, skills, peers, timeline, market, interview prep, LinkedIn) go inside `<details>` elements that default closed except for the peer benchmark (the most visually rich) and the change report (the payoff of the evidence flow), which are always open.
- **The two side rails are always present.** Side A ("Evidence used") and Side B ("Hiring manager: add & how to get it") render on every dashboard. Side A itemises every source that actually fed the CV, with provenance; Side B turns the Step 14b verdict into gap cards that each end with a concrete `how_to_get_evidence` action (speak to your manager, GitHub, Firebase, analytics, App Store Connect, postmortems, OKRs). Each rail carries as many `<details>` subsections as the data needs; omit a subsection entirely rather than render it empty. Gaps that a candidate is expected to show "in this day and age" are tagged `market_gap` and sorted to the top of Side B.
- **Tone is direct and honest.** No hedging, no corporate softening. If the candidate is not ready, say so clearly and tell them what to do about it.
- **The action plan is the payoff.** If the candidate only reads one section, it should be section 11. Render it with visual weight (larger headings, more whitespace, distinct block backgrounds).
- **Graceful degradation.** If a pipeline step did not run, show the section with a "Not run" note and a one-line suggestion on how to unlock it (e.g. "Provide a job description to see match analysis").
- **Print first for PDF, web first for reading.** Test the web layout on a 1440px viewport and a 1024px laptop; test the print layout mentally against A4 page breaks. Sections 6, 7, 8, 11, and 12 often need their own page in print. Use the `.page-break-before` utility class to force breaks where needed.
- **Save the file immediately** after generating it. Include the path in `files_written` in the final report, along with a one-line note telling the user how to export to PDF (`cmd+P` in the browser, or `chrome --headless --print-to-pdf`).
