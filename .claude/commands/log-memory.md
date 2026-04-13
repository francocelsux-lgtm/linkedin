# /log-memory

Log a published post to supermemory. Creates a structured memory entry in `memory/posts/` and updates the hook library and topic map.

Run this 48 hours after every post goes live.

## Usage

```
/log-memory
```

Then provide the post details when prompted, or pass them inline:

```
/log-memory
Date: 2026-04-14
Hook: "El 80% de los team buildings no cambian nada. Aquí está el problema."
Format: hot-take
Pillar: Cultura que transforma
Impressions: 4200
Reactions: 187
Comments: 43
Reposts: 12
```

---

## What this command does

### Step 1 — Collect Post Data
Ask for (or parse from input):
- Date published
- Full post hook (first line, exact text)
- Format: story | list | framework | hot take | curation | question
- Pillar: Cultura que transforma | El arte del evento | RRHH estratégico | Liderazgo y equipos | Historias de campo
- Hook pattern used (from hook library)
- Metrics: impressions, reactions, comments, reposts

### Step 2 — Calculate Engagement Rate
```
engagement_rate = (reactions + comments + reposts) / impressions × 100
```

### Step 3 — Assign Performance Tier
- **A**: Top 20% — high impressions + engagement rate above 5%
- **B**: Solid — engagement rate 2-5%
- **C**: Below average — engagement rate under 2% or low impressions

### Step 4 — Write Memory Entry
Create file at `memory/posts/YYYY-MM-DD-[slug].md`:

```markdown
## Post Memory Entry

**Date published:** YYYY-MM-DD
**Topic:** [one-line summary]
**Format:** [format]
**Pillar:** [pillar]
**Hook pattern:** [pattern name]
**Hook text:** [exact first line]

### Performance Metrics
- Impressions: 
- Reactions: 
- Comments: 
- Reposts: 
- Engagement rate: X.X%
- "See more" estimated: [high / medium / low]
- Follower gain attributed: 

### Qualitative Notes
**What worked:**

**What could be improved:**

**Audience reaction (what comments revealed):**

**Unexpected outcome:**

### Tags
[topic tags] [format] [hook pattern] [tier: A / B / C]
```

### Step 5 — Update Hook Library
In `memory/hook-library.md`:
- Find the hook pattern used
- Add this post as a data point (date, tier, engagement rate)
- Update the pattern's average performance score

### Step 6 — Update Topic Map
In `memory/topic-map.md`:
- Mark the topic as used
- Record the date and performance tier
- Note: "ready to revisit in [30/60/90] days" based on tier

---

## Scaffold Memory Folders

If `memory/` doesn't exist yet, this command creates the full structure:

```
memory/
  posts/
  weekly-logs/
  monthly-logs/
  hook-library.md
  topic-map.md
  competitor-log.md
```
