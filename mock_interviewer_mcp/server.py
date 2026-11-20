"""Mock Interviewer MCP server.

Exposes the interview-prep method to any MCP-capable AI client (Claude, ChatGPT
desktop, Codex, Gemini CLI, Cursor, VS Code, Goose, ...). The method itself is the
same SKILL.md and reference files as the skill; this server just serves them as
tools, because tools are the one MCP feature every client supports. It also adds
three deterministic helpers that a model should not do by eye: checking that a
question bank will load in the interviewer, reading the numbers out of a debrief,
and creating the working folder from the blank templates.

Nothing here calls a model, a network, or a paid API.
"""
from __future__ import annotations

import pathlib
import re
import sys

try:  # MCP Python SDK 2.x
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # MCP Python SDK 1.x
    from mcp.server.fastmcp import FastMCP as _Server


# --------------------------------------------------------------------------- files
def _skills_root() -> pathlib.Path:
    here = pathlib.Path(__file__).resolve().parent
    for cand in (here / "skills", here.parent / "skills"):
        if (cand / "interview-prep" / "SKILL.md").exists():
            return cand
    raise FileNotFoundError("Cannot find the skills/ folder next to the server.")


SKILLS = _skills_root()
LANGS = {"en": "interview-prep", "zh": "interview-prep-zh"}
STEPS = {
    "overview": "SKILL.md",
    "employer": "references/01-employer-research.md",
    "self": "references/02-story-bank.md",
    "mock": "references/03-mock-and-debrief.md",
}
TEMPLATES = ["company-dossier", "why-them", "question-bank", "gap-list",
             "story-card", "selling-points", "self-intro", "weaknesses"]
FOLDERS = {
    "01_why_them": ["company-dossier", "why-them"],
    "02_why_me": ["selling-points", "self-intro", "weaknesses"],
    "03_questions": ["question-bank", "gap-list"],
    "04_mocks": [],
}


def _lang(language: str) -> str:
    l = (language or "en").strip().lower()
    return "zh" if l.startswith("zh") or l in ("中文", "chinese", "cn") else "en"


def _read(lang: str, rel: str) -> str:
    return (SKILLS / LANGS[lang] / rel).read_text(encoding="utf-8")


def _strip_frontmatter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S).lstrip()


# ------------------------------------------------- question bank (mirrors the tool)
# Same rules as parseBank() in interviewer/index.html, so a bank that passes here
# loads there.
FIELDMAP = {
    "type": "type", "budget": "budget", "reading": "reading", "mode": "type",
    "类型": "type", "题型": "type", "预算": "budget", "时间": "budget", "时长": "budget", "阅读": "reading", "阅读时间": "reading",
    "best story": "best", "beststory": "best", "最优素材": "best", "素材": "best",
    "backup": "backup", "次优": "backup", "opener": "opener", "开场句": "opener", "开头一句": "opener",
    "watch": "watch", "注意": "watch", "framework": "watch", "框架": "watch",
    "fact": "fact", "factpattern": "fact", "fact pattern": "fact", "题面": "fact",
    "key": "key", "answer key": "key", "answerkey": "key", "参考答案": "key",
    "source": "source", "来源": "source",
}
_H = re.compile(r"^###\s*(.*?)\s*$")
_F = re.compile(r"^\s*[-*]\s*([^:：]{1,24})[:：]\s*(.*)$")
_CONT = re.compile(r"^\s{2,}\S")


def _parse_budget(v: str | None) -> int | None:
    if not v:
        return None
    s = str(v).strip().lower()
    m = re.match(r"^(\d+(?:\.\d+)?)\s*m", s)
    if m:
        return round(float(m.group(1)) * 60)
    m = re.match(r"^(\d+)\s*s?$", s)
    return int(m.group(1)) if m else None


def _mmss(s: int) -> str:
    sign = "-" if s < 0 else ""
    s = abs(int(s))
    return f"{sign}{s // 60}:{s % 60:02d}"


def parse_bank(md: str) -> tuple[list[dict], list[str]]:
    out, unknown = [], []
    cur, last = None, None
    for raw in (md or "").splitlines():
        h = _H.match(raw)
        if h:
            if cur:
                out.append(cur)
            cur = {"text": h.group(1), "fields": {}, "raw": {}} if h.group(1) else None
            last = None
            continue
        if not cur:
            continue
        f = _F.match(raw)
        if f:
            label = f.group(1).strip()
            key = FIELDMAP.get(label.lower())
            last = key
            if key:
                cur["fields"][key] = (f.group(2) or "").strip()
                cur["raw"][key] = label
            else:
                unknown.append(f'"{label}" under "{cur["text"][:60]}"')
            continue
        if last and _CONT.match(raw):
            cur["fields"][last] = ((cur["fields"].get(last, "") + "\n" + raw.strip()).strip())
    if cur:
        out.append(cur)
    return out, unknown


# ------------------------------------------------------------------------- server
INSTRUCTIONS = """Interview preparation in three steps: research the employer, research the candidate, then timed mock interviews whose debriefs are folded back into the material.

Whenever the user mentions an upcoming interview, pastes a job posting, asks for STAR stories, wants to practise, or brings back a mock-interview debrief, call interview_prep_guide with step="overview" first and follow it. Fetch the step files as the overview tells you to. Never invent the user's experience: ask, structure and sharpen."""

VERSION = "1.1.0"
try:
    mcp = _Server("mock-interviewer", instructions=INSTRUCTIONS, version=VERSION)
except TypeError:  # SDK 1.x has no version argument
    mcp = _Server("mock-interviewer", instructions=INSTRUCTIONS)


@mcp.tool()
def interview_prep_guide(step: str = "overview", language: str = "en") -> str:
    """Return the interview-prep method to follow.

    Call this first, with step="overview", whenever the user mentions an interview,
    a job posting, STAR stories, practising, or a mock-interview debrief. The
    overview says when to fetch each step file.

    step: "overview" (the whole method), "employer" (step 1: JD teardown, dossier,
          why-them, question bank), "self" (step 2: résumé interrogation, STAR
          story cards, selling points, intro, weaknesses), or "mock" (step 3:
          running a mock and marking a debrief).
    language: "en" or "zh" (中文). Use the language the user writes in.
    """
    key = (step or "overview").strip().lower()
    aliases = {"1": "employer", "step1": "employer", "2": "self", "step2": "self",
               "3": "mock", "step3": "mock", "debrief": "mock", "all": "overview"}
    key = aliases.get(key, key)
    if key not in STEPS:
        return f'Unknown step "{step}". Use one of: {", ".join(STEPS)}.'
    lang = _lang(language)
    text = _strip_frontmatter(_read(lang, STEPS[key]))
    if key == "overview":
        text += ("\n\n---\nServed by the Mock Interviewer MCP server. Where the text says "
                 '"read references/…", call interview_prep_guide with step "employer", '
                 '"self" or "mock". Where it says "assets/", call get_template. To start the '
                 "working folder on the user's computer, call create_prep_folder.")
    return text


@mcp.tool()
def get_template(name: str, language: str = "en") -> str:
    """Return a blank template for one of the prep files, to copy and fill in.

    name: company-dossier, why-them, question-bank, gap-list, story-card,
          selling-points, self-intro or weaknesses.
    language: "en" or "zh".
    Keep the question-bank format exactly: the interviewer parses it.
    """
    n = (name or "").strip().lower().removesuffix(".md").replace("_", "-").replace(" ", "-")
    if n not in TEMPLATES:
        return f'Unknown template "{name}". Available: {", ".join(TEMPLATES)}.'
    return _read(_lang(language), f"assets/{n}.md")


@mcp.tool()
def check_question_bank(markdown: str) -> str:
    """Check a question bank before the user loads it into Mock Interviewer.

    Parses the markdown with the same rules as the interviewer and reports how
    many questions it will load, each question's type and time budget, and
    problems: budgets it cannot read, field names it will ignore, duplicate
    questions, and questions with no prepared opener or best story (the debrief
    is far less useful for those). Pass the full text of question-bank.md.
    """
    qs, unknown = parse_bank(markdown)
    if not qs:
        return ("0 questions found. Each question must start on its own line with '### ' "
                "followed by the question text, with fields below it as '- budget: 120s'.")
    lines, problems, unprepared, seen = [], [], [], {}
    for i, q in enumerate(qs, 1):
        f = q["fields"]
        b = _parse_budget(f.get("budget"))
        if f.get("budget") and b is None:
            problems.append(f'Q{i:02d}: budget "{f["budget"]}" not understood; use 90, 90s or 2m. It will default to 2:00.')
        is_case = bool(re.search(r"case|fact|笔试|案例", f.get("type", ""), re.I)) or bool(f.get("fact"))
        budget = b or (600 if f.get("fact") else 120)
        if not (f.get("opener") or f.get("best")) and not is_case:
            unprepared.append(f"Q{i:02d}")
        k = re.sub(r"\W+", " ", q["text"].lower()).strip()
        if k in seen:
            problems.append(f"Q{i:02d} repeats Q{seen[k]:02d}.")
        seen.setdefault(k, i)
        lines.append(f'Q{i:02d} · {f.get("type") or "no type"} · {_mmss(budget)}{" · case" if is_case else ""} — {q["text"][:90]}')
    total = sum((_parse_budget(q["fields"].get("budget")) or (600 if q["fields"].get("fact") else 120)) for q in qs)
    out = [f"{len(qs)} questions will load. Total budget {_mmss(total)}.", ""] + lines
    if unknown:
        problems.append("Ignored field names (the interviewer will not show them): " + "; ".join(unknown[:12]))
    if unprepared:
        problems.append("No opener or best story yet: " + ", ".join(unprepared) +
                        ". Fill these from the story bank, or list them in gap-list.md.")
    out += ["", "Problems:" if problems else "No problems found."] + [f"- {p}" for p in problems]
    return "\n".join(out)


_DEB_Q = re.compile(r"^###\s*Q(\d+[a-z]?)\s*[—-]\s*(.*)$", re.M)


def _secs(t: str) -> int | None:
    m = re.match(r"\s*(-?)(\d+):(\d{2})", t or "")
    return (-1 if m.group(1) else 1) * (int(m.group(2)) * 60 + int(m.group(3))) if m else None


@mcp.tool()
def read_debrief(markdown: str) -> str:
    """Read the numbers out of a debrief file exported by Mock Interviewer.

    Returns, per question: time against budget, the user's three self-marks,
    whether it was skipped, words spoken, and whether anything was prepared;
    then the questions to re-run first by those measurable signals. Use this
    before marking a debrief, so the time and mark figures are exact, then do
    the judgment part (prepared-vs-said gap, STAR, opening line) yourself and
    fold the results back into question-bank.md, the story cards and gap-list.md.
    """
    md = markdown or ""
    heads = list(_DEB_Q.finditer(md))
    if not heads:
        return "No questions found. Pass the whole debrief .md file exported by Mock Interviewer."
    rows, flags, total = [], [], 0
    for i, h in enumerate(heads):
        body = md[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(md)]
        n, text = h.group(1), h.group(2).strip()
        n = n if not n.isdigit() else f"{int(n):02d}"
        n = re.sub(r"^(\d)([a-z])$", r"0\1\2", n)
        tb = re.search(r"^-\s*(?:time / budget|用时/预算):\s*([-\d:]+)\s*/\s*([-\d:]+)", body, re.M)
        used, bud = (_secs(tb.group(1)), _secs(tb.group(2))) if tb else (None, None)
        marks_line = re.search(r"^-\s*(?:self-marks|自评):\s*(.*)$", body, re.M)
        marks = re.findall(r"=([YN])", marks_line.group(1)) if marks_line else []
        skipped = bool(marks_line and "SKIPPED" in marks_line.group(1))
        prep_line = re.search(r"^-\s*(?:what I prepared|我准备的):\s*(.*)$", body, re.M)
        prepared = bool(prep_line and prep_line.group(1).strip() not in ("—", "-", ""))
        said = re.search(r"\*\*(?:What I actually said|我实际说的)\*\*\s*\n+(.*?)(?:\n\*\*|\n### |\Z)", body, re.S)
        said_txt = (said.group(1).strip() if said else "")
        empty = (not said_txt) or said_txt.startswith("_(")
        words = 0 if empty else len(re.findall(r"[一-鿿]|[A-Za-z0-9'’-]+", said_txt))
        over = used is not None and bud is not None and used > bud
        total += max(used or 0, 0)
        reasons = []
        if skipped: reasons.append("skipped")
        if over: reasons.append(f"over budget by {_mmss(used - bud)}")
        if marks[:1] == ["N"]: reasons.append("no conclusion in the first 15 seconds")
        if marks[1:2] == ["N"]: reasons.append("STAR incomplete")
        if marks[2:3] == ["N"] and prepared: reasons.append("prepared story not used")
        if not prepared: reasons.append("nothing prepared")
        if empty and not skipped: reasons.append("no transcript to check")
        rows.append(f'Q{n} · {_mmss(used) if used is not None else "?"} / {_mmss(bud) if bud is not None else "?"}'
                    f' · marks {"".join(marks) or "—"} · {words} words{" · SKIPPED" if skipped else ""} — {text[:80]}')
        if reasons:
            flags.append((len(reasons) + (2 if skipped or over else 0), f"Q{n}: " + "; ".join(reasons)))
    flags.sort(key=lambda x: -x[0])
    out = [f"{len(rows)} questions answered, {_mmss(total)} in total.", ""] + rows + [""]
    out += (["Re-run first (by measurable signals only; read the transcripts for the rest):"]
            + [f"- {f}" for _, f in flags[:5]]) if flags else ["Nothing flagged by the numbers. Read the transcripts for the prepared-vs-said gap."]
    return "\n".join(out)


@mcp.tool()
def create_prep_folder(employer: str, role: str, parent_dir: str, language: str = "en") -> str:
    """Create the working folder for one application, filled with blank templates.

    Makes <parent_dir>/<employer>-<role>/ with 01_why_them, 02_why_me (and
    stories/), 03_questions and 04_mocks, and copies in the templates. Never
    overwrites an existing file. parent_dir must be an existing folder the user
    named, given as an absolute path (or starting with ~).
    """
    base = pathlib.Path(parent_dir).expanduser()
    if not base.is_absolute():
        return "parent_dir must be an absolute path (or start with ~)."
    if not base.is_dir():
        return f"{base} does not exist. Ask the user which existing folder to use."
    slug = re.sub(r"[^\w一-鿿]+", "-", f"{employer}-{role}".strip().lower()).strip("-") or "interview-prep"
    root = base / slug
    lang = _lang(language)
    made, kept = [], []
    for folder, names in FOLDERS.items():
        (root / folder).mkdir(parents=True, exist_ok=True)
        for n in names:
            dest = root / folder / f"{n}.md"
            if dest.exists():
                kept.append(str(dest.relative_to(base)))
            else:
                dest.write_text(_read(lang, f"assets/{n}.md"), encoding="utf-8")
                made.append(str(dest.relative_to(base)))
    stories = root / "02_why_me" / "stories"
    stories.mkdir(exist_ok=True)
    s01 = stories / "S01.md"
    if s01.exists():
        kept.append(str(s01.relative_to(base)))
    else:
        s01.write_text(_read(lang, "assets/story-card.md"), encoding="utf-8")
        made.append(str(s01.relative_to(base)))
    msg = [f"Folder: {root}"]
    if made: msg.append("Created: " + ", ".join(made))
    if kept: msg.append("Already there, left unchanged: " + ", ".join(kept))
    return "\n".join(msg)


# ------------------------------------------------------------------ prompts
@mcp.prompt()
def interview_prep(employer: str = "", role: str = "", job_posting: str = "") -> str:
    """Start interview prep for one employer and role."""
    parts = ["I have an interview coming up and want to prepare properly."]
    if employer or role:
        parts.append(f"Employer: {employer or '—'}. Role: {role or '—'}.")
    if job_posting.strip():
        parts.append("Job posting:\n\n" + job_posting.strip())
    parts.append('Call interview_prep_guide with step "overview" and follow the method from step 1.')
    return "\n\n".join(parts)


@mcp.prompt()
def mark_debrief(debrief: str) -> str:
    """Mark a debrief exported by Mock Interviewer and fold it back into the prep files."""
    return ("Here is the debrief from my mock interview. Call read_debrief on it first for the "
            "exact times and marks, then interview_prep_guide with step \"mock\", mark it as that "
            "file says, and tell me what to change in my question bank, story cards and gap list.\n\n"
            + (debrief or ""))


def main() -> None:
    if "--version" in sys.argv:
        print(f"mock-interviewer-mcp {VERSION}")
        return
    mcp.run()


if __name__ == "__main__":
    main()
