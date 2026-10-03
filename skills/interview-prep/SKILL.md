---
name: interview-prep
description: Interview prep in three steps — research the employer (dossier and a defensible "why them"), research yourself (STAR story bank, selling-point matrix, self-introduction, prepared weaknesses), then run timed mock interviews and fold every debrief back into that material. ALWAYS use this skill whenever the user mentions an upcoming interview or 面试, pastes a job posting or job description, asks for STAR stories or wants an answer polished, says 面经 / behavioural question / competency question / "why this firm" / "why me" / "tell me about yourself", wants to research a target employer, asks to practise or run a mock interview, or pastes a mock-interview debrief or transcript to be marked — even if they never use the words "interview prep". Also use when they name an employer and a role together and ask where to start.
---

# Interview Prep — Research, Story Bank, Mock

Interview outcomes turn on **fit**, and fit has two halves: knowing the employer (why them) and knowing yourself (why me). An AI can only say something substantive about either one if it can read real material about both. Without that material it produces universal-sounding answers that fit any candidate and any employer — which is exactly what loses interviews.

So this skill produces material first and practises against it second. Three steps, in order:

| Step | Question it answers | Output |
|---|---|---|
| 1. Research the role | Who are they, what are they actually testing? | `company-dossier.md`, `why-them.md`, `question-bank.md` |
| 2. Research yourself | Who am I, where is my evidence? | `stories/S01…Sn.md`, `selling-points.md`, `self-intro.md`, `weaknesses.md` |
| 3. Mock interview | What do I drop under pressure? | `debrief-<date>.md`, plus updates to everything above |

If the user opens with "just run a mock interview" and has no material from steps 1 and 2, build a minimum viable version first — five questions from the JD, three story cards, a 30-second intro. A mock against an empty story bank teaches nothing, because there is nothing to compare the performance against. Say this in one line and get on with it rather than lecturing.

## Working files

Create a folder named for the employer. Everything lands on disk so it can be reused for the next role and read back by any AI tool later.

```
<employer>-<role>/
├── 01_why_them/   company-dossier.md, why-them.md
├── 02_why_me/     stories/, selling-points.md, self-intro.md, weaknesses.md
├── 03_questions/  question-bank.md, gap-list.md
└── 04_mocks/      debrief-<date>.md (one per session)
```

Blank templates for each file are in `assets/`. Copy and fill rather than inventing a new format — the question bank format in particular is read by Mock Interviewer.

## Language

Notes and discussion can be in whatever language the user prefers, but **anything they will say out loud — STAR stories, self-introduction, why-them, answer openers — must be written in the language the interview is conducted in**. Thinking it through in a first language and translating live is the most common cause of a slow, hedged, conclusion-less answer.

If the interview language isn't obvious, ask. For cross-language cases (a Chinese-native speaker interviewing in English), write the story cards in English and leave a single first-language memory anchor at the bottom of each card.

## Step 1 — Research the role

Read `references/01-employer-research.md`. Four outputs:

1. **Tear down the job description line by line.** Every listed responsibility hides one or two questions. A JD is not an advertisement, it's a syllabus.
2. **Build the dossier** — business or statutory mandate, structure, the last twelve months of material events. Search for this; cite dates and sources. Anything uncertain gets marked `[unverified]` rather than smoothed over.
3. **Write "why them" in three layers** — why my trajectory points here → what I actually think about their business or direction → what specifically I want to work on. Then apply the test: *if this answer could be pasted into an application to their closest competitor without changing a word, it isn't ready.* Run the test yourself before showing it to the user.
4. **Build the question bank** — JD-derived questions, published interview reports, role-type standards, sorted into motivation / behavioural / situational / employer-specific. Keep the format strict (`###` per question); Mock Interviewer parses it.

## Step 2 — Research yourself

Read `references/02-story-bank.md`.

Start by interrogating the résumé **line by line** against the JD — every line, not the highlights. The user can't predict which experience an interviewer will find interesting, and full coverage is where fluency and confidence come from. Hand them the question list and let them answer it.

**Never invent experience, numbers, or outcomes.** The material has to come from them. When an answer is vague, push: what did *you* do as distinct from the team, what number attached to it, who objected, what happened afterwards. Vagueness is usually modesty or forgetting, not absence — people who solved a hard problem tend to describe it as though it wasn't hard.

Then turn the raw material into 10–15 numbered STAR cards (S01, S02…), one file each, each tagged with the question types it can answer. Proportions matter: Situation gets a sentence or two, Action takes more than half and its subject is "I" rather than "we", Result carries a number wherever one exists.

Finish with the selling-point matrix (the employer's three most-valued traits × the stories that evidence them), a 30-second and 90-second self-introduction, and a prepared weakness in three parts — candid, what's already being done about it, why it doesn't compromise this role.

**Reconcile before moving on.** Fill in every question in the bank with its best story, backup story and a one-line opener. Anything with no good story goes into `gap-list.md`. That list is what the user should spend their remaining time on — not re-rehearsing questions they can already answer.

## Step 3 — Mock interview

Read `references/03-mock-and-debrief.md`. Two ways to run it:

- **Mock Interviewer** (github.com/Frikasong/mock-interviewer) — a single HTML file opened in Chrome, with video, live transcript and a per-question clock. The user loads `question-bank.md` (paste it, or use the file button), pastes `selling-points.md`, `self-intro.md` and the story cards they expect to use into the "What you prepared" box, and answers. At the end it downloads a `debrief-….md` with a coaching prompt at the top. It runs entirely in the browser and cannot write to their folder, so tell them to save that file into `04_mocks/` and bring it back here.
- **In conversation** — you play the interviewer: one question at a time, state the time budget, wait for the answer, ask the follow-up a real panel would ask, then give feedback before the next question. Never fire off the whole list and grade in bulk; that's an exam, not an interview.

**The fold-back is the point of the step.** When a debrief comes back, mark it against the four questions in its header (conclusion in 15 seconds, STAR completeness, time against budget, prepared-vs-said gap), then *edit the files*: sharpen openers and `watch:` lines in `question-bank.md`, revise or add story cards, update `gap-list.md`, and add any real follow-up the user couldn't handle as a new question. Feedback that stays in the chat is gone by the next session; feedback written into the bank compounds. Three sessions in, the bank fits the user's own weak points better than any published interview report.

## Boundaries

- Don't fabricate the user's experience, metrics, or achievements. Ask, structure, and sharpen — that's the whole job.
- Don't promise outcomes. Preparation changes the odds, not the result.
- Facts about a specific employer (financials, regulatory developments, reorganisations) get searched and sourced, never written from memory.

## Reference files

- `references/01-employer-research.md` — JD teardown, dossier, three-layer why-them, question bank and where to find real questions
- `references/02-story-bank.md` — résumé interrogation prompts, STAR cards, selling-point matrix, self-introduction, weaknesses
- `references/03-mock-and-debrief.md` — running a mock (in the tool or in conversation), marking a debrief, folding it back into the files
- `assets/` — blank templates for every output file
