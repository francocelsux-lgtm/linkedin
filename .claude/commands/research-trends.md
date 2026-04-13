# /research-trends

Run a deep research pass on a topic, competitor, or the RRHH/cultura space. Uses the full `deep-research-skill.md` protocol.

## Usage

```
/research-trends [topic or competitor name]
```

**Examples:**
- `/research-trends cultura organizacional tendencias 2026`
- `/research-trends competidor: Top Employers Institute`
- `/research-trends qué está funcionando en LinkedIn RRHH esta semana`
- `/research-trends` *(no argument = full weekly trend scan)*

---

## What this command does

### If a topic is given → Topic Deep Dive

1. **Core claim research** — find 3+ sources, pull the most surprising data point
2. **Competitor coverage check** — has this angle been published recently in the niche?
3. **Audience question mining** — what are RRHH professionals asking about this topic?
4. **Counterargument** — steelman the opposing view
5. **Hook angle** — which hook pattern from the library fits best?

Output: A filled-out Research Brief ready to pass to `/draft-post`.

---

### If a competitor is given → Competitor Audit

Analyze the competitor using the Layer 2 protocol from `deep-research-skill.md`:

```
Competitor:
Follower count / growth:
Post frequency:
Top 3 performing formats:
Recurring hooks/patterns used:
Topics with highest engagement:
Topics they are NOT covering (gaps):
Comment quality:
Key takeaway for Celsux strategy:
```

---

### If no argument → Weekly Trend Scan

Scan the RRHH / cultura / eventos corporativos space for:

1. **Rising topics** — what's gaining traction in the last 7 days?
2. **Viral hooks** — what first lines are stopping scrolls in the niche right now?
3. **Gaps** — what questions are being asked that nobody's answering well?
4. **Trend timing** — which topics are 3 days early (ideal) vs. already peaked?

Output: A prioritized list of 5 content opportunities with suggested hook patterns for each.

---

## Output Format

Always end with:
- **Top 3 content opportunities** ranked by urgency + differentiation potential
- **Suggested pillar** for each (from profile-analysis.md content pillars)
- **Suggested format** for each (story, list, framework, hot take, curation)
- **Status**: Add findings to `memory/competitor-log.md` or `memory/topic-map.md`
