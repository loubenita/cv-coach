> **Bundled skill: `peer-benchmark`** - reference doc for the cv-generator agent pipeline.
>
> Does a deep read of 5 real LinkedIn profiles in the same role as the candidate, extracts what makes each one strong, runs cross-profile pattern recognition, and maps the gaps back to the candidate's CV. Produces a prioritised "they have, you don't" list for the dashboard with quick-wins and long-term investments separated. Called by the cv-generator agent after trend lookup.

# peer-benchmark

The best way to know what a strong profile looks like is to read five of them, side by side, in the same role. This skill does a thorough read of each comparator, runs pattern analysis across all five, and surfaces the specific gaps between those profiles and the candidate. Depth matters here. A surface-level "they have Kubernetes, you don't" is useless. A well-grounded "4 of 5 comparators lead a rewrite project with a named outcome, and you have one similar story that's currently undersold" is actionable.

## Input

```json
{
  "role": "",
  "seniority": "",
  "industry": "",
  "company": "",
  "company_domain": "",
  "company_profile_tier": "",
  "location": "",
  "candidate_cv": {}
}
```

- `industry` is the sector label (e.g. fintech, e-commerce, healthtech, gaming).
- `company` is the candidate's current employer.
- `company_domain` is the more specific sub-sector for peer matching. Derive this from the candidate's current role + company. Examples:
  - Northwind Fitness → `e-commerce / D2C fitness apparel`
  - Harbour Property → `consumer property tech`
  - Monzo → `fintech / challenger bank`
  - Deliveroo → `marketplace / on-demand logistics`
  - Depop → `marketplace / secondhand commerce`
- `company_profile_tier` captures how recognisable the employer is to a non-specialist recruiter. Use this scale:
  - `tier_1_global_brand` - universally recognised (Apple, Google, Meta, Amazon, Microsoft, Netflix, Spotify)
  - `tier_2_prestige_local` - high-profile in-market (Monzo, Revolut, Starling, Deliveroo, Bumble, Trainline, ASOS, Northwind Fitness in the UK)
  - `tier_3_strong_mid_market` - credible scale-ups and established companies (Depop, Huel, Castore, Perkbox, Onto, Trustpilot)
  - `tier_4_niche_or_unknown` - domain specialists or regionally obscure (agencies, B2B SaaS with narrow reach, boutique studios)
- `location` scopes the search to the candidate's market (e.g. UK, Germany, remote-EU). If omitted, search globally and note the skew in the summary.

## Tooling note

LinkedIn blocks unauthenticated `WebFetch` requests (HTTP 999). For a proper deep read, use, in order of preference:

1. **Chrome MCP with an authenticated session** (`mcp__Claude_in_Chrome__*` tools). Navigate to each profile, scroll to load lazy content, then call `get_page_text`. This is the only way to read full experience bullets, recommendations, and the activity feed.
2. **Public Google cache or third-party profile aggregators** (e.g. indexed search results showing "About" + experience snippets). Shallower but works without auth.
3. **Web search snippets alone** as a last resort. Flag `signal_strength: "low"` and `depth: "shallow"` in the output and tell the user the read was surface only.

If the agent lacks Chrome MCP access, ask the user to either grant it or provide the 5 profile URLs along with any pre-captured content.

## Process

### Step 1: Candidate selection (cast wide, filter tight)

The goal is a peer set that is **credibly comparable** but also **upwardly ambitious**. Bias the search toward the candidate's domain first, then layer in high-profile comparators that a hiring manager would recognise instantly.

#### Two non-negotiable biases

1. **Domain-first.** Prioritise comparators who work (or recently worked) in the candidate's `company_domain`. Sam at Northwind Fitness is compared against e-commerce / D2C / retail iOS engineers first, not against fintech by default.
2. **High-profile override.** A comparator from a `tier_1_global_brand` or `tier_2_prestige_local` employer can be included **even if the domain does not match**, because their company name is itself a recognisable signal. A Senior iOS at Monzo is a valid comparator for a Northwind Fitness engineer because Monzo's brand weight makes it a useful benchmark, even though fintech ≠ e-commerce. The same applies for Apple, Google, Meta, Amazon, Netflix, Spotify, Stripe, Figma, and similar.

When the candidate is already at a tier_1 or tier_2 employer, do **not** pad the peer set with tier_3 or tier_4 comparators from matching domains. Keep the bar at or above the candidate's current tier.

#### Search query shapes

Search with multiple query shapes to avoid single-query bias. Run at least three of these per peer slot:

- `"{Role}" site:linkedin.com/in {location}` (e.g. `"Senior iOS Engineer" site:linkedin.com/in UK`)
- `"{Role}" "{key skill}" linkedin` (seniority is often missing from titles; anchor on a core skill)
- `"{Role}" "{candidate_company_domain}" linkedin` (domain-first query, e.g. `"Senior iOS Engineer" "e-commerce" linkedin`)
- `"{Role}" "{tier_1 or tier_2 company name}" linkedin` (e.g. `"Senior iOS Engineer" "Monzo" linkedin`)
- `"{Role}" speaker OR author OR "open source" linkedin` (bias toward visible profiles)
- `site:linkedin.com/in "{Competitor brand to candidate's employer}" "{Role}"` (direct-competitor sweep, e.g. at Northwind Fitness try ASOS, Nike, Lululemon, Castore, Huel)

Collect 15-25 candidate profiles. Record each one's employer, employer tier, and domain so the filter step can apply the rules below honestly.

#### Filter to 5 using this mix

- **2 domain peers** - same role, same seniority, same (or directly competing) domain. These are the fairest direct comparators. At Northwind Fitness: iOS engineers at ASOS, Nike, Lululemon, Castore, Huel, Depop, Vinted, HelloFresh. Required: **both must be at a recognisable employer (tier_1, tier_2, or a respected tier_3 scale-up)**.
- **2 prestige peers** - same role, same seniority, at a tier_1 or tier_2 brand, **domain mismatch is acceptable and often preferred**. This is where Monzo, Apple, Google, Meta, Stripe, etc. enter the set. They show what "Senior iOS at a recognisable brand" looks like outside the candidate's industry.
- **1 one-rung-above peer** - Staff / Principal / Lead iOS at either a domain peer or a prestige peer. Shows the next step on the ladder. Do **not** use this slot for a lateral comparator.

If fewer than 5 profiles can be found, return what exists, note the count, and explicitly tell the user the pattern analysis is weaker.

#### Tier-floor rule

Do not include a comparator whose employer is **more than one tier below** the candidate's own employer. Examples:

- Candidate at Northwind Fitness (tier_2) → all 5 comparators must be tier_1, tier_2, or tier_3. A tier_4 agency iOS engineer would drag the peer signal down rather than up.
- Candidate at Apple (tier_1) → all 5 comparators should be tier_1 or tier_2. A tier_3 comparator is acceptable only if they bring a unique signal the tier_1/2 set lacks (e.g. they are the Staff+ comparator).
- Candidate at a tier_3 scale-up → the peer set should span tier_2 and tier_3, with at least one tier_1/2 prestige peer to pull the bar up.

Rule of thumb: **comparators should either share the candidate's domain or exceed them on employer brand.** Both is best. Neither is a failed peer slot - replace it.

### Step 2: Deep read (every section of every profile)

For each of the 5 selected profiles, pull these sections (in priority order). Do not skip sections that exist.

| Section | What to extract | Why it matters |
|---------|-----------------|----------------|
| Headline | How they brand themselves in one line | Tells you the positioning norm for the role |
| About | Narrative, tone, themes, specialisms claimed | Reveals what they lead with |
| Experience (every role) | Title, company, dates, every bullet verbatim | This is the deep signal: scope, tech, outcomes |
| Licenses & Certifications | Name, issuer, year | Separates candidates who invested in formal credentials |
| Education | Degrees, institutions, extracurriculars | Baseline and sometimes a differentiator |
| Skills & Endorsements | Top 10 skills with endorsement counts | Endorsed ≥20 times = real depth claim |
| Recommendations | Full text of recommendations received | Third-party validation; reveals working style |
| Featured | Links, media, articles they pin | What they are proudest of |
| Projects | Side work, personal projects | Shows initiative beyond employed work |
| Publications | Articles, papers, books | Thought leadership signal |
| Honors & Awards | Any named recognition | Peer / industry validation |
| Patents | Any filed patents | IP contribution signal |
| Volunteer | Boards, mentoring, community work | Extracurricular engagement |
| Languages | Spoken languages | Market access, sometimes relevant |
| Activity (posts) | Last 20 posts | Talks attended, deals closed, launches (overlaps with `post-miner` logic) |

For each profile, produce a `profile_digest` object containing every section that exists. A profile missing a section is itself a signal (e.g. 0 recommendations is a weak profile).

### Step 3: Per-profile differentiator extraction

Against each deep read, tag what makes this profile competitive. Split into:

- **Surface skills**: skills they list that the candidate does not
- **Demonstrated skills**: skills referenced in their experience bullets that the candidate's bullets don't reference (stronger signal than a skill tag)
- **Implicit skills**: skills implied by the company, product, or project type (e.g. "worked at a payments fintech" implies PCI / card-scheme knowledge)
- **Achievements**: certifications, conference talks, OSS projects, awards, publications
- **Process signals**: do they use metrics in bullets? Do they name products? Do they claim ownership?
- **Visibility signals**: do they post? Speak? Publish? Have recommendations from senior people?
- **Career trajectory**: linear progression, lateral moves, industry switches

### Step 4: Cross-profile pattern recognition

This is the step the first version of this skill missed. Aggregate across all 5 profiles:

- **Universal signals** (5 of 5): almost certainly table-stakes for the role
- **Majority signals** (3-4 of 5): strong signal that the candidate is expected to have or build this
- **Divergent signals** (1-2 of 5): one comparator's differentiator, not a pattern. Low priority.
- **Absent signals** (0 of 5): things the candidate has that nobody else lists. Candidate strength.

For each signal, record how many profiles show it and weight accordingly.

### Step 5: Map back to candidate

For each aggregated signal, compare against the candidate's CV (full bullets, not just skills list). Classify each gap:

- **Rename opportunity**: candidate has this but labels it differently or buries it in prose. Quick win.
- **Surface-but-not-demonstrated**: candidate lists the skill but no bullet demonstrates it. Medium effort, rewrite a bullet.
- **Genuine gap, addable**: candidate has adjacent experience that could honestly support a new bullet. Medium effort.
- **Genuine gap, not addable now**: candidate lacks this experience entirely. Long-term investment, flagged for awareness only.

For each gap, attach a `suggestion` with a concrete next action.

### Step 6: Candidate strengths

Note anything the candidate has that 0-1 of the comparators have. These are competitive advantages to emphasise on the CV, not gaps to fix.

### Step 7: Summary

Write a 2-3 sentence plain-English read on where the candidate sits relative to the peer set. Tone: direct, no hedging, no fluff.

## Output

```json
{
  "search": {
    "queries_used": [],
    "candidates_considered": 0,
    "profiles_selected": 0,
    "depth": "deep | medium | shallow",
    "notes": ""
  },
  "comparators": [
    {
      "profile_url": "",
      "alias": "",
      "display_name": "",
      "selection_reason": "domain_peer | prestige_peer | one_above",
      "current_role": "",
      "current_company": "",
      "current_company_type": "",
      "current_company_domain": "",
      "current_company_profile_tier": "tier_1_global_brand | tier_2_prestige_local | tier_3_strong_mid_market | tier_4_niche_or_unknown",
      "domain_match_vs_candidate": "same | competitor | adjacent | mismatch",
      "brand_match_vs_candidate": "above | equal | below",
      "why_included": "",
      "signal_strength": "high | medium | low",
      "profile_digest": {
        "headline": "",
        "about_summary": "",
        "experience": [
          { "title": "", "company": "", "dates": "", "notable_bullets": [] }
        ],
        "certifications": [],
        "skills_top": [],
        "recommendations_count": 0,
        "featured_count": 0,
        "publications": [],
        "honors": [],
        "activity_signals": []
      },
      "differentiators": {
        "surface_skills": [],
        "demonstrated_skills": [],
        "implicit_skills": [],
        "achievements": [],
        "process_signals": [],
        "visibility_signals": [],
        "trajectory": ""
      }
    }
  ],
  "cross_profile_patterns": {
    "universal": [],
    "majority": [],
    "divergent": [],
    "absent_from_all": []
  },
  "candidate_gaps": [
    {
      "gap": "",
      "seen_in_n_profiles": 0,
      "gap_type": "rename | surface_not_demonstrated | addable | long_term",
      "priority": "high | medium | low",
      "effort": "quick_win | medium | long_term",
      "suggestion": "",
      "addable_now": true,
      "evidence_from_comparators": [],
      "notes": ""
    }
  ],
  "candidate_strengths": [
    { "strength": "", "unique_to_candidate": true, "how_to_emphasise": "" }
  ],
  "summary": ""
}
```

### Priority logic

Priority is a function of frequency in the peer set AND relevance to the target role:

- **high**: gap appears in 3+ of 5 profiles AND is directly relevant to the target role, OR is a rename opportunity (quick win with no new experience required)
- **medium**: appears in 2 profiles, or in 3+ but indirectly relevant, or requires rewriting an existing bullet
- **low**: appears in 1 profile, or is a long-term investment the candidate cannot act on now

### Edge cases

- **0 profiles found**: return an empty `comparators` array, set `depth: "shallow"`, and put a clear note in `summary` telling the user the benchmark could not run. Do not fabricate.
- **Locked / private profiles**: if a profile is found in search but cannot be read (login wall, deleted account), exclude it and pick the next candidate.
- **Candidate is the top comparator**: if the candidate's own profile is one of the top results, skip it and continue.
- **All comparators look the same**: if cross-profile patterns produce fewer than 3 signals total, the peer set is too narrow. Note this and suggest the user broaden the industry or location filter.
- **Only tier_4 matches available for the domain**: if the domain is niche enough that no tier_1/2/3 domain peer exists, fill those slots with prestige peers from mismatching domains and note in `summary` that direct-domain comparators were not available at a comparable brand tier.
- **Candidate is tier_1 already**: comparators should all be tier_1 or tier_2. Never drop below tier_2 in this case. If fewer than 5 tier_1/2 profiles surface, return what exists rather than padding with weaker comparators.

## Rules

- **No fabrication. Every claim must be verifiable.** Every comparator must be a real, publicly visible profile. Every differentiator must be traceable to a specific, named artefact - a blog URL, a GitHub repo, a talk on SpeakerDeck or YouTube, an engineering-blog byline with a date, an App Store link. If the claim cannot be traced to a live URL or a dated public source, do not include it. Inferred or "likely has X" signals belong in the agent's internal notes, not in the output.
- **Cross-verify every web-sourced claim.** A LinkedIn title alone is not enough. Before asserting a comparator has a blog, OSS package, or conference talk, the agent must have visited (via `WebFetch` or Chrome MCP) a second source that corroborates it: the actual blog URL resolves, the repo page loads with commit activity, the talk has a video or slide deck link. If the second source fails, drop the claim or drop the comparator.
- **Rich-footprint minimum bar.** Each comparator must have at least two verifiable public artefacts from this list: personal blog with iOS content, named OSS package, conference talk with video/slides, engineering-blog byline under their name, book/course/newsletter they run, shipped App Store app. A LinkedIn profile with no secondary public footprint fails the bar - replace the comparator rather than padding the matrix with "Not public" cells.
- **Matrix integrity.** The side-by-side matrix must only contain rows where every comparator has a verifiable yes/no/partial answer. If a signal cannot be verified for one or more comparators, drop the row entirely. A matrix with "Not public" cells for half the rows is worse than a shorter matrix with honest, verifiable rows.
- **Named peers in the dashboard.** The dashboard shows each comparator's real first name + last initial (or full name if already widely public, e.g. Donny Wals, Antoine van der Lee), company, and a link to the profile. This is explicitly requested by the user. Full profile URLs are included. Do not expose contact info, phone numbers, email addresses, or anything not publicly visible.
- **Privacy first.** Pull only publicly visible profile data. No contact info, phone numbers, private posts, or anything behind a connection-only filter. Publicly visible headline, title, employer, recommendations count, Featured items, and public posts are fair game.
- **Domain-first, brand-up.** The peer set is ordered by domain match first, then brand tier. Never fill a peer slot with someone who is both a domain mismatch and a tier_3 or tier_4 employer - that profile brings no useful signal.
- **Never compare down on brand.** Do not include a comparator whose employer is more than one tier below the candidate's. See the tier-floor rule in Step 1.
- **Demonstrated beats surface.** A skill referenced in experience bullets counts more than a skill listed in the skills section. Reflect this weighting in the gap priority.
- **Rename opportunities are the highest-leverage fixes.** If the candidate has the skill but labels it differently, that's a 5-minute CV fix that closes a real gap. Flag it as a quick win.
- **Flag long-term gaps separately.** Do not put "learn Kubernetes" in the same bucket as "rename 'mentoring' to 'technical leadership'". The dashboard distinguishes them.
- **Weight by frequency honestly.** A skill in 1 of 5 profiles is a weak pattern, not a gap. Do not over-weight one outlier.
- **The summary must be useful.** Avoid hedging language ("it seems", "might be"). Say what the peer set tells us directly.
