# CV Generator: Locked Dashboard Template, JSON-First Rendering, Output Naming

## Context

The dashboard HTML was re-authored from scratch by the agent on every run. Output drifted in structure and size run-to-run (37 KB → 51 KB → 49 KB across three Sam runs), and the layout oscillated between two incompatible designs: the `SKILL.md` prose described a **3-column** layout (an "Evidence used" left rail + a "Hiring manager" right rail), while the outputs the user actually liked (the v2 dashboard) were a clean **2-column** layout (a section-nav rail + content). The 2026-07-16 run followed the 3-column skeleton; the v2 run didn't. That oscillation is the "the agent generates whatever it wants" problem.

This change locks the structure, introduces the rendering discipline that prevents drift at the root, and defines how per-run outputs are named and grouped.

User decisions captured this session:
1. **Base template = the v2 dashboard** (`versions/2026-07-15-0005-sam-rivera-dashboard-v2.html`), 2-column, cleaner than the 3-column variant. The two side rails are **dropped**, not preserved.
2. **Side nav restructured** into collapsible groups. Final grouping (user-specified): findings / the agent's scores & decisions / the hiring manager - realised as **four** groups (see below), user having said "more groups if required".
3. **Content order is NOT reordered** to match the nav groups this pass - the nav groups categorise; they don't move sections. (Revisit once sections render from JSON, where reordering is free.)
4. **JSON-first rendering** is the direction. `base.json` is already the declared source of truth; the gap is the *rendering* discipline.
5. **Output naming/grouping by identity** - generic runs version up (`-v1`, `-v2`); JD runs key on the company (`-apple`, then `-apple-v2`).
6. Dashboard nav carries a **Download CV** block linking the three CV formats.

All edits target the authoritative bundle (`~/.claude/agents/cv-generator/`). Persisted per-user data lives under `~/.cv-generator/<user>/`.

---

## Core principle: separate *what to say* from *how it looks*

- **What to say** = judgment → the LLM's job (bullet wording, scores, framing, tailoring). Output is **data**.
- **How it looks** = mechanical → a renderer's job (layout, order, CSS, pagination). Output is **pixels**.

The drift came from letting the LLM decide layout. The fix is to take layout away from it: the LLM emits validated data; a deterministic step turns data into the artifact. Same input → same structure, every run.

### Layered data model

```
base.json      ← raw extracted profile + provenance   (sacred; already exists, "Base is sacred")
target.json    ← the anchor (role, seniority, trajectory, geography)   (exists)
      │  pipeline (LLM: extract → improve → score → tailor)
      ▼
cv.json        ← final CV content (polished/tailored bullets, section order)  ──►  render_cv.py     ──► <identity>.md / .pdf
dashboard.json ← final analysis content (scores, findings, verdict, plan)     ──►  locked template  ──► <identity>-dashboard.html
```

Both `cv.json` and `dashboard.json` derive from `base.json` → one source of truth, DRY, and the change-report becomes a diff between JSON snapshots.

**Layer note (important):** `base.json` holds *raw* extracted bullets. The *polished* bullets the pipeline produces (impact-generator, tailoring, ATS) are a downstream content layer (`cv.json`) with the same shape. `render_cv.py` reads whichever it is given, so the raw and polished CVs render through the identical path.

### Deliberate CV/dashboard split

The two artifacts are **not** treated identically - matched to each artifact's nature:

| Artifact | Approach | Why |
| --- | --- | --- |
| **CV** | **Deterministic script renderer** (`templates/render_cv.py`) | Stable, bounded structure; it is the actual product sent to employers; worth pixel-determinism. |
| **Dashboard** | **Locked HTML template + `dashboard.json` data contract** (agent fills the template) | 14 prose-heavy, conditional sections; a full script renderer is more maintenance than it's worth. The template already locks the layout. |

So the CV goes fully deterministic; the dashboard keeps the locked template but is fed structured data instead of being free-formed.

---

## Locked dashboard template - `templates/dashboard.html`

Built from the v2 dashboard. The inline `<style>` block, the section set/order/ids, and the nav are fixed; the agent fills content and tokens.

### Side nav - four collapsible groups (`<details class="navgroup">`, no JS)

| Group | Sections (ids) |
| --- | --- |
| **Overview & scores** | Executive summary (`#verdict`) · Score breakdown (`#scores`) · Recruiter simulation (`#recruiter`) |
| **Findings** | Role fit (`#rolefit`) · JD match (`#jdmatch`) · Bullet audit (`#bullets`) · Skills audit (`#skills`) · Peer benchmark (`#peers`) · Timeline & market (`#timeline`) · LinkedIn check (`#linkedin`) |
| **Hiring manager** | Hiring-manager verdict (`#hmverdict`) · Interview prep (`#interview`) |
| **Action plan** | Action plan (`#actionplan`) · Application strategy (`#strategy`) |

Nav groups categorise the sections; content order in `<main>` is the v2 order (kept, incl. its numbering that skips a standalone "10").

### Download CV block (top of the nav)

Three tokenized links to the identity's CV files (relative paths, same folder):

| Label | Token | Style |
| --- | --- | --- |
| Designed PDF | `{{CV_PDF_FANCY}}` | green accent (the "fancy" one) |
| ATS PDF (basic) | `{{CV_PDF_ATS}}` | plain - for applying via portals |
| Markdown source | `{{CV_MD}}` | plain |

### Tokens the agent fills per run
`{{CANDIDATE_NAME}}`, `{{GENERATED_DATE}}`, `{{CV_PDF_FANCY}}`, `{{CV_PDF_ATS}}`, `{{CV_MD}}`.

### Superseded rails
The two side rails in the old `SKILL.md` prose ("Evidence used", "Hiring manager: add & how to get it") are **superseded** by this single-nav-rail layout. Their content is still valuable and now belongs in the main column (Executive summary, Hiring-manager, Action-plan sections). `SKILL.md` carries a precedence rule: **where the prose conflicts with `templates/dashboard.html`, the template wins.**

---

## Output naming & grouping convention

Group every run's outputs into one folder per **identity** under `versions/`.

- **Identity** = `<candidate-slug>-<line>`, where `<line>` is:
  - **generic** (no JD): a version - `v1`, `v2`, `v3`, … (N = prior generic runs + 1). → `sam-rivera-v3`
  - **JD-targeted**: the company/JD slug - first run `<company>`, repeats add `-v2`, `-v3`. → `sam-rivera-apple`, then `sam-rivera-apple-v2`
- Folder `versions/<identity>/` contains, all named with the identity (self-describing when shared individually):

```
versions/sam-rivera-v3/
├── sam-rivera-v3.md                  ← canonical CV (markdown)
├── sam-rivera-v3.pdf                 ← designed / "fancy" PDF (via templates/Terminal Resume.html)
├── sam-rivera-v3-ats.pdf             ← ATS / basic PDF for applying
├── sam-rivera-v3-dashboard.html      ← dashboard; Download CV nav links to the 3 files above (relative)
└── sam-rivera-v3-change-report.md    ← change report
```

- Never overwrite a prior identity's folder; a new generic run or a repeat JD run takes the next `-vN`.
- Folder-per-identity keeps the dashboard's relative download links portable.
- Put the absolute path of every file written into `files_written`.

---

## Status

**Built this session**
- `templates/dashboard.html` - locked template: 4-group collapsible nav + Download CV block + tokens.
- `templates/render_cv.py` - deterministic CV → Markdown renderer (stdlib only). Proven end-to-end on Sam's `base.json`, reposition framing preserved (header "Senior iOS Engineer", Northwind Fitness entry honest "iOS Engineer").
- `skills/dashboard/SKILL.md` - "Canonical template - start here" section, precedence rule, 3-column skeleton replaced with the 2-column grouped-nav skeleton, Download block + save path documented.
- `cv-generator.md` - output naming/grouping convention; change-report and dashboard paths point at `versions/<identity>/`.
- `versions/sam-rivera-v3/` - first grouped identity folder, assembled from the 2026-07-16 real outputs. Dashboard opened for review. (Its body is the last full analysis; its download links point at the real v3 files. Next full run renders a fresh body through the template.)

**Pending (recommended next, in order)**
1. **Wire `render_cv.py` into the pipeline** - Step 14 emits `cv.json`; the script renders `<identity>.md` (+ HTML/PDF via `Terminal Resume.html`). Validates the `cv.json` contract before touching the dashboard. *(Highest value, lowest risk.)*
2. **Define `dashboard.json`** and have Step 16 fill `templates/dashboard.html` from it (rather than free-forming content).
3. Optionally reorder the dashboard `<main>` sections to match the four nav groups (renumbering) once sections render from `dashboard.json`.

## Open questions
- Do we want a `cv.json` schema versioned like `intake.json`/`base.json` (`schema_version`), and validated before render?
- CV HTML/PDF: reuse `Terminal Resume.html` as the render target for `render_cv.py`, or keep the current PDF path? (Recommend reuse - one CV template, one renderer.)
- Should the "Evidence used" provenance become a compact main-column dashboard section, or stay solely in the change-report?
