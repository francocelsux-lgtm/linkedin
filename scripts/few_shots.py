"""
few_shots.py
------------
Adapted from github.com/Saurav0129/Linkedin-Post-Generator (Few_shots.py)

Loads Luis Durruty's preprocessed posts and provides filtered access for
few-shot example selection when generating new LinkedIn content.

Key adaptations vs. the original:
- "influencer" axis replaced by "performance_tier" (A/B/C) — we only want
  Luis's own posts, so we filter by quality, not by person
- Tags mapped to Celsux content pillars
- Languages: "Spanish", "English", "Spanglish"
- Added get_best_examples() — primary method used by post_generator.py
"""

import json
import os
import pandas as pd


class FewShotPosts:
    def __init__(self, file_path: str = os.path.join("data", "preprocessed.json")):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_posts(self, file_path: str) -> None:
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)

        if not posts:
            self.df = pd.DataFrame()
            self.unique_tags = []
            return

        self.df = pd.json_normalize(posts)

        # Derive length category from line_count (same thresholds as original)
        if "line_count" in self.df.columns:
            self.df["length"] = self.df["line_count"].apply(self._categorize_length)

        # Collect unique tags globally
        if "tags" in self.df.columns:
            all_tags = self.df["tags"].apply(lambda x: x if isinstance(x, list) else []).sum()
            self.unique_tags = list(set(all_tags))
        else:
            self.unique_tags = []

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _categorize_length(line_count: int) -> str:
        if line_count < 5:
            return "Short"
        elif line_count <= 10:
            return "Medium"
        return "Long"

    # ------------------------------------------------------------------
    # Core example selector — used by post_generator.py
    # ------------------------------------------------------------------

    def get_best_examples(
        self,
        length: str,
        language: str,
        tag: str,
        max_examples: int = 2,
        min_tier: str = "A",
    ) -> list[dict]:
        """
        Primary method for few-shot selection.

        Returns up to `max_examples` posts that match:
        - length (Short / Medium / Long)
        - language (Spanish / English / Spanglish)
        - tag (one of Celsux pillars)
        - performance tier >= min_tier (A > B > C)

        Falls back progressively if exact matches are scarce:
        1. Exact match: length + language + tag + tier A
        2. Relax tier to B
        3. Relax length constraint
        4. Relax tag constraint (same pillar family not strictly matched)
        """
        tier_order = {"A": 2, "B": 1, "C": 0}
        min_tier_val = tier_order.get(min_tier, 1)

        if self.df is None or self.df.empty:
            return []

        def tier_ok(t):
            return tier_order.get(t, 0) >= min_tier_val

        # Attempt 1: full match
        results = self._filter(length, language, tag, tier_filter=tier_ok)
        if len(results) >= max_examples:
            return results[:max_examples]

        # Attempt 2: relax tier
        results = self._filter(length, language, tag, tier_filter=lambda t: True)
        if len(results) >= max_examples:
            return results[:max_examples]

        # Attempt 3: relax length
        results = self._filter(None, language, tag, tier_filter=lambda t: True)
        if len(results) >= max_examples:
            return results[:max_examples]

        # Attempt 4: relax tag (return any high-tier post)
        results = self._filter(None, language, None, tier_filter=tier_ok)
        return results[:max_examples]

    def _filter(self, length, language, tag, tier_filter=None) -> list[dict]:
        df = self.df.copy()

        if length and "length" in df.columns:
            df = df[df["length"] == length]

        if language and "language" in df.columns:
            df = df[df["language"] == language]

        if tag and "tags" in df.columns:
            df = df[df["tags"].apply(lambda tags: isinstance(tags, list) and tag in tags)]

        if tier_filter and "performance_tier" in df.columns:
            df = df[df["performance_tier"].apply(tier_filter)]

        # Sort by engagement descending so best examples come first
        if "engagement" in df.columns:
            df = df.sort_values("engagement", ascending=False)

        return df.to_dict(orient="records")

    # ------------------------------------------------------------------
    # Analytics helpers
    # ------------------------------------------------------------------

    def get_filtered_posts(self, length: str, language: str, tag: str) -> list[dict]:
        """Original-style filter. Kept for compatibility."""
        return self._filter(length, language, tag)

    def get_top_posts(self, top_n: int = 5, min_engagement: int = 0) -> list[dict]:
        if self.df is None or self.df.empty:
            return []
        df = self.df[self.df.get("engagement", pd.Series(dtype=int)) >= min_engagement]
        return df.nlargest(top_n, "engagement").to_dict(orient="records")

    def get_posts_by_tier(self, tier: str = "A") -> list[dict]:
        if self.df is None or "performance_tier" not in self.df.columns:
            return []
        return self.df[self.df["performance_tier"] == tier].to_dict(orient="records")

    def get_posts_by_pillar(self, pillar: str) -> list[dict]:
        if self.df is None or "tags" not in self.df.columns:
            return []
        return self.df[
            self.df["tags"].apply(lambda t: isinstance(t, list) and pillar in t)
        ].to_dict(orient="records")

    def get_tags(self) -> list[str]:
        return self.unique_tags

    def get_tag_stats(self) -> dict:
        """Return engagement stats per tag/pillar."""
        if self.df is None or self.df.empty:
            return {}
        stats = {}
        for tag in self.unique_tags:
            posts = self.get_posts_by_pillar(tag)
            if posts:
                engagements = [p.get("engagement", 0) for p in posts]
                stats[tag] = {
                    "count": len(posts),
                    "avg_engagement": sum(engagements) / len(engagements),
                    "max_engagement": max(engagements),
                    "a_tier_count": sum(1 for p in posts if p.get("performance_tier") == "A"),
                }
        return stats

    def get_format_stats(self) -> dict:
        """Return engagement stats per post format."""
        if self.df is None or "format" not in self.df.columns:
            return {}
        return (
            self.df.groupby("format")["engagement"]
            .agg(["count", "mean", "max"])
            .rename(columns={"count": "posts", "mean": "avg_engagement", "max": "max_engagement"})
            .to_dict(orient="index")
        )

    def get_hook_stats(self) -> dict:
        """Return engagement stats per hook pattern."""
        if self.df is None or "hook_pattern" not in self.df.columns:
            return {}
        return (
            self.df.groupby("hook_pattern")["engagement"]
            .agg(["count", "mean", "max"])
            .rename(columns={"count": "posts", "mean": "avg_engagement", "max": "max_engagement"})
            .to_dict(orient="index")
        )


if __name__ == "__main__":
    fs = FewShotPosts()

    if not fs.df.empty:
        print("=== Tag stats ===")
        for tag, stats in fs.get_tag_stats().items():
            print(f"  {tag}: {stats}")

        print("\n=== Format stats ===")
        for fmt, stats in fs.get_format_stats().items():
            print(f"  {fmt}: {stats}")

        print("\n=== Hook pattern stats ===")
        for hook, stats in fs.get_hook_stats().items():
            print(f"  {hook}: {stats}")

        print("\n=== Top 3 posts ===")
        for p in fs.get_top_posts(top_n=3):
            print(f"  [{p.get('performance_tier')}] {p.get('engagement')} — {p['text'][:80]}...")
    else:
        print("No preprocessed data yet. Run preprocess_posts.py first.")
