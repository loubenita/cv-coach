#!/usr/bin/env python3
"""
render_cv.py — deterministic CV renderer (PROOF OF CONCEPT).

Reads the canonical profile data model (base.json, the pipeline's declared
"single source of truth") and emits a canonical CV in Markdown. Layout is a
pure function of data: no LLM, no per-run drift. Wording lives in the data;
structure/order/formatting lives here.

Layer note: base.json holds the RAW extracted experience. In the full design
the pipeline's improved/tailored bullets live in a `cv.json` content layer with
the same shape as the `experience[].bullets` used here — this same renderer
consumes that instead, so the polished CV renders through the identical path.

Usage:
    python3 render_cv.py <base.json> [target.json] > cv.md
Stdlib only.
"""
import json, sys

SKILL_LABELS = {
    "languages": "Languages", "frameworks": "Frameworks",
    "architecture": "Architecture", "apis": "APIs & Data",
    "testing": "Testing", "platform": "Platform",
    "ci_cd": "CI/CD",
    "tooling": "Tooling", "docs": "Docs & Diagramming",
}
# Order skills groups deterministically.
SKILL_ORDER = ["languages", "frameworks", "architecture", "apis",
               "testing", "platform", "ci_cd", "tooling", "docs"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def header_title(base, target):
    # Header presents the target-role framing (per target.json reposition
    # stance); the Experience entries keep their honest held titles.
    if target:
        t = (target.get("target_role") or {}).get("title")
        if t:
            return t
    return base.get("role_detected", "")


def contact_line(base):
    c = base.get("contact", {}) or {}
    parts = [base.get("location", ""), c.get("email", ""),
             c.get("phone", ""), c.get("github", "")]
    return " · ".join(p for p in parts if p)


def render_experience(exp):
    out = []
    for role in exp:
        title = role.get("title", "")
        company = role.get("company", "")
        loc = role.get("location", "")
        dates = role.get("dates", "")
        out.append(f"### {title}, {company}".rstrip(", "))
        meta = " · ".join(p for p in (loc, dates) if p)
        if meta:
            out.append(f"*{meta}*")
        for b in (role.get("bullets") or role.get("bullets_from_resume") or []):
            out.append(f"- {b}")
        out.append("")
    return "\n".join(out).rstrip()


def render_skills(skills):
    lines = []
    for key in SKILL_ORDER:
        vals = skills.get(key)
        if vals:
            lines.append(f"**{SKILL_LABELS.get(key, key.title())}:** " + ", ".join(vals))
    # include any group not in the known order, deterministically sorted
    for key in sorted(k for k in skills if k not in SKILL_ORDER):
        if skills[key]:
            lines.append(f"**{key.title()}:** " + ", ".join(skills[key]))
    return "  \n".join(lines)


def render_projects(projects):
    out = []
    for p in projects:
        name = p.get("name", "")
        desc = p.get("description", "")
        link = ""
        links = p.get("links") or {}
        for k in ("web", "app", "repo", "github"):
            if links.get(k):
                link = f" ([{k}]({links[k]}))"
                break
        out.append(f"### {name}{link}".rstrip())
        if desc:
            out.append(desc)
        out.append("")
    return "\n".join(out).rstrip()


def render_education(education):
    return "\n".join(
        f"- {e.get('qualification','')}" + (f" *({e.get('dates')})*" if e.get("dates") else "")
        for e in education
    )


def render(base, target=None):
    md = []
    md.append(f"# {base.get('name','')}")
    title = header_title(base, target)
    md.append(f"**{title}** · {contact_line(base)}" if title else contact_line(base))
    md.append("")

    if base.get("summary_raw"):
        md.append("## Summary")
        md.append(base["summary_raw"])
        md.append("")

    if base.get("experience"):
        md.append("## Experience")
        md.append(render_experience(base["experience"]))
        md.append("")

    if base.get("projects"):
        md.append("## Projects")
        md.append(render_projects(base["projects"]))
        md.append("")

    if base.get("skills"):
        md.append("## Skills")
        md.append(render_skills(base["skills"]))
        md.append("")

    if base.get("education"):
        md.append("## Education")
        md.append(render_education(base["education"]))
        md.append("")

    return "\n".join(md).rstrip() + "\n"


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    base = load(argv[1])
    target = load(argv[2]) if len(argv) > 2 else None
    sys.stdout.write(render(base, target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
