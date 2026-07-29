> **Bundled skill: `cv-principles`** — reference doc for the cv-generator agent pipeline.
>
> Codified, source-cited rules for what makes a top-notch tech CV in 2025/2026. Reference codex used by ats-validator, content-improvement, recruiter-simulator, benchmark, and cv-tailor. Synthesises Pragmatic Engineer (Gergely Orosz), Google's X-Y-Z formula (Laszlo Bock), Will Larson, Gayle Laakmann McDowell, Levels.fyi top samples, FAANG resume guides, and UK National Careers Service. Every rule carries a citation so downstream skills can justify decisions to the user.

# cv-principles

Reference codex of CV-writing rules. Other pipeline skills consult this skill instead of re-deriving rules ad-hoc. Rules are imperative. Citations are inline.

## How other skills use this codex

- `ats-validator` consults sections 1, 4 (formatting, ATS rules).
- Step 6 Content Improvement consults sections 2 (bullet writing), 3 (section recipe), 5 (tailoring loop).
- `recruiter-simulator` consults section 8 (red flags) and section 1 (universal rules) when deciding bin or shortlist.
- `benchmark` weights bullets against section 2 metric taxonomy.
- `cv-tailor` runs the section 5 three-pass loop.
- iOS-specific roles also consult section 6.
- UK roles also consult section 7.

If a rule below conflicts with a more specific instruction inside another skill's `SKILL.md`, the other skill wins for its own scope. This codex is the default, not an override.

---

## 1. Universal rules

Ranked by importance. Citations link back to the original guidance.

1. **Write for a 6 to 10 second skim, not a read.** Recruiters spend ~6 to 10 seconds on the first pass. If the top third does not earn the next 30, the CV is binned. Source: Orosz, *The Tech Resume Inside Out* (https://thetechresume.com/). McDowell's earlier figure of 15 seconds (https://www.gayle.com/careercup-blog/2008/06/great-resumes-for-software-engineers) is the upper bound; the trend is downward.
2. **Lead every bullet with an outcome, not a responsibility.** "Reduced LCP by 35%, by..." beats "worked on frontend performance." Source: Orosz; Google/Bock X-Y-Z (https://www.amynewman.com/lcc/2020/5/5/resume-advice-from-google).
3. **Use the X-Y-Z formula.** Laszlo Bock, ex-SVP People Operations at Google: *"Accomplished [X] as measured by [Y], by doing [Z]."* Section 2 expands. Source: https://law.utexas.edu/wp-content/uploads/sites/44/2020/09/Google-Recruiters-Say-Using-the-X-Y-Z-Formula-on-Your-Resume-Will-Improve-Your-Odds-of-Getting-Hired-at-Google-_-Inc.com_.pdf
4. **Quantify or cut.** Every bullet should carry a number (latency, %, $, users, headcount, time saved, crash rate). Bullets without a metric are the first to be deleted in tailoring. Source: Orosz; https://www.designgurus.io/blog/best-resume-formats-for-faang-and-top-tech-companies-2025
5. **Reverse-chronological only.** FAANG ATS pipelines and human reviewers expect it. Functional / skills-first formats trigger suspicion. Source: https://www.techinterviewhandbook.org/resume/
6. **One column. No tables. No text boxes. No icons. No headshot.** These break parsing on Greenhouse, Lever, Workday, iCIMS, Taleo. Source: https://www.designgurus.io/blog/best-resume-formats-for-faang-and-top-tech-companies-2025
7. **Use standard section headers.** ATS parsers key on the literal strings `Experience` (or `Work Experience`), `Education`, `Skills`, `Projects`, `Summary`. Same source as rule 6.
8. **Submit a text-based PDF.** Not an image, not a Pages export, not a screenshot. Verify by selecting and copying the text into a plain-text editor. Same source.
9. **Length: 1 page if under 10 years experience, 2 pages for senior or staff, never 3.** "One page for every 10 years of experience" is the FAANG rule of thumb. Senior and staff resumes are expected to run two pages. Sources: https://www.techiecv.com/job-search-toolkit/resume-writing/resume-length and https://owl.purdue.edu/owl/job_search_writing/resumes_and_vitas/using_two_pages_or_more.html
10. **Tailor per role.** Mirror the JD's exact terminology (e.g. "SwiftUI" not "declarative UI") because keyword matching at the ATS layer is literal. Source: rule 6 source.
11. **Cap bullets per role at 3 to 5 for current and recent role, 2 to 3 for older roles.** Senior roles' first bullet must show ownership, not implementation. Source: https://www.techinterviewhandbook.org/resume/
12. **List only languages and frameworks you can be tested on.** McDowell: if you list C++, expect to be asked to write C++. Group by proficiency. Source: https://www.gayle.com/careercup-blog/2008/06/great-resumes-for-software-engineers
13. **Never invent metrics.** If a number is not verifiable, omit the bullet or downgrade to a qualitative claim. Truthfulness is non-negotiable; recruiters cross-check against references and on-site interviews.
14. **Zero typos.** One typo costs ~7 percentage points of interview probability; five costs ~18 pp. 77% of hiring managers reject for grammar or spelling errors. Sources: https://www.cnbc.com/2024/04/08/3-resume-red-flags-recruiters-look-out-for-and-how-to-avoid-them.html , https://resumegenius.com/blog/resume-help/resume-red-flags
15. **Strip buzzwords.** "Innovative", "results-driven", "team player", "synergy", "ninja", "rockstar". Recruiters flag these as fluff in surveys. Sources: https://novoresume.com/career-blog/resume-red-flags , https://www.welcometothejungle.com/en/articles/red-flags-on-a-resume
16. **Drop the objective statement.** A "summary" optionally replaces it; an "objective" telegraphs junior. Consensus across Orosz, McDowell, FAANG guides.
17. **Education goes after experience for anyone with 2+ years of work.** Only new-grads put education on top. Source: https://www.gayle.com/careercup-blog/2008/06/great-resumes-for-software-engineers
18. **Hyperlink GitHub, portfolio, App Store, and any production URL** the candidate cites. A clickable claim is worth more than an unverifiable one.
19. **Use Arial, Calibri, Helvetica, Times New Roman, or Source Sans / Source Serif at 10 to 12pt body.** UK National Careers Service recommends 11pt+. Avoid decorative fonts. Source: https://nationalcareers.service.gov.uk/careers-advice/cv-sections
20. **Margins 0.5 to 1 inch (12 to 25mm), single-spaced, consistent date format.** UK = `DD MMM YYYY`; US = `MMM YYYY`. Source: https://airesume.guru/blog/uk-cv-vs-us-resume

---

## 2. Bullet-writing rules

### The X-Y-Z format (verbatim, Laszlo Bock / Google)

> *"Accomplished [X] as measured by [Y], by doing [Z]."*

Google's worked example (https://www.amynewman.com/lcc/2020/5/5/resume-advice-from-google):

- OK: "Won second place in hackathon."
- Better: "Won second place out of 50 teams in hackathon."
- Best: "Won second place out of 50 teams in hackathon at NJ Tech by working with two colleagues to develop an app that synchronises mobile calendars."

### Outcome verbs

Use these. They imply the result is the candidate's:

> Built, Shipped, Launched, Delivered, Architected, Designed, Engineered, Implemented, Migrated, Refactored, Reduced, Cut, Eliminated, Optimised, Accelerated, Automated, Increased, Grew, Doubled, Scaled, Owned, Led, Drove, Mentored, Hired, Unblocked, Resolved, Decommissioned, Open-sourced, Productionised.

Sources: https://resumeworded.com/software-engineer-resume-action-verbs , https://www.dice.com/career-advice/power-verbs-for-technical-work

### Activity verbs

Avoid. They imply the candidate was nearby when something happened:

> Worked on, Helped, Assisted, Contributed to, Participated in, Involved in, Supported, Aided, Was responsible for, Handled, Took part in, Familiar with.

### Metric taxonomy

In descending order of weight for tech CVs:

1. **Money / business.** Revenue impacted ($), cost saved ($/yr), ARR unblocked, conversion %, retention %, churn %, GMV.
2. **Performance.** Latency (p50, p95, p99 ms), throughput (RPS, QPS), cold-start time, build time, App Store load time.
3. **Reliability.** Crash-free sessions %, uptime %, SLO / SLA attainment, MTTR, incident count.
4. **Scale.** DAU / MAU, requests per day, rows, GB / PB, regions, devices.
5. **Mobile-specific.** App Store rating (e.g. 4.8 stars), downloads (1M+), app-size delta (-25%), launch time, frame drops, ANR rate (Android).
6. **Team / leverage.** Engineers mentored, hires made, on-call rotation owned, headcount unblocked, teams onboarded.
7. **Velocity.** Lead time, deploy frequency, PR throughput, CI duration.

Synthesis from Orosz (https://thetechresume.com/) plus iOS-specific guidance from https://www.resumeviking.com/samples/ios-developer/ and https://medium.com/@reshtei/resume-for-ios-developer-examples-ats-keywords-ff045b07cc83 .

### Bullet anti-patterns (with examples)

- *Responsibility-stated-as-bullet.* "Responsible for backend services." Replace with what shipped and the result.
- *Tech-name-dropping.* "Used React, Redux, GraphQL, Webpack, Babel, Jest." Move to skills section. In bullets, name only tech that earned the result.
- *Team accomplishment claimed solo.* "Increased revenue by 40%." Specify the candidate's contribution: "Led the migration that..."
- *Unfalsifiable adjectives.* "Built a highly scalable, robust microservice." Replace: "Built a service handling 12k RPS at p99 < 80ms."
- *Date-padded internships listed at senior level.* Drop them.

---

## 3. Section-by-section recipe

### Header / contact (top, single line preferred, max 2)

- **In:** full name, role title (one line, e.g. "Senior iOS Engineer"), city + country (city only is acceptable; full street address NOT recommended in UK), phone, professional email, LinkedIn URL, GitHub URL, portfolio or App Store URL.
- **Out:** photo, DOB, marital status, nationality, full street address, gender. Source: UK National Careers Service https://nationalcareers.service.gov.uk/careers-advice/cv-sections
- **Length:** 4 lines maximum.

### Profile / summary (optional; senior+ benefit, junior usually skip)

- 2 to 3 lines, 40 words maximum.
- Formula: `[Role] with [N] years building [domain]. Shipped [headline outcome]. Specialise in [stack].`
- **Out:** objective statements; "passionate about technology"; first-person "I".

### Experience (~60% of page real estate)

- Anchor line per role: `Company, Title  |  Location  |  Mon YYYY to Mon YYYY`. Add a one-line company descriptor only if the company is unknown ("Series-B fintech, 80 engineers").
- 3 to 5 bullets for current and most-recent prior role; 2 to 3 for older roles; 1 line each for jobs older than 8 years, or strip them.
- First bullet of every senior role = scope or ownership ("Led 6-engineer team owning the iOS payments stack").
- Subsequent bullets = X-Y-Z outcomes.
- Reverse chronological. Source: https://www.techinterviewhandbook.org/resume/

### Skills (one block, plain text, comma-separated, no bars or stars or percentages)

- Group by category: Languages, Frameworks, Tools, Cloud, Practices.
- Order within group by genuine proficiency.
- 6 lines total maximum. Cut anything the candidate cannot be tested on. Source: https://www.gayle.com/careercup-blog/2008/06/great-resumes-for-software-engineers

### Projects (mandatory for juniors and new-grads, optional for seniors)

- 3 to 4 projects ideal. Source: https://www.gayle.com/careercup-blog/2008/06/great-resumes-for-software-engineers
- Mark personal vs class vs OSS explicitly.
- Each: name, 1-line what, 1-line outcome or metric, tech, link.

### Education

- New grads: above experience.
- Everyone else: below experience. 1 to 2 lines per degree. Drop GPA after 3 years out unless 3.7+/4.0 from a top school.
- **Out:** secondary school results once a degree exists. Source: UK convention, Prospects and National Careers Service consensus.

### Optional sections (include only if load-bearing)

- *Publications, talks.* Include for staff+ and DevRel; cite venue + year.
- *Open source.* Include if commits are visible and meaningful (link, not "passionate about OSS").
- *Certifications.* Include only if the JD lists them (AWS SA-Pro, CKA). Drop generic Coursera completions.
- *Patents.* Include for senior+ at FAANG.
- *Languages (human).* Include only if relevant to the role's market.

---

## 4. Length, layout, formatting

- **1 page:** 5 years experience or less, new grads, career-changers. Source: https://www.techiecv.com/job-search-toolkit/resume-writing/resume-length
- **2 pages:** senior, staff, principal, 10+ years, leadership scope. Endorsed by Purdue OWL: https://owl.purdue.edu/owl/job_search_writing/resumes_and_vitas/using_two_pages_or_more.html
- **Never 3+ pages** outside academic CVs and publication lists.
- **Single column.** Two-column resumes lose ~20 to 30% of content in older parsers (Taleo, iCIMS) and risk column-order scrambling in Workday. Source: https://www.designgurus.io/blog/best-resume-formats-for-faang-and-top-tech-companies-2025
- **Section headers** in 12 to 14pt bold, ALL CAPS or Title Case. ATS keys on these literal strings.
- **Body** 10 to 11pt, line-height 1.15 to 1.25, margins 12 to 20mm. Density target: 6 to 9 bullets per page max in the experience section. Never wrap a bullet beyond two lines.
- **File:** export as text-selectable PDF. Filename: `Firstname-Lastname-Role.pdf` (no spaces, no `final_v3`).

---

## 5. Tailoring to a job, the 3-pass loop

### Pass 1, keyword extraction

Read the JD twice. Extract:

- Required tech (must-haves).
- Nice-to-haves.
- Role-scope verbs ("lead", "mentor", "architect").
- Domain ("payments", "media", "FinTech").
- Team-size and seniority signals.

Build a 15 to 25 term keyword list.

### Pass 2, bullet rewrite

For each existing bullet, ask: does it surface 1 or more keywords *truthfully*?

- If yes, rewrite to use the JD's exact phrasing (e.g. "asynchronous Swift" becomes "async/await" if that is the JD term).
- If no, demote or cut.
- Add at most 2 new bullets if there is verifiable evidence for a JD must-have not yet on the CV.

### Pass 3, cut for fit

Anything on the CV that does not earn its space relative to the JD goes. A backend bullet on an iOS-focused application is dead weight. Aim for 80%+ of bullets touching JD keywords after this pass.

### Truthfulness rule (non-negotiable)

Never fabricate a metric. Never claim a tech the candidate has not shipped to production or substantial personal-project use. If unsure of a number, downgrade to a verifiable qualitative ("materially reduced", "halved") with an internal source the candidate can defend at interview.

---

## 6. Mobile / iOS specifics

What a senior iOS hiring manager scans for in the first 6 seconds. Synthesised from https://www.resumeviking.com/samples/ios-developer/ , https://cvcompiler.com/ios-developer-resume-examples , https://medium.com/@reshtei/resume-for-ios-developer-examples-ats-keywords-ff045b07cc83 , https://himalayas.app/resumes/ios-developer .

1. **Shipped App Store apps.** Name them, link them, cite downloads + rating (e.g. "Spotify iOS, 100M+ MAU, 4.8 stars").
2. **Years of Swift** stated explicitly ("Swift since 2015"). Objective-C is a plus for legacy roles, neutral elsewhere.
3. **SwiftUI vs UIKit split**, ideally as a percentage ("70% SwiftUI / 30% UIKit, migrating since iOS 16").
4. **Concurrency model.** `async/await`, structured concurrency, actors. Combine and RxSwift acceptable but increasingly seen as legacy.
5. **Architecture.** MVVM, TCA (The Composable Architecture), Clean / VIPER, Coordinator pattern. Senior expects opinion + tradeoff context, not a list.
6. **Modularisation.** Swift Package Manager modules, multi-target apps, build-time numbers ("split monolith into 28 SPM modules; cold build minus 42%").
7. **Crash-free sessions %** (e.g. 99.7%) and **App Store rating** are the two most-cited mobile metrics.
8. **Performance metrics** specific to mobile: cold launch ms, scroll FPS, app size MB, memory peak, battery drain.
9. **Release cadence and process.** fastlane, Xcode Cloud, TestFlight, phased release, App Store Connect API automation.
10. **Testing.** XCTest, XCUITest, snapshot testing (Point-Free, Pixel-Test), test coverage %.
11. **Team / leverage signals.** Number of iOS engineers led, App Review escalations resolved, accessibility audits owned.
12. **Apple ecosystem breadth.** WidgetKit, App Intents, Live Activities, watchOS, visionOS, App Clips. List only if shipped.

What backend CVs emphasise that iOS CVs should de-emphasise: distributed-systems jargon (CAP, consensus), Kubernetes, microservice counts. Substitute with App Store-visible outcomes.

---

## 7. UK conventions (different from US)

Authoritative source: UK National Careers Service, https://nationalcareers.service.gov.uk/careers-advice/cv-sections

- **Term:** "CV", not "resume".
- **No photo.** No exceptions in tech.
- **No date of birth, age, marital status, nationality, gender.** Explicitly disallowed by National Careers Service to prevent age and discrimination bias.
- **Address:** city + postcode optional; full street address not required and increasingly omitted. Source: https://airesume.guru/blog/uk-cv-vs-us-resume
- **Length:** 2 pages is the UK norm even for mid-level. Same source. Contrast with US 1-page bias for early-career.
- **Education placement:** still after experience for non-grads. UK CVs more often retain a one-line "A-Levels / GCSE" entry for early-career; drop once 5+ years post-degree.
- **Date format:** `MMM YYYY to MMM YYYY` or `DD/MM/YYYY` for date of writing. Never US `MM/DD/YYYY`.
- **References:** UK convention tolerates "References available on request" as a one-line footer (https://topcv.co.uk/career-advice/should-i-include-references-available-upon-request-in-my-cv) but it is increasingly considered dead weight and may be omitted. Never list referee contact details on the CV.
- **Right-to-work line:** if the candidate is non-UK and applying to UK roles, a one-line "Right to work in the UK: Yes (Skilled Worker visa, valid to 2027)" or "British citizen" is helpful at the top of the contact block. Visa-status disclosure is NOT recommended on US resumes.
- **Spelling:** British English throughout (`organisation`, `optimise`, `colour`) when applying in the UK; US spelling for US roles. Never mix.

---

## 8. Anti-patterns / red flags

Each item below is something hiring managers actively bin for, with citation:

1. **Typos and grammar errors.** 61% auto-reject for one typo (CareerBuilder, https://resumegenius.com/blog/resume-help/resume-red-flags). Two typos lower interview probability by ~7 pp (https://www.cnbc.com/2024/04/08/3-resume-red-flags-recruiters-look-out-for-and-how-to-avoid-them.html).
2. **Buzzword stuffing without evidence.** "Rockstar", "ninja", "synergy", "innovative", "passionate" without attached metrics. Sources: https://novoresume.com/career-blog/resume-red-flags , https://www.welcometothejungle.com/en/articles/red-flags-on-a-resume
3. **Listing every technology ever touched.** Recruiters read this as covering for a lack of depth. McDowell: "if you list C++, expect to be tested on C++."
4. **Two-column / heavily-designed templates with icons / progress bars.** Break ATS, scrambled in Workday and Taleo.
5. **Photos / DOB / marital status (UK).** Triggers compliance concern in UK and can lead to instant filtering by HR.
6. **Unexplained 12+ month gaps.** Address briefly with a one-line label: "Career break (caregiving)", "Sabbatical (open-source contributions)". Silence reads worse than the truth.
7. **Job-hopping pattern (under 1 year stints repeating).** Group contracts under a single agency or header where possible. Otherwise pre-empt with one line on context.
8. **Generic "Objective" statement.** Outdated. Replace with summary or omit.
9. **Including high school or GCSE details after a degree + 5 years of work.** Reads as filler.
10. **"References available on request" in US resumes.** Wastes a line. In UK it is tolerated but optional.
11. **Personal pronouns.** "I led the team..." Drop the "I". Bullets are headline-style fragments.
12. **Inconsistent tense.** Past roles in past tense; current role in present tense. Never mix within a role.
13. **Dense paragraph blocks.** Anything over 2 lines per bullet is paragraph-shaped and gets skipped in the 6-second pass.
14. **Salary, references' phone numbers, photo of family, hobbies like "watching Netflix".** Instant dismissal signals.
15. **Claims that contradict LinkedIn.** Recruiters cross-check. Mismatched dates or titles read as dishonesty.

---

## Disagreements between sources, resolved

- *McDowell (2008) says ~15s scan; Orosz (2021+) says ~6 to 10s.* Use Orosz as the primary number; the trend is downward as ATS pre-filters more candidates. Both citations available.
- *"References available on request" outdated globally vs still standard in UK.* Drop on US resumes; tolerated as a single line on UK CVs but increasingly seen as dead weight.
- *One-page-only rule.* Strict in US early-career advice; Purdue OWL and UK guides explicitly endorse 2 pages for senior / staff. Resolved: tie length to seniority, not to an absolute rule.

---

## Source registry

- https://thetechresume.com/ , Gergely Orosz, *The Tech Resume Inside Out*
- https://blog.pragmaticengineer.com/the-pragmatic-engineers-resume-template/ , Pragmatic Engineer template
- https://www.amynewman.com/lcc/2020/5/5/resume-advice-from-google , Google X-Y-Z (Laszlo Bock)
- https://law.utexas.edu/wp-content/uploads/sites/44/2020/09/Google-Recruiters-Say-Using-the-X-Y-Z-Formula-on-Your-Resume-Will-Improve-Your-Odds-of-Getting-Hired-at-Google-_-Inc.com_.pdf , Inc / Bock X-Y-Z (PDF)
- https://www.gayle.com/careercup-blog/2008/06/great-resumes-for-software-engineers , Gayle Laakmann McDowell
- https://www.techinterviewhandbook.org/resume/ , FAANG-ready resume handbook
- https://www.designgurus.io/blog/best-resume-formats-for-faang-and-top-tech-companies-2025 , ATS / format rules 2025
- https://nationalcareers.service.gov.uk/careers-advice/cv-sections , UK National Careers Service
- https://airesume.guru/blog/uk-cv-vs-us-resume , UK vs US conventions
- https://topcv.co.uk/career-advice/should-i-include-references-available-upon-request-in-my-cv , UK references rule
- https://resumeworded.com/software-engineer-resume-action-verbs , verb taxonomy
- https://www.dice.com/career-advice/power-verbs-for-technical-work , power verbs
- https://www.techiecv.com/job-search-toolkit/resume-writing/resume-length , length rules
- https://owl.purdue.edu/owl/job_search_writing/resumes_and_vitas/using_two_pages_or_more.html , Purdue OWL on 2-page resumes
- https://www.resumeviking.com/samples/ios-developer/ , https://cvcompiler.com/ios-developer-resume-examples , https://medium.com/@reshtei/resume-for-ios-developer-examples-ats-keywords-ff045b07cc83 , https://himalayas.app/resumes/ios-developer , iOS-specific patterns
- https://www.cnbc.com/2024/04/08/3-resume-red-flags-recruiters-look-out-for-and-how-to-avoid-them.html , red-flag survey
- https://resumegenius.com/blog/resume-help/resume-red-flags , Resume Genius / CareerBuilder typo data
- https://novoresume.com/career-blog/resume-red-flags , buzzwords red flags
- https://www.welcometothejungle.com/en/articles/red-flags-on-a-resume , recruiter confessions
