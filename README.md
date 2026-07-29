# cv-generator

A self-contained [Claude Code](https://docs.claude.com/en/docs/claude-code) agent that turns raw experience — or an existing CV — into a polished, ATS-optimised, recruiter-tested CV. It runs a full pipeline end to end: extract, benchmark, ATS-optimise, generate impact bullets, simulate a recruiter and a skeptical hiring manager, compare you against real peers in your target role, and render a CV (Markdown + two PDF styles) plus a visual HTML dashboard telling you exactly where you stand and what to fix next.

Everything the agent needs is bundled in this one folder. There are no external service dependencies beyond Claude Code itself.

---

## What it produces

Every run writes, per candidate:

- **The CV** in three formats — a clean Markdown source, an **ATS-safe PDF** (system fonts, plain layout, parses reliably in applicant-tracking systems), and a **designed PDF** (styled terminal-themed layout for sending to humans).
- **A dashboard** (`*-dashboard.html`) — a single self-contained page answering three questions: *Am I ready to apply? What specifically is holding me back? How long until I'm competitive?* It includes score cards, a recruiter simulation, an adversarial hiring-manager verdict, a bullet-by-bullet audit, a skills audit, a peer benchmark against real engineers in your role, an experience timeline, market context, and a tiered action plan.
- **A change report** — what your original CV lacked, which evidence filled each gap, what changed and why, and what's still worth gathering.
- **A hiring-manager verdict** (`*-verdict.json`) — a veteran hiring manager's deliberately hostile read of the finished CV, with the gaps that would get you rejected and the interview questions the CV invites.

---

## Requirements

- **Claude Code** (CLI, desktop, or IDE extension).
- Optional: **Claude in Chrome** for reading login-walled pages (LinkedIn) through your own browser — see [LinkedIn](#linkedin--login-walled-pages) below.
- Optional: **Google Chrome** on your machine for rendering the CV/dashboard HTML to PDF headlessly.

---

## Install

Clone this repo into your user-level Claude Code agents directory:

```bash
git clone <this-repo> ~/.claude/agents/cv-generator
```

Claude Code discovers the agent by the `name: cv-generator` field in `cv-generator.md`; the folder name itself is cosmetic. On next launch the agent is available.

The two entry-point slash commands (`/cv`, `/cv-concerns`) live in `~/.claude/commands/`. If you want them, add `cv.md` and `cv-concerns.md` there. Without them, you can still invoke the agent with a plain prompt (see below).

---

## Using it

### Generate or improve a CV — `/cv`

```
/cv <path-to-your-latest-CV> <any extra material>
```

`/cv` is **intake-first**. Before the agent runs, a short guided questionnaire collects:

- **Anchor** — target seniority, trajectory (same role / promotion / pivot), geography, desired outputs.
- **Assets** — existing CV, LinkedIn content, GitHub/portfolio, a job description to tailor for.
- **Evidence** — a recent performance review, metrics, a brag doc, launch notes.

Then one plain-text step to paste the actual documents. The recommended input is **your latest CV as the source of truth**, plus whatever extra you have. Job-posting and GitHub URLs are optional enrichment; LinkedIn usually needs a paste or the Chrome integration.

Returning users are **not re-interviewed** — the orchestrator loads your saved `intake.json` and only asks *"what changed since last time?"*.

### Fix the hiring manager's concerns — `/cv-concerns`

```
/cv-concerns <your name or CV path>
```

The companion fix-loop. It surfaces each gap from the last run's hiring-manager verdict, walks you through how you want to approach each one (fix with detail you add / rewrite as suggested / leave as-is / not applicable), files any evidence you paste, then applies the agreed changes and re-scores into a new version.

### Plain prompt

Any phrasing like *"improve my CV"*, *"tailor my CV for this posting"*, or *"score my CV"* routes to the agent through its description — no slash command required.

---

## How it works

The agent runs a linear pipeline; each stage is a bundled **skill** (a reference doc under `skills/`, read on demand — not a separately-invokable `/` command). At a high level:

| Stage | What it does | Skill |
|---|---|---|
| Extract | Parse the CV/experience into structured data | *(built in)* |
| Role detection | Infer the target role and seniority band | *(built in)* |
| Trend lookup | Pull current in-demand keywords for the role | `trend-lookup` |
| ATS validation | Check the CV parses cleanly and hits must-have keywords | `ats-validator` |
| Benchmark | Score against a typical competitive candidate | `benchmark` |
| Job-description intel | Read a supplied JD for must-haves / nice-to-haves | `job-description-intel` |
| Peer benchmark | Compare against real engineers in the same role | `peer-benchmark` |
| Impact generation | Turn responsibilities into quantified impact bullets | `impact-generator` |
| Post-mining | Surface achievements worth adding, with your sign-off | `post-miner` |
| Job matching | Score the CV against a specific posting | `job-matcher` |
| Tailoring | Produce a per-JD variant | `cv-tailor` |
| Recruiter simulation | 6-second / 30-second / deep reads | `recruiter-simulator` |
| Hiring-manager verdict | Adversarial final read, built to reject | `hiring-manager-verdict` |
| LinkedIn optimiser | Convert the CV into a consistent LinkedIn profile | `linkedin-optimiser` |
| Output & dashboard | Render CV files and the visual dashboard | `dashboard` |
| Feedback loop | Track changes across runs over time | `feedback-loop` |

Content rules (bullet quality, tense, no fabrication, no em-dashes) are centralised in `skills/cv-principles/SKILL.md`, the canonical rule source the other skills defer to.

The agent runs as a subagent and can't talk to you directly. When extra evidence would genuinely improve the CV, it pauses with a `needs_input` checkpoint that the main session relays and answers. With a complete intake, expect at most one checkpoint: the end-of-run approvals batch (impact ranges, mined claims, anything that looks confidential).

### Evidence store (compaction-proof)

Every document you paste — performance review, metrics, JD, LinkedIn content, the CV itself — is written **verbatim to disk the moment it arrives**, before the agent even launches, under `~/.cv-generator/<user>/`:

- `intake.json` — questionnaire answers, evidence pointers, per-run history, and `declined` / `do_not_ask_again` flags so you're never re-asked.
- `evidence/` — the raw documents, timestamped and immutable. A different CV next month or a new JD per application becomes a **new** entry; nothing is overwritten.
- `evidence/index.json` — the provenance index (type, coverage period, source label, what each item produced). Every claim promoted into the working CV data carries a `source` pointing back to an index entry.

This means context compaction can never lose your metrics or reviews: the agent re-reads everything from disk on resume, and later sessions reuse the same store.

### Versioning

Finished CVs are written as immutable versions under `~/.cv-generator/<user>/versions/vN/` with a stable filename per version. Each version keeps its own CV files, dashboard, change report, and verdict, so you can always diff or roll back.

### LinkedIn / login-walled pages

Plain fetching is blocked by LinkedIn (login wall). To let the agent read LinkedIn through your own logged-in browser, enable **Claude in Chrome** before running `/cv`:

1. One-time: install the Claude extension from the Chrome Web Store (Chrome or Edge).
2. Per session: type `/chrome` in Claude Code (or start with `claude --chrome`).

The browser window stays visible and pauses for you on CAPTCHAs or re-logins. Without Chrome, the agent still works — unreachable URLs come back in a checkpoint asking you to paste the page content.

---

## Repo layout

```
cv-generator/
├── cv-generator.md     ← the agent definition (the ONLY file with agent frontmatter)
├── README.md           ← this file
├── skills/             ← 15 bundled pipeline skills, read on demand
│   ├── ats-validator/SKILL.md
│   ├── benchmark/SKILL.md
│   ├── cv-principles/SKILL.md        (canonical rule source)
│   ├── cv-tailor/SKILL.md
│   ├── dashboard/SKILL.md
│   ├── feedback-loop/SKILL.md
│   ├── hiring-manager-verdict/SKILL.md
│   ├── impact-generator/SKILL.md
│   ├── job-description-intel/SKILL.md
│   ├── job-matcher/SKILL.md
│   ├── linkedin-optimiser/SKILL.md
│   ├── peer-benchmark/SKILL.md
│   ├── post-miner/SKILL.md
│   ├── recruiter-simulator/SKILL.md
│   └── trend-lookup/SKILL.md
├── docs/               ← design docs / architecture notes
└── templates/          ← CV + dashboard HTML templates, shared CSS, and render_cv.py
```

Generated CVs (`~/.cv-generator/`) live outside the repo and are never committed.

## How the bundled skills work

At user scope, Claude Code scans `~/.claude/agents/` recursively and registers **any** `.md` whose YAML frontmatter has a `name:` as an agent. Raw `SKILL.md` files each declare `name:`, so they would otherwise show up as ~15 phantom agents.

To stay self-contained without that pollution, each bundled `SKILL.md` has its YAML frontmatter converted into a leading markdown blockquote (name + description preserved as text); the skill **body is unchanged**. The agent reads these on demand — when a pipeline step says `→ skills/<name>`, it opens `skills/<name>/SKILL.md`. They are reference docs, not separately-invokable `/` skills.

---

## Notes

- **No fabrication.** The agent never invents metrics, employers, or claims. Where a stronger claim isn't truthfully supported by your evidence, it stays qualitative and says so in the change report.
- **Your data stays local.** The evidence store is a per-user working store on your machine so inputs survive compaction and are reusable across runs. It is not a database of other people.
