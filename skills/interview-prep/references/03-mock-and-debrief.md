# Step 3 — Mock interview and debrief

A mock is a measuring instrument, not a rehearsal. Its job is to show the distance between what the user prepared and what comes out of their mouth under a clock. Everything in this file serves that one measurement.

## 3.1 Before the session

- **Pick 5–8 questions, not the whole bank.** Mix types the way a real panel would: one motivation, three or four behavioural, one situational, one employer-specific. Put at least one item from `gap-list.md` in every session — the user will avoid those on their own.
- **Set budgets from the format, not from comfort.** 90–120s for behavioural, 150s for situational, 60–90s for the opening "tell me about yourself". Use the `budget:` field so the tool's clock enforces it.
- **Say what's being measured.** One line before starting: conclusion in the first 15 seconds, STAR with a result, inside the budget, and whether the prepared story actually got used.

## 3.2 Running it in Mock Interviewer

1. Open `index.html` in Chrome (live transcript only works in Chrome or Edge).
2. Load `03_questions/question-bank.md` — paste it, or use the file button. The question count appears next to the box; if it reads zero, a `###` heading is missing.
3. Paste into "What you prepared": `selling-points.md`, the 30-second `self-intro.md`, and the story cards for this session's questions. Skip this and the debrief can only say how long they talked.
4. Answer. `Space` starts, stops and advances. Correct obvious transcription errors in proper nouns before moving on.
5. Download the debrief `.md` (and recordings, if they want to watch themselves). Save it to `04_mocks/`.

The tool contains no AI and uploads nothing. The marking happens when the user brings the debrief back to you.

## 3.3 Running it in conversation

You are the interviewer, then the coach — never both at once.

- **Ask one question.** Quote the budget ("about two minutes"). Then stop and wait.
- **Don't help mid-answer.** No hints, no "great start". A panel gives nothing back while you're talking.
- **Ask one follow-up**, the one a real panel would ask: *What did you personally do? What would you do differently? How did you measure that? Who disagreed?* Follow-ups are where rehearsed answers fall apart, so they're the most valuable part of the mock.
- **Then switch to coach** and give feedback in the four-point format below before asking the next question.

If the user typed rather than spoke, say so in the feedback — written answers hide the hedging, filler and slow openings that speaking exposes. Recommend at least one session in the tool or out loud before the real thing.

## 3.4 Marking a debrief

Whether it came from the tool or from the conversation, mark each answer on the same four points. The tool's exported file asks for exactly these in its header prompt.

| Point | What to look for |
|---|---|
| Conclusion in 15 seconds | Did the first sentence answer the question? Quote the sentence they actually opened with. |
| STAR completeness | Is there a Result, and does it have a number? Is the subject of the Action "I"? |
| Time against budget | Over: name the sentence to cut (almost always Situation). Under: name what's missing (usually Result or the link back to the employer). |
| Prepared vs said | Which prepared point, story or opener got dropped? **This is the one that matters most.** Name it specifically. |

Score each answer 1–5 and write one better opening line they could say verbatim, in the interview language. Finish with the three questions to re-run first.

Be direct. "Good answer overall" teaches nothing; "you opened with two sentences about the team's structure and reached your actual decision at 0:48" does.

## 3.5 Folding it back

This is what separates a question bank that improves from one that's practised into the ground. After marking, edit the files — don't leave the findings in the chat.

| What the debrief showed | Where it goes |
|---|---|
| A better opener | Replace `opener:` on that question in `question-bank.md` |
| A habit to watch (long setup, "we" instead of "I", no number) | Add or sharpen `watch:` on that question |
| The prepared story didn't fit the question | Change `best story:` / `backup:`, or revise the card in `stories/` |
| A new story surfaced while answering | Write it up as a new card (next S number) — this happens more often than people expect |
| A question they couldn't answer at all | Add to `gap-list.md` with what's missing |
| A follow-up that broke the answer | Add it to the bank as its own question, tagged `source: mock · <date>` |
| Questions asked in a *real* interview | Add them tagged `source: actual · <org> · <date>`; these outrank everything else |

Confirm changes with the user before overwriting a story card — the facts in it are theirs.

## 3.6 Cadence

- **Three sessions** is the useful minimum: the first measures the baseline, the second tests the fold-back, the third checks it held.
- **Re-run the top three** from the last debrief at the start of the next session, before any new question.
- **Shuffle order** between sessions so the user isn't memorising a sequence.
- **In the last 48 hours**, stop adding stories. Only sharpen openers, re-read the dossier, and do one short session to warm up — not a full one that leaves them drained.
