# LinkedIn Posts — AI Writing System

A skill-based system for writing high-performing LinkedIn posts using continuous learning, competitor analysis, viral hooks, and a consistent personal brand voice.

**Account:** Luis Durruty — CEO Celsux | RRHH | +3.000 eventos en LATAM y el mundo

## Repository Structure

```
.
├── README.md                    # This file — system overview
│
├── — SKILL FILES —
├── celsux-voice.md              # Brand voice, tone, and style guide
├── deep-research-skill.md       # How to research topics, profiles, and competitors
├── supermemory-skill.md         # How to retain and recall what has worked
├── best-practices.md            # LinkedIn formatting, hooks, and engagement rules
├── content-research-writer.md   # End-to-end workflow for writing a post
├── claude-api-skill.md          # Automate batch drafting and analysis via Claude API
│
├── — PROFILE & STRATEGY —
├── profile-analysis.md          # Luis Durruty profile analysis, audience, pillars
│
├── — CLAUDE CODE INTEGRATION —
├── .claude/
│   ├── settings.json            # Hooks config (session-start + stop reminder)
│   ├── hooks/
│   │   └── session-start.sh     # Auto-runs on every session start
│   └── commands/
│       ├── draft-post.md        # /draft-post — full post creation workflow
│       ├── research-trends.md   # /research-trends — topic and competitor research
│       ├── weekly-review.md     # /weekly-review — weekly learning loop
│       ├── generate-hooks.md    # /generate-hooks — 5 scored hook variations
│       └── log-memory.md        # /log-memory — log post to supermemory
│
├── — MEMORY (persistent learning) —
│   └── memory/
│       ├── posts/               # One .md file per published post (48h after publish)
│       ├── weekly-logs/         # Weekly learning loop entries
│       ├── monthly-logs/        # Monthly strategy reviews
│       ├── hook-library.md      # Hook patterns + performance data
│       ├── topic-map.md         # Topics tried, tier, last used, revisit date
│       └── competitor-log.md    # Competitor audit observations over time
│
└── — FEW-SHOT DATA PIPELINE —
    ├── data/
    │   ├── raw_posts.json       # Luis's published posts (text + engagement + date)
    │   └── preprocessed.json   # Auto-enriched: tags, format, hook_pattern, tier
    └── scripts/
        ├── preprocess_posts.py  # LLM pipeline: raw → preprocessed (run after adding posts)
        ├── few_shots.py         # FewShotPosts: filter examples by pillar/length/language/tier
        ├── post_generator.py    # Generate posts with few-shot examples via Claude API
        └── requirements.txt     # anthropic, pandas, langchain-core
```

## How the Skills Connect

```
Research         → /research-trends  → deep-research-skill.md
        ↓
What Works       → memory/ + data/   → supermemory-skill.md + few_shots.py
        ↓
Write Draft      → /draft-post       → content-research-writer.md
        ↓  (or batch: post_generator.py with few-shot examples)
Apply Voice      →                   → celsux-voice.md
        ↓
Polish & Publish →                   → best-practices.md
        ↓
Log & Learn      → /log-memory       → memory/posts/
        ↓
Weekly Review    → /weekly-review    → memory/weekly-logs/
```

## Slash Commands

| Command | What It Does | Powered By |
|---|---|---|
| `/draft-post [topic]` | Full post creation, 6-phase workflow | content-research-writer + celsux-voice + best-practices |
| `/research-trends [topic]` | Deep research on topic, competitor, or weekly trend scan | deep-research-skill |
| `/generate-hooks [topic]` | 5 scored hook variations, ranked | celsux-voice + hook-library |
| `/weekly-review` | Weekly learning loop, update memory | supermemory-skill |
| `/log-memory` | Log published post + metrics to memory | supermemory-skill |

**Automate the weekly review with the loop skill:**
```
/loop 1w /weekly-review
```

## Few-Shot Data Pipeline

The generation quality compounds as Luis publishes more posts. The pipeline:

```
1. Add post to data/raw_posts.json  (text + engagement + date)
2. python scripts/preprocess_posts.py   → enriches with tags, format, tier
3. Few-shot examples are now available for future generation
4. Quality of generated drafts improves automatically
```

**Adding a new post to the dataset:**
```json
{
  "text": "full post text here",
  "engagement": 1842,
  "date": "2026-04-14",
  "url": "https://www.linkedin.com/posts/luis-durruty-..."
}
```

Then run:
```bash
cd /path/to/linkedin-posts
pip install -r scripts/requirements.txt
python scripts/preprocess_posts.py
```

**Generating a batch of posts from a content plan:**
```python
from scripts.post_generator import batch_draft

plan = [
    {"tag": "Cultura que transforma", "length": "Medium", "language": "Spanish",
     "format_type": "hot-take", "hook_pattern": "Bold claim"},
    {"tag": "RRHH estratégico", "length": "Short", "language": "Spanish",
     "format_type": "question", "hook_pattern": "Direct challenge"},
]
drafts = batch_draft(plan)
for d in drafts:
    print(d["draft"])
```

---

## Core Mission

Write LinkedIn posts that:
- Build a recognizable personal brand (Celsux voice)
- Speak directly to RRHH directors and People leads
- Use few-shot examples from Luis's own best posts so every draft sounds like him
- Continuously improve from data logged in memory and the dataset
- Stay ahead of competitors in the cultura/eventos corporativos space

## Quick Start

1. Run `/research-trends` to see what's moving in the niche
2. Pick a topic from `memory/topic-map.md` (or a fresh idea)
3. Run `/draft-post [topic]` to create the full post
4. Publish — put external links in the first comment, not the body
5. 48 hours later: run `/log-memory` and add the post to `data/raw_posts.json`
6. Run `python scripts/preprocess_posts.py` to enrich the dataset
7. Every Monday: run `/weekly-review` (or set `/loop 1w /weekly-review`)
