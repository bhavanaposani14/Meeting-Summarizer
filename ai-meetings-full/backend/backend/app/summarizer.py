from openai import AsyncOpenAI
from .settings import get_settings

settings = get_settings()
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

_PROMPT = """You are an expert meeting assistant.
Given the raw transcript below, produce:
1. A concise paragraph summary (<150 words).
2. A bulleted list of ACTION ITEMS in the format "- [ ] owner · description · due‑date".
3. A numbered DECISION LOG where each item is <=25 words.

TRANSCRIPT:
\"\"\"{t}\"\"\"
"""

async def summarize(transcript: str) -> tuple[str, list[dict], list[str]]:
    msg = _PROMPT.format(t=transcript[:15000])   # stay under context window
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": msg}],
        temperature=0.2,
    )
    text = response.choices[0].message.content.strip()

    # very light heuristic parsing ↓
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    summary = lines[0]
    a_items, decisions = [], []
    mode = None
    for ln in lines[1:]:
        if ln.lower().startswith("action"):
            mode = "a"
            continue
        if ln.lower().startswith("decision"):
            mode = "d"
            continue
        if mode == "a" and ln.startswith("-"):
            box, rest = ln[1:].split("]", 1)
            owner, desc, *due = rest.strip().split("·")
            a_items.append(
                {"owner": owner.strip(), "description": desc.strip(), "due_date": (due[0].strip() if due else None)}
            )
        elif mode == "d":
            decisions.append(ln.lstrip("0123456789. ").strip())
    return summary, a_items, decisions
