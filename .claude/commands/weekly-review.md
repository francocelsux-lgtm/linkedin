# /weekly-review

Run the weekly learning loop from `supermemory-skill.md`. Reviews the week's posts, assigns performance tiers, extracts insights, and updates memory.

Pair with the **loop skill** to run this automatically every Monday morning:
```
/loop 1w /weekly-review
```

## Usage

```
/weekly-review [optional: week ending date YYYY-MM-DD]
```

**Examples:**
- `/weekly-review`
- `/weekly-review 2026-04-20`

---

## What this command does

### Step 1 — Collect Posts
List all posts published this week. For each:
- Date published
- Topic / hook (first line)
- Format used
- Pillar

### Step 2 — Pull Metrics
For each post, record:
- Impressions
- Reactions
- Comments
- Reposts
- Engagement rate = (reactions + comments + reposts) / impressions × 100
- Estimated "see more" click rate: high / medium / low (infer from comment depth)

### Step 3 — Assign Performance Tiers

| Tier | Criteria |
|------|----------|
| A | Top 20% — high impressions + above-average engagement rate |
| B | Average — solid but not viral |
| C | Below average — low reach or shallow engagement |

### Step 4 — Extract Learnings

Answer:
- What made the A-tier post(s) work? (hook? topic? format? timing?)
- What went wrong with C-tier posts? (hook failure? wrong topic? timing?)
- What did the comments reveal about audience interests?
- What format hasn't been used recently that has historically worked?

### Step 5 — Update Memory Files

1. Write weekly log to `memory/weekly-logs/YYYY-WW.md` using this template:

```markdown
## Weekly Learning Log — Week of [DATE]

**Posts published:** [N]
**Best performing post:** [hook] — [tier] — [why it worked]
**Lowest performing post:** [hook] — [tier] — [diagnosis]

**Key insight this week:**

**Audience observation:**

**Hypothesis to test next week:**

**Hook pattern to double down on:**

**Hook pattern to retire or rest:**

**Content pillar to prioritize next week:**
```

2. Update `memory/hook-library.md` — add performance data for any hooks used
3. Update `memory/topic-map.md` — mark topics used, update last-used dates, note resonance level

### Step 6 — Next Week Plan

Recommend:
- 3-5 post ideas for next week based on learnings
- 1 experiment to run (new format, hook pattern, or topic angle)
- Optimal posting days/times based on this week's data

---

## Loop Skill Integration

To automate this review every Monday at 9 AM, use:

```
/loop 1w /weekly-review
```

The loop skill will run `/weekly-review` on a weekly interval, keeping the supermemory current without manual effort.
