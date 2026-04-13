# Claude API Skill — LinkedIn Posts Automation

## Purpose

Use the Claude API (Anthropic SDK) to automate high-volume or repetitive tasks in the LinkedIn content workflow: batch hook generation, post drafting from a backlog, topic research summarization, and supermemory analysis.

This skill is powered by the **claude-api** built-in skill. It applies whenever you want to programmatically generate, analyze, or process content at scale rather than doing it interactively one post at a time.

---

## Architecture: Few-Shot Generation

The core generation pattern is adapted from the [Saurav0129/Linkedin-Post-Generator](https://github.com/Saurav0129/Linkedin-Post-Generator) approach:

**Original approach:** Feed 2 example posts from third-party influencers (Ankur Warikoo, Kunal Shah, Justin Welsh) as few-shot context before generating.

**Our adaptation:** Feed 2 of Luis Durruty's own best-performing posts as examples — same mechanism, but using Celsux's actual voice and style as the signal instead of someone else's.

```
data/raw_posts.json          ← Luis's published posts (manually collected)
        ↓
scripts/preprocess_posts.py  ← LLM extracts tags, format, hook_pattern, line_count
        ↓
data/preprocessed.json       ← Enriched dataset with performance tiers (A/B/C)
        ↓
scripts/few_shots.py         ← FewShotPosts: filter by pillar × length × language × tier
        ↓
scripts/post_generator.py    ← Build prompt with 2 A-tier examples → Claude Opus 4.6
        ↓
New post                     ← Grounded in what has actually worked before
```

This creates a **self-improving loop**: every new post that performs well gets added to `raw_posts.json`, preprocessed, and becomes available as a future few-shot example.

---

## When to Use the Claude API

| Use Case | Interactive (chat) | Claude API (scripts/) |
|---|---|---|
| Drafting 1 post | ✅ Use `/draft-post` | — |
| Drafting a week's worth of posts at once | — | ✅ `batch_draft()` |
| Generating 5 hooks for 1 topic | ✅ Use `/generate-hooks` | — |
| Generating hooks for 20 topics from backlog | — | ✅ Batch mode |
| Running weekly review | ✅ Use `/weekly-review` | — |
| Analyzing 3 months of post data for patterns | — | ✅ Analysis mode |
| Preprocessing new raw posts | — | ✅ `preprocess_posts.py` |
| Inspecting few-shot dataset stats | — | ✅ `few_shots.py` |
| Real-time trend research | ✅ Chat | — |
| Summarizing a competitor's last 30 posts | — | ✅ Summarization |

---

## Setup

```bash
pip install anthropic
```

Requires: `ANTHROPIC_API_KEY` environment variable set.

**Always use prompt caching** (`cache_control`) on system prompts and large context documents to reduce cost and latency. This matters here because the system prompt (voice guide + best practices) is large and reused across every post generation call.

---

## Core Pattern: Post Drafting with Full Context

```python
import anthropic

client = anthropic.Anthropic()

# Load skill files as context (cached)
with open("celsux-voice.md") as f:
    voice_guide = f.read()

with open("best-practices.md") as f:
    best_practices = f.read()

with open("content-research-writer.md") as f:
    writer_workflow = f.read()

def draft_post(topic: str, pillar: str, hook_pattern: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": f"""You are a LinkedIn content writer for Luis Durruty, CEO of Celsux.
                
Follow these documents exactly:

## Voice Guide
{voice_guide}

## Best Practices  
{best_practices}

## Writing Workflow
{writer_workflow}""",
                "cache_control": {"type": "ephemeral"}  # Cache the large system prompt
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"""Draft a LinkedIn post.

Topic: {topic}
Pillar: {pillar}
Hook pattern: {hook_pattern}

Follow the full 6-phase workflow. Output only the final post, ready to publish."""
            }
        ]
    )
    return response.content[0].text


# Example usage
post = draft_post(
    topic="Por qué el 80% de los team buildings no cambian la cultura",
    pillar="Cultura que transforma",
    hook_pattern="Bold claim"
)
print(post)
```

---

## Pattern: Batch Hook Generation from Backlog

```python
import anthropic
import json

client = anthropic.Anthropic()

# Load topic backlog
topics = [
    "Diferencia entre evento y experiencia corporativa",
    "Cómo justificar el presupuesto de cultura ante el CEO",
    "El error más común en team buildings",
    # ... add from memory/topic-map.md
]

with open("celsux-voice.md") as f:
    voice_guide = f.read()

def generate_hooks_batch(topics: list[str]) -> dict:
    results = {}
    
    for topic in topics:
        response = client.messages.create(
            model="claude-sonnet-4-6",  # Use Sonnet for batch tasks (faster/cheaper)
            max_tokens=512,
            system=[
                {
                    "type": "text",
                    "text": f"You write LinkedIn hooks for Luis Durruty (Celsux). Voice guide:\n{voice_guide}",
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": f"Generate 3 hook variations for this topic: {topic}\n\nFormat: numbered list, one line each."
                }
            ]
        )
        results[topic] = response.content[0].text
    
    return results

hooks = generate_hooks_batch(topics)
for topic, hook_options in hooks.items():
    print(f"\n## {topic}\n{hook_options}")
```

---

## Pattern: Supermemory Analysis

Analyze 90 days of post memory entries to surface patterns.

```python
import anthropic
import os
from pathlib import Path

client = anthropic.Anthropic()

# Load all memory entries
memory_dir = Path("memory/posts")
entries = []
for f in sorted(memory_dir.glob("*.md")):
    entries.append(f.read_text())

all_memory = "\n\n---\n\n".join(entries)

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": "You are a LinkedIn content strategist analyzing performance data for Luis Durruty / Celsux.",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Here are all post memory entries from the last 90 days:",
                    "cache_control": {"type": "ephemeral"}  # Cache the large memory blob
                },
                {
                    "type": "text",
                    "text": all_memory
                },
                {
                    "type": "text",
                    "text": """Analyze and report:
1. Top 3 hook patterns by average engagement rate
2. Top 3 topics by average engagement rate  
3. Best performing post format
4. Best performing content pillar
5. Optimal post length (word count range of A-tier posts)
6. 3 strategic recommendations for the next 30 days"""
                }
            ]
        }
    ]
)

print(response.content[0].text)
```

---

## Model Selection Guide

| Task | Recommended Model | Reason |
|---|---|---|
| Full post drafting | `claude-opus-4-6` | Highest quality voice + nuance |
| Hook generation | `claude-sonnet-4-6` | Fast, cost-effective, sufficient quality |
| Batch processing | `claude-sonnet-4-6` | Speed + cost at scale |
| Memory analysis | `claude-opus-4-6` | Complex reasoning over data |
| Research summarization | `claude-sonnet-4-6` | Good summaries at lower cost |

---

## Prompt Caching Rules

Always cache:
- The voice guide (`celsux-voice.md`) — large, reused in every call
- The best practices doc — large, reused in every call
- The writing workflow — large, reused in post drafting calls
- The memory blob — large, when running analysis across many entries

Never cache:
- The specific topic/task input — it changes every call
- The final user question — always fresh

**Why it matters:** The combined skill files are ~15,000 tokens. Without caching, every post draft call costs the full input. With caching, you pay the cache write cost once and cache read cost (5x cheaper) on every subsequent call in the session.

---

## File Structure for API Scripts

```
/scripts
  draft_post.py          # Single post drafting
  batch_hooks.py         # Batch hook generation from topic backlog
  analyze_memory.py      # 90-day performance analysis
  research_summary.py    # Summarize research briefs into post briefs
  requirements.txt       # anthropic>=0.40.0
```
