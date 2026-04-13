# /draft-post

Draft a LinkedIn post for Luis Durruty (Celsux) from start to finish, following the full content-research-writer workflow.

## What this command does

Walks through all 6 pre-publish phases defined in `content-research-writer.md`, applying the voice from `celsux-voice.md` and validating against `best-practices.md`.

## Usage

```
/draft-post [topic or idea]
```

**Examples:**
- `/draft-post por qué el 80% de los team buildings no funcionan`
- `/draft-post historia: el evento que casi sale mal y lo que aprendimos`
- `/draft-post 5 señales de que tu cultura corporativa necesita una intervención`

---

## HubSpot Context

Before drafting, check `data/hubspot/context.md` for relevant CRM data:
- Is the client (if mentioned) in the Closed Won list? → Use specific event details (activity name, attendee count, city)
- Is a similar company in the active pipeline? → The post can address their objections or aspirations without naming them
- Are there recent Closed Won events that haven't been turned into posts yet? → Content goldmine

Never include in the post: deal amounts, pipeline stages, internal notes, or any data marked confidential.

---

## Workflow

### Phase 1 — Research Brief
Fill out the research brief before writing a single word:

```
Topic: $ARGUMENTS
Pillar: [Cultura que transforma | El arte del evento | RRHH estratégico | Liderazgo y equipos | Historias de campo]
Core claim: 
Proof / anchor:
Target reader:
Hook pattern (from hook-library):
Competing content found:
Differentiated angle:
Post format: [story | list | framework | hot take | curation | question]
Closer / CTA:
```

### Phase 2 — Write 5 Hooks
Generate 5 different hooks for this topic. Score each one:
- Specificity (names a number, person, or thing)
- Tension (creates a gap to close)
- Relevance (speaks to RRHH/culture buyer)
- Voice match (sounds like Luis Durruty / Celsux)

Select the strongest hook. Explain why.

### Phase 3 — Draft the Body
Write the full post using the selected hook + the appropriate format template from `content-research-writer.md`.

Rules:
- Lead with the conclusion
- One idea only
- Show, don't tell — use a specific number, name, or scene
- Cut the first paragraph if it's a warm-up

### Phase 4 — Voice Pass
Apply the Celsux voice filter from `celsux-voice.md`:
- Replace any corporate jargon
- Make passive voice active
- Cut all hedging phrases
- Read aloud test

### Phase 5 — Format Pass
Apply formatting from `best-practices.md`:
- Line breaks after every 1-3 sentences
- No external link in body
- Max 3 hashtags
- Bold used once

### Phase 6 — Pre-Publish Review
Answer these 5 questions before delivering the final draft:
1. Does the first line stop a scroll?
2. Is every sentence necessary?
3. Does it sound like a real person, not a content machine?
4. Is there one clear takeaway?
5. Is the voice consistent with Celsux?

---

## Output Format

Deliver:
1. The final post (ready to copy-paste into LinkedIn)
2. Recommended hashtags (max 3)
3. Link placement note (if a URL is needed, note it goes in first comment)
4. One-line summary for logging to supermemory
