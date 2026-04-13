"""
post_generator.py
-----------------
Adapted from github.com/Saurav0129/Linkedin-Post-Generator (post_generator.py)

Generates LinkedIn posts for Luis Durruty / Celsux using:
1. Few-shot examples from Luis's own best-performing posts (via FewShotPosts)
2. Claude API with prompt caching on voice guide and best practices
3. Length, language, pillar, format, and hook pattern controls

Key adaptations vs. the original:
- Uses Claude (anthropic SDK) instead of ChatGroq
- Voice guide + best practices injected as cached system context
- Examples sourced from Luis's own A-tier posts (not third-party influencers)
- Added: hook_pattern and format parameters for tighter control
- Added: batch_draft() for generating a week's worth of posts at once

Usage:
    python scripts/post_generator.py
    → Generates a sample post and prints it.
"""

import os
import anthropic
from few_shots import FewShotPosts

# ---------------------------------------------------------------------------
# Load skill files as cached context (loaded once per process)
# ---------------------------------------------------------------------------

def _load_skill(filename: str) -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, filename)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return ""

VOICE_GUIDE = _load_skill("celsux-voice.md")
BEST_PRACTICES = _load_skill("best-practices.md")
WRITER_WORKFLOW = _load_skill("content-research-writer.md")

# ---------------------------------------------------------------------------
# Client + few-shot loader
# ---------------------------------------------------------------------------

client = anthropic.Anthropic()
few_shot = FewShotPosts()


# ---------------------------------------------------------------------------
# Length → line count range (same mapping as original repo)
# ---------------------------------------------------------------------------

def get_length_str(length: str) -> str:
    mapping = {
        "Short": "1 to 5 lines",
        "Medium": "6 to 10 lines",
        "Long": "11 to 15 lines",
    }
    return mapping.get(length, "6 to 10 lines")


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def build_prompt(
    tag: str,
    length: str,
    language: str,
    format_type: str,
    hook_pattern: str,
    examples: list[dict],
) -> str:
    """
    Constructs the user-turn prompt with few-shot examples embedded.
    Mirrors the structure from the original post_generator.py get_prompt(),
    extended with Celsux-specific parameters.
    """
    length_str = get_length_str(length)

    prompt = f"""Generate a LinkedIn post for Luis Durruty (CEO Celsux). No preamble. Output only the post.

Parameters:
1. Topic/Pillar: {tag}
2. Length: {length_str}
3. Language: {language}
4. Format: {format_type}
5. Hook pattern: {hook_pattern}

Language note:
- "Spanish" → write entirely in Spanish
- "English" → write entirely in English
- "Spanglish" → mix Spanish and English naturally, always use Latin script"""

    # Inject up to 2 high-performing examples (same limit as original repo)
    if examples:
        prompt += "\n\n6) Write in the style of these real posts by Luis Durruty that performed well:\n"
        for i, post in enumerate(examples[:2]):
            tier = post.get("performance_tier", "")
            eng = post.get("engagement", "")
            prompt += f"\nExample {i+1} (Tier {tier}, {eng} engagements):\n\n{post['text']}"

    return prompt


# ---------------------------------------------------------------------------
# Core generation function
# ---------------------------------------------------------------------------

def generate_post(
    tag: str,
    length: str = "Medium",
    language: str = "Spanish",
    format_type: str = "hot-take",
    hook_pattern: str = "Bold claim",
    min_example_tier: str = "A",
) -> str:
    """
    Generate a single LinkedIn post.

    Args:
        tag          : Celsux content pillar or topic
        length       : "Short" | "Medium" | "Long"
        language     : "Spanish" | "English" | "Spanglish"
        format_type  : "story" | "list" | "framework" | "hot-take" | "curation" | "question"
        hook_pattern : one of the 10 hook patterns from the hook library
        min_example_tier : minimum performance tier for few-shot examples ("A" | "B")

    Returns:
        str: The generated post text, ready to copy into LinkedIn.
    """
    # Select few-shot examples from Luis's own posts
    examples = few_shot.get_best_examples(
        length=length,
        language=language,
        tag=tag,
        max_examples=2,
        min_tier=min_example_tier,
    )

    prompt = build_prompt(tag, length, language, format_type, hook_pattern, examples)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": f"""You are the LinkedIn ghostwriter for Luis Durruty, CEO of Celsux.
Celsux is an All-in-One Agency with 23+ years and 3,000+ corporate events in LATAM.
Target audience: RRHH directors, People & Culture leads, CHROs.

Always follow these documents:

## Voice Guide
{VOICE_GUIDE}

## Best Practices
{BEST_PRACTICES}""",
                "cache_control": {"type": "ephemeral"},  # Cache on first call, read cheaply after
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


# ---------------------------------------------------------------------------
# Batch draft — generate a full week of posts from a content plan
# ---------------------------------------------------------------------------

def batch_draft(content_plan: list[dict]) -> list[dict]:
    """
    Generate multiple posts from a content plan list.

    Each item in content_plan should be a dict with keys matching
    generate_post() parameters. Returns the same list with a "draft" key added.

    Example content_plan entry:
    {
        "tag": "Cultura que transforma",
        "length": "Medium",
        "language": "Spanish",
        "format_type": "hot-take",
        "hook_pattern": "Bold claim"
    }
    """
    results = []
    for i, item in enumerate(content_plan):
        print(f"[{i+1}/{len(content_plan)}] Drafting: {item.get('tag')} / {item.get('format_type')}...")
        draft = generate_post(
            tag=item.get("tag", "Cultura que transforma"),
            length=item.get("length", "Medium"),
            language=item.get("language", "Spanish"),
            format_type=item.get("format_type", "hot-take"),
            hook_pattern=item.get("hook_pattern", "Bold claim"),
        )
        results.append({**item, "draft": draft})
    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Generating sample post ===\n")

    post = generate_post(
        tag="Cultura que transforma",
        length="Medium",
        language="Spanish",
        format_type="hot-take",
        hook_pattern="Bold claim",
    )

    print(post)
    print("\n" + "=" * 60)

    # Show few-shot stats if data is available
    if not few_shot.df.empty:
        print("\n=== Few-shot dataset stats ===")
        fmt_stats = few_shot.get_format_stats()
        if fmt_stats:
            print("Format performance:")
            for fmt, s in sorted(fmt_stats.items(), key=lambda x: -x[1].get("avg_engagement", 0)):
                print(f"  {fmt}: avg={s['avg_engagement']:.0f}, posts={s['posts']}")
    else:
        print("\nNote: No preprocessed posts yet. Add Luis's posts to data/raw_posts.json")
        print("and run: python scripts/preprocess_posts.py")
