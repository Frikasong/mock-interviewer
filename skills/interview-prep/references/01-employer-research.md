# Step 1 — Employer research

Goal: turn "who are they and what do they want" into three files that can be cited over and over.

---

## 1. Tear down the job description

Read it line by line and derive one or two likely questions from each responsibility.

| JD line | What it tests | Likely question |
|---|---|---|
| Manage relationships with internal and external stakeholders | Cross-functional friction | Tell me about a time you had to push back on someone senior. |
| Work in a fast-paced environment with competing deadlines | Triage under pressure | Three deadlines land on the same day. Walk me through how you'd handle it. |
| Draft submissions and correspondence | Writing, audience awareness | How do you adjust your writing for a non-specialist reader? |

Two things to notice while reading:

**Verb tier.** *Support / assist / contribute* roles are testing reliability and speed of learning. *Lead / own / develop* roles are testing judgment and accountability. The same story gets told differently depending on which one you're answering.

**The odd item.** One requirement that doesn't fit the rest of the role — a back-office post that mentions public-facing communication, a research post that mentions stakeholder briefings — is usually a real pain point on the team, and gets asked about far more often than its prominence suggests.

## 2. Company dossier

Search for this. Cover:

- **Business model and revenue** — for a government body or regulator: enabling statute, who they regulate, how they're funded
- **Structure** — which unit this role sits in, who it reports to, what that unit does
- **Last twelve months** — product launches, results, leadership changes, regulatory or industry shifts, strategy documents (for public bodies: business plan, annual report, statement of priorities)
- **Which real business lines the JD's responsibilities map onto**
- **Three concrete things that distinguish them from peers** — answered separately, because it's the raw material for why-them

Every entry gets a date and a source link. Nothing goes in from memory. Uncertain items get marked `[unverified]`.

Prompt to use with web search:

```
Research [organisation]: core business and structure; key developments in the last
12 months (launches, results, leadership, regulatory or industry change); and which
of their real business lines each responsibility in this job posting maps onto.
Output markdown with a date and source link for every entry.
Then answer separately: three concrete things that distinguish them from peers.
```

## 3. Why them, in three layers

Not the values page. Not "industry leader with a great culture."

**Layer one — why my trajectory points here.** Past choices form a line whose endpoint is this role. Facts, not adjectives: courses taken, projects built, where you interned, what you wrote.

**Layer two — what I actually think about their business or direction.** You've read the annual report, the strategy document, the recent regulatory development, and you have a specific view. This is the layer that separates candidates, because most stop at layer one. The view doesn't have to be contrarian, but it has to be specific enough to survive a follow-up question.

**Layer three — what I want to work on.** Name the unit, the business line, the live initiative, and what you'd contribute.

**The test:** cover the organisation's name. Could this go to their closest competitor unchanged? If yes, rewrite it.

## 4. Question bank

Sources, roughly in order of reliability:

- Questions derived from the JD (section 1 above)
- The organisation's own published hiring process — public bodies and regulators frequently publish a competency framework, and preparing against it directly is unusually high-yield
- Alumni, current employees, anyone one degree away — the best source, and worth the awkwardness of asking
- Published interview reports: Glassdoor, Reddit, local job forums, LinkedIn posts by their employees
- Standard question sets for the role type

Sort into four buckets:

- **Motivation** — why this role, why us, why leave, where next
- **Behavioural** — "tell me about a time…", answered with STAR
- **Situational** — "what would you do if…", answered with a decision framework first, then a conclusion
- **Employer-specific** — only this organisation asks it: their mandate, a recent event, a written or technical exercise

Keep the format strict, because tooling reads it:

```markdown
### Tell me about a time you disagreed with a supervisor.
- type: behavioural
- best story: S03
- backup: S07
- opener: I raised it early, in writing, and framed it as a risk to the file rather than a disagreement.
- watch: no more than two sentences of background
```
