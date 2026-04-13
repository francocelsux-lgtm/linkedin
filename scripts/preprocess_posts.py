"""
preprocess_posts.py
-------------------
Adapted from github.com/Saurav0129/Linkedin-Post-Generator (preprocess.py)

Takes raw_posts.json (Luis Durruty's published posts) and enriches each entry
with LLM-extracted metadata: line_count, language, tags mapped to Celsux pillars,
format type, hook pattern, and performance tier.

Outputs preprocessed.json — the dataset used by few_shots.py for example selection.

Usage:
    python scripts/preprocess_posts.py
"""

import json
import os
import anthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

# ---------------------------------------------------------------------------
# Celsux content taxonomy — used to constrain tag extraction
# ---------------------------------------------------------------------------

CELSUX_PILLARS = [
    "Cultura que transforma",
    "El arte del evento",
    "RRHH estratégico",
    "Liderazgo y equipos",
    "Historias de campo",
]

CELSUX_FORMATS = ["story", "list", "framework", "hot-take", "curation", "question"]

CELSUX_HOOK_PATTERNS = [
    "Bold claim",
    "Surprising number",
    "Mistake/failure",
    "Contrarian",
    "Curiosity gap",
    "Personal story",
    "Social proof",
    "Direct challenge",
    "List promise",
    "Question",
]

# ---------------------------------------------------------------------------
# Claude client (replaces Groq from the original repo)
# Uses prompt caching on the large taxonomy context.
# ---------------------------------------------------------------------------

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


def extract_metadata(post_text: str) -> dict:
    """
    Use Claude to extract structured metadata from a raw post.

    Returns a dict with:
        line_count  : int
        language    : "Spanish" | "English" | "Spanglish"
        tags        : list[str]  — 1-2 Celsux pillar tags
        format      : str        — one of CELSUX_FORMATS
        hook_pattern: str        — one of CELSUX_HOOK_PATTERNS
    """
    pillar_list = "\n".join(f"- {p}" for p in CELSUX_PILLARS)
    format_list = ", ".join(CELSUX_FORMATS)
    hook_list = "\n".join(f"- {h}" for h in CELSUX_HOOK_PATTERNS)

    prompt = f"""You are analyzing a LinkedIn post by Luis Durruty, CEO of Celsux (corporate events and culture transformation for RRHH teams in LATAM).

Extract structured metadata. Respond with ONLY a valid JSON object — no explanation, no preamble.

JSON keys required:
- "line_count": (integer) number of lines in the post
- "language": one of "Spanish", "English", or "Spanglish"
- "tags": array of 1-2 strings chosen ONLY from the pillar list below
- "format": one string chosen ONLY from the format list below
- "hook_pattern": one string chosen ONLY from the hook pattern list below

Pillar options:
{pillar_list}

Format options: {format_list}

Hook pattern options:
{hook_list}

Post:
{post_text}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # fast + cheap for batch metadata extraction
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": "You extract structured metadata from LinkedIn posts. Output only valid JSON.",
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise OutputParserException(f"Failed to parse metadata JSON: {e}\nRaw response: {raw}")


def get_unified_tags(posts_with_metadata: list[dict]) -> dict:
    """
    Normalise tags across all posts so that slight variations map to the
    canonical Celsux pillar names.

    Adapted from the original repo's get_unified_tags() but constrained to
    Celsux pillars so tags never drift from the taxonomy.
    """
    all_tags = set()
    for post in posts_with_metadata:
        all_tags.update(post.get("tags", []))

    tag_list = ", ".join(sorted(all_tags))
    pillar_list = "\n".join(f"- {p}" for p in CELSUX_PILLARS)

    prompt = f"""You are unifying LinkedIn post tags to a fixed taxonomy.

Map each tag to its closest Celsux pillar. Output ONLY a valid JSON object where
each key is an original tag and each value is the matching Celsux pillar.

Celsux pillars (use these exact strings as values):
{pillar_list}

Tags to unify: {tag_list}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise OutputParserException(f"Failed to parse tag unification JSON: {e}\nRaw: {raw}")


def assign_performance_tier(engagement: int, all_engagements: list[int]) -> str:
    """
    Assign A/B/C tier based on relative engagement percentile.
    A = top 20%, C = bottom 30%, B = everything else.
    """
    if not all_engagements:
        return "B"
    sorted_eng = sorted(all_engagements)
    p80 = sorted_eng[int(len(sorted_eng) * 0.8)]
    p30 = sorted_eng[int(len(sorted_eng) * 0.3)]
    if engagement >= p80:
        return "A"
    if engagement <= p30:
        return "C"
    return "B"


def process_posts(
    raw_data_path: str = os.path.join("data", "raw_posts.json"),
    preprocessed_path: str = os.path.join("data", "preprocessed.json"),
) -> None:
    """
    Main pipeline: load raw posts → extract metadata → unify tags →
    assign performance tiers → write preprocessed.json.
    """
    with open(raw_data_path, encoding="utf-8") as f:
        posts = json.load(f)

    if not posts:
        print("No posts found in raw_posts.json. Add Luis's posts and rerun.")
        return

    print(f"Processing {len(posts)} posts...")

    # Step 1 — extract metadata for each post
    enriched = []
    for i, post in enumerate(posts):
        print(f"  [{i+1}/{len(posts)}] Extracting metadata...")
        try:
            metadata = extract_metadata(post["text"])
            enriched.append({**post, **metadata})
        except Exception as e:
            print(f"  WARNING: skipped post {i+1} due to error: {e}")
            enriched.append(post)  # keep raw entry without metadata

    # Step 2 — unify tags to Celsux pillar taxonomy
    print("Unifying tags to Celsux pillars...")
    try:
        unified = get_unified_tags(enriched)
        for post in enriched:
            post["tags"] = list({unified.get(t, t) for t in post.get("tags", [])})
    except Exception as e:
        print(f"WARNING: tag unification failed ({e}). Keeping raw tags.")

    # Step 3 — assign performance tiers relative to the full dataset
    all_engagements = [p.get("engagement", 0) for p in enriched]
    for post in enriched:
        post["performance_tier"] = assign_performance_tier(
            post.get("engagement", 0), all_engagements
        )

    # Step 4 — write output
    with open(preprocessed_path, encoding="utf-8", mode="w") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print(f"Done. {len(enriched)} posts written to {preprocessed_path}")

    # Summary
    tiers = {"A": 0, "B": 0, "C": 0}
    for p in enriched:
        tiers[p.get("performance_tier", "B")] += 1
    print(f"Performance tiers — A: {tiers['A']}, B: {tiers['B']}, C: {tiers['C']}")


if __name__ == "__main__":
    process_posts()
