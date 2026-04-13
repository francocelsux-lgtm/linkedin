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
└── — MEMORY (persistent learning) —
    └── memory/
        ├── posts/               # One .md file per published post (48h after publish)
        ├── weekly-logs/         # Weekly learning loop entries
        ├── monthly-logs/        # Monthly strategy reviews
        ├── hook-library.md      # Hook patterns + performance data
        ├── topic-map.md         # Topics tried, tier, last used, revisit date
        └── competitor-log.md    # Competitor audit observations over time
```

## How the Skills Connect

```
Research         → /research-trends  → deep-research-skill.md
        ↓
What Works       → memory/           → supermemory-skill.md
        ↓
Write Draft      → /draft-post       → content-research-writer.md
        ↓
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

## Core Mission

Write LinkedIn posts that:
- Build a recognizable personal brand (Celsux voice)
- Speak directly to RRHH directors and People leads
- Leverage viral hooks and proven formats
- Continuously improve from data logged in memory
- Stay ahead of competitors in the cultura/eventos corporativos space

## Quick Start

1. Run `/research-trends` to see what's moving in the niche
2. Pick a topic from `memory/topic-map.md` (or a fresh idea)
3. Run `/draft-post [topic]` to create the full post
4. Publish — put external links in the first comment, not the body
5. 48 hours later: run `/log-memory` to record performance
6. Every Monday: run `/weekly-review` (or set `/loop 1w /weekly-review`)
