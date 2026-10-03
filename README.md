# Mock Interviewer

English · [中文](README.zh.md)

![Mock Interviewer — one question, a real clock, a debrief that knows what you prepared](docs/demo.gif)

Two things that work together, and work separately.

1. **A skill** for Claude — builds the two research assets that make interview preparation actually work: an employer dossier with a defensible *why them*, and a STAR story bank with the evidence behind *why me*. Available in English and 中文.
2. **The interviewer** (`interviewer/index.html`) — a single HTML file you open in Chrome to practise against a real clock, with video, transcript, and a debrief your AI coach can mark up.

The premise behind both: **interview outcomes turn on fit, and an AI can only say something useful about fit if it can read real material about you and about them.** Ask a model to "run a mock interview" cold and it produces answers that fit any candidate and any employer — which is exactly what loses interviews. So the skill produces material first, and the interviewer measures your performance against it.

---

## Install the skill

```bash
git clone https://github.com/Frikasong/mock-interviewer.git
cd mock-interviewer
./install.sh en        # English edition; ./install.sh for 中文
```

The installer copies the skill into `~/.claude/skills` and warns you if the other
language edition is already sitting there — the two compete for the same requests,
so install one. Restart Claude Code afterwards.

**Claude.ai** — download the `.skill` file from [Releases](../../releases) and upload it
under Settings → Capabilities → Skills.

**Neither** — paste `skills/interview-prep/SKILL.md` into a conversation. It works; you
just re-paste it each time.

Then describe your situation rather than naming the skill: *"I'm interviewing at
Tidewater Outfitters for a product marketing role next Thursday, here's the posting."*
It takes it from there.

## Run the interviewer

Download [`interviewer/index.html`](interviewer/index.html) and open it
in Chrome. That is the entire installation procedure — no Node, no server, no API key, no
account. See [its README](interviewer/README.md) for the question format and
browser support.

---

## How they fit together

```
   skill                                  interviewer
   ─────                                  ───────────
   step 1  employer research  ──┐
           dossier, why-them    │
           question-bank.md  ───┼──────────►  loads directly
                                │            (### question + fields)
   step 2  self research      ──┤
           story cards S01…   ───┼──────────►  pasted as "what you prepared"
           selling points       │
                                │
   step 3  mark the debrief  ◄──┴──◄──────── debrief.md comes back:
                                             answered badly → back to the bank
                                             new story surfaced → new card
```

Three sessions in, your question bank is more accurate than any published interview report, because it grew around your own weak points rather than someone else's.

## Repository layout

```
mock-interviewer/
├── build.py                    builds every release artifact
├── DEPLOY.md                   release process
├── skills/
│   ├── interview-prep/         English skill
│   │   ├── SKILL.md
│   │   ├── references/         employer research · story bank · mock & debrief
│   │   └── assets/             blank templates for every output
│   └── interview-prep-zh/      中文版，结构相同
├── interviewer/
│   ├── index.html              the whole tool
│   ├── README.md
│   └── scripts/                five ready-made question banks
├── install.sh                  copies the skill into ~/.claude/skills
├── docs/                       release notes for other channels
└── LICENSE
```

## Design notes

A few decisions worth stating, since they're the ones people usually ask about:

**The skill never writes your experience for you.** It interrogates, structures, and sharpens; the facts have to come from you. A fabricated story survives exactly one follow-up question, and the failure mode is worse than having no story.

**The interviewer contains no AI.** No key, no cost, no recording of yours passing through anyone's inference. The debrief is a markdown file designed to be pasted into whatever assistant you already use, with the coaching prompt written at the top.

**Nothing is uploaded, ever.** Video, audio and transcript live in the browser tab and are discarded when you close it unless you download them first. For a file full of your own unrehearsed interview answers, that is the correct default.

## Licence

MIT — see [LICENSE](LICENSE).
