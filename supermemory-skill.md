# Supermemory Skill

## Purpose

Build a persistent, queryable memory of everything that has worked, failed, and been learned about LinkedIn content — so the system improves continuously instead of starting from scratch with every post.

---

## What Supermemory Stores

Supermemory is the long-term brain of the content system. It retains:

1. **Post performance records** — what was written, how it performed, why
2. **Hook effectiveness data** — which hook patterns get the highest "see more" clicks
3. **Format performance** — lists vs. stories vs. frameworks vs. hot takes
4. **Topic resonance** — which subjects drive deep comments vs. shallow likes
5. **Audience insights** — what the audience cares about, based on engagement signals
6. **Failed experiments** — what was tried and didn't work (equally important)
7. **Competitor learnings** — what worked for competitors and what the takeaway is
8. **Recurring patterns** — angles, phrases, or formats that consistently outperform

---

## Memory Schema

Every post that gets published should be logged with the following structure:

```markdown
## Post Memory Entry

**Date published:** YYYY-MM-DD
**Topic:** [one-line topic summary]
**Format:** [story | list | framework | hot take | curation | question | poll]
**Hook pattern used:** [pattern name from hook library]
**Hook text (first line):** [exact text]

### Performance Metrics (update 48h after posting)
- Impressions:
- Reactions:
- Comments:
- Reposts:
- Engagement rate (%):
- "See more" estimated clicks: [high / medium / low based on comment ratio]
- Follower gain attributed: [if trackable]

### Qualitative Notes
- What worked about this post:
- What could be improved:
- Audience reaction patterns (what comments revealed):
- Unexpected outcome (if any):

### Tags
[topic tags] [format tag] [hook pattern tag] [performance tier: A / B / C]
```

---

## Performance Tiers

Classify every post into a tier after 48 hours:

| Tier | Criteria                                          | Action                                   |
|------|---------------------------------------------------|------------------------------------------|
| **A** | Top 20% — high impressions + high engagement    | Reverse-engineer and replicate format    |
| **B** | Average performance — solid but not viral        | Note what worked, tweak and retry        |
| **C** | Below average — low reach or low engagement      | Diagnose: was it hook, topic, or timing? |

---

## Memory Queries

When researching a new post, query supermemory with these questions:

- "What hook patterns produced A-tier posts in the last 90 days?"
- "Which topics drove the most comments (not just likes)?"
- "What's the last time I wrote about [topic X]? How did it perform?"
- "What formats have I NOT used recently that historically performed well?"
- "What did my top competitor post that got outsized engagement? What was the angle?"
- "What experiments have I tried that failed? Why?"

---

## Learning Loops

### Weekly Learning Loop

At the end of each week:
1. Pull all posts from the week
2. Assign performance tiers
3. Extract 1-3 learnings from A-tier posts
4. Extract 1-2 learnings from C-tier posts
5. Update the hook library and format preferences based on data
6. Note any topic or audience shift observed

```markdown
## Weekly Learning Log — [Week of YYYY-MM-DD]

**Best performing post:** [title/hook] — [why it worked]
**Lowest performing post:** [title/hook] — [diagnosis]
**Key insight this week:**
**Hypothesis to test next week:**
**Hook pattern to retire (if any):**
**Hook pattern to double down on:**
```

### Monthly Learning Loop

At the end of each month:
1. Review all A-tier posts — find patterns across them
2. Review competitor evolution — what changed in their strategy?
3. Update the voice guide if the audience has shifted
4. Set 1-2 content experiments for next month
5. Identify the top 3 performing topics for the month

---

## Memory for Continuous Improvement

The supermemory system enables compound learning. Over time it answers:

- What is the single best-performing hook pattern for this account?
- How has audience engagement evolved over the past 6 months?
- Which topics have a short shelf life vs. evergreen value?
- What is the optimal post length for this audience?
- Are there seasonal patterns (certain topics spike at certain times)?
- What is the correlation between posting frequency and follower growth?

---

## Integration with Other Skills

| Skill                     | How Supermemory Feeds It                                 |
|---------------------------|-----------------------------------------------------------|
| `deep-research-skill`     | Informs which topics are already covered or overdone      |
| `content-research-writer` | Pre-loads the best hook patterns and formats for a draft  |
| `celsux-voice`            | Captures evolving audience preferences to refine voice    |
| `best-practices`          | Updates which practices are currently yielding results    |

---

## Memory Storage Format

Organize memory entries in a folder structure:

```
/memory
  /posts
    YYYY-MM-DD-[slug].md     # one file per published post
  /weekly-logs
    YYYY-WW.md               # one file per week
  /monthly-logs
    YYYY-MM.md               # one file per month
  /hook-library.md           # living document of hook patterns + performance data
  /topic-map.md              # topics tried, performance tier, last used date
  /competitor-log.md         # competitor observations over time
```
