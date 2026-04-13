# /generate-hooks

Generate 5 high-quality hook variations for a LinkedIn post topic, scored and ranked. Uses the hook pattern library and Celsux voice.

## Usage

```
/generate-hooks [topic or core claim]
```

**Examples:**
- `/generate-hooks por qué los eventos corporativos no cambian la cultura`
- `/generate-hooks 23 años organizando eventos: las 3 cosas que siempre fallan`
- `/generate-hooks cómo los equipos de RRHH pueden convertirse en socios estratégicos`

---

## What this command does

1. Identify the **core tension** in the topic — the thing that would make someone stop scrolling
2. Generate **5 hooks** using different patterns from the hook library
3. **Score each hook** on 5 criteria
4. **Rank and recommend** the top hook, with rationale
5. Flag any hook that risks being a **bait-and-switch** (hook doesn't match body)

---

## Hook Patterns to Draw From

| Pattern | Example (adapted to Celsux) |
|---|---|
| Bold claim | "Los team buildings no funcionan. Y hay datos que lo prueban." |
| Surprising number | "Organizamos +3.000 eventos. El 80% de los clientes cometían el mismo error." |
| Mistake/failure | "El evento más costoso que hice casi destruye la cultura de una empresa." |
| Contrarian | "Todos dicen que el team building une equipos. Yo vi lo contrario." |
| Curiosity gap | "Hay una diferencia entre un evento corporativo y una experiencia. Muy poca gente la conoce." |
| Personal story | "En mi primer evento fallé en algo tan básico que hoy no puedo creer." |
| Social proof | "Cómo diseñamos una experiencia que transformó la cultura de una empresa de 800 personas." |
| Direct challenge | "Equipo de RRHH: estás organizando eventos cuando deberías estar diseñando experiencias." |
| List promise | "3 señales de que tu próximo evento corporativo va a ser un fracaso." |
| Question | "¿Qué pasaría si el problema de cultura de tu empresa no se resuelve con talleres?" |

---

## Scoring Rubric (1-5 per criterion)

| Criterion | Question |
|---|---|
| **Specificity** | Does it name a number, person, result, or situation? |
| **Tension** | Does it create a gap the reader urgently wants to close? |
| **Relevance** | Would an RRHH director or People lead stop for this? |
| **Originality** | Is this angle different from what's already in the feed? |
| **Voice match** | Does it sound like Luis Durruty / Celsux — direct, experienced, human? |

---

## Output Format

```
HOOK 1 — [pattern name]
[hook text]
Score: Specificity X | Tension X | Relevance X | Originality X | Voice X | Total: X/25
Note: [one line on what works or what to watch for]

HOOK 2 — [pattern name]
...

[repeat for all 5]

---
RECOMMENDED: Hook [N]
Why: [2-3 sentences on why this is the strongest choice]
Body format that fits best: [story | list | framework | hot take]
```
