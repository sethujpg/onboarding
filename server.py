"""NeoCognition Onboarding Agent — FastAPI backend.

Serves a single-page chat UI and a streaming /chat endpoint that calls
Claude Sonnet 4.6 with the onboarding knowledge base loaded as a cached
system prompt (Anthropic prompt caching → ~10x cheaper from turn 2 on).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

load_dotenv()

ROOT = Path(__file__).parent
KNOWLEDGE_FILES = [
    "onboarding_notes.md",
    "modal_setup_guide.md",
    "gcp_setup_guide.md",
]

# Routing: prefer Portkey (company gateway) if a key is present, else direct Anthropic.
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
if PORTKEY_API_KEY:
    MODEL = os.getenv("MODEL", "@anthropic-default/claude-sonnet-4-6")
    ROUTE = "portkey"
else:
    MODEL = os.getenv("MODEL", "claude-sonnet-4-6")
    ROUTE = "anthropic"


def load_knowledge_base() -> str:
    parts: list[str] = []
    for fn in KNOWLEDGE_FILES:
        path = ROOT / fn
        if not path.exists():
            continue
        parts.append(f"## Source file: `{fn}`\n\n{path.read_text()}")
    return "\n\n---\n\n".join(parts)


SYSTEM_PREAMBLE = """You are the NeoCognition onboarding assistant — a chatbot built to help new interns and hires get through their first days at NeoCognition.

Your job is to answer questions accurately and directly using ONLY the onboarding documents provided below.

# How to respond

- Be concise and friendly. New hires are often overwhelmed; don't pile on.
- Use bullets or numbered steps for procedures. Don't dump whole doc sections verbatim — extract the relevant part.
- When the docs name a specific human (by name or Slack handle), name them when relevant.
- Render Slack handles with the `@` prefix exactly as the docs do.
- It's fine to mention which file an answer came from if it would help the user explore further.

# Critical rules

1. **Never make up information.** If something is not in the documents, say so plainly.
2. **Never guess names, contacts, codes, URLs, dollar amounts, or deadlines.** These must come from the docs verbatim.
3. **When you don't know, route the user to a human.** Use this map:
   - Benefits, WeBox / meals, reimbursements, desk equipment, weekend meal vouchers → **@Surbhi Agarwal** in the **#help** Slack channel.
   - Login or account problems for any company tool → **@Yao Yang** or **@Xiang Deng**.
   - Slack channel invites, Notion page links, Modal access, GitHub repo access, team-specific questions → **your mentor**.
   - I-9 verification, Rippling, payroll, tax forms, bank info, benefits enrollment → **HR**.
   - Office-building things (gym code, post-5pm door code, mail, parking, food schedule) → **the Industrious main desk** in person, or email **pagemill@industriousoffice.com**.
   - Anything else not in the docs → ask your mentor first, then HR.
4. **Don't speculate on policy.** If asked "can I do X" and X isn't covered, say: "I don't see that in my materials — best to check with [the right human]."
5. **Stay on topic.** If asked something unrelated to onboarding (general coding help, world questions, opinions), politely redirect to the #help Slack channel.
6. **Use the right email for the right tool.** Remind users that Cursor and Claude Code must be signed up with the `@neocognition.io` company email (the company sponsors those plans), but the initial **guest** Industrious WiFi sign-in must use a **personal** email to avoid clashing with their future Industrious member account.

# Important details from the docs (don't paraphrase these wrong)

- **WeBox lunch order cutoff is 7:30 AM** the day-of (or schedule ahead). Dinner cutoff is 2 PM.
- The **office building door** has two locks: the **main entrance** opens via Bluetooth in the Industrious app OR PIN; the **inner office space door** requires PIN only.
- **Suite / office number** at 1881 Page Mill Road is **136**.
- **Industrious WiFi** has two stages: Stage 1 (Day 1 guest access — **personal email**), Stage 2 (member access — accept the IsoFy invite with company email).

The full onboarding knowledge base follows. Use it as your only source of truth."""


def build_system() -> list[dict]:
    return [
        {"type": "text", "text": SYSTEM_PREAMBLE},
        {
            "type": "text",
            "text": f"# Onboarding knowledge base\n\n{load_knowledge_base()}",
            "cache_control": {"type": "ephemeral"},
        },
    ]


if ROUTE == "portkey":
    client = AsyncAnthropic(
        api_key="dummy",  # auth flows through the x-portkey-api-key header
        base_url="https://api.portkey.ai",
        default_headers={"x-portkey-api-key": PORTKEY_API_KEY},
    )
else:
    client = AsyncAnthropic()  # reads ANTHROPIC_API_KEY from env

SYSTEM = build_system()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


class FeedbackRequest(BaseModel):
    rating: str  # "up" or "down"
    question: str
    answer: str
    comment: str | None = None


FEEDBACK_FILE = ROOT / "feedback.jsonl"


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse((ROOT / "index.html").read_text())


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "route": ROUTE,
        "model": MODEL,
        "kb_files_loaded": [f for f in KNOWLEDGE_FILES if (ROOT / f).exists()],
    }


@app.post("/chat")
async def chat(req: ChatRequest):
    api_messages = [{"role": m.role, "content": m.content} for m in req.messages]

    async def event_stream():
        def sse(obj: dict) -> str:
            return f"data: {json.dumps(obj)}\n\n"

        try:
            async with client.messages.stream(
                model=MODEL,
                max_tokens=2048,
                system=SYSTEM,
                messages=api_messages,
                thinking={"type": "disabled"},
                output_config={"effort": "low"},
            ) as stream:
                async for text in stream.text_stream:
                    yield sse({"text": text})
                final = await stream.get_final_message()
                yield sse({
                    "done": True,
                    "usage": {
                        "input": final.usage.input_tokens,
                        "output": final.usage.output_tokens,
                        "cache_read": final.usage.cache_read_input_tokens,
                        "cache_creation": final.usage.cache_creation_input_tokens,
                    },
                })
        except Exception as e:
            yield sse({"error": f"{type(e).__name__}: {e}"})

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/feedback")
async def feedback(req: FeedbackRequest) -> dict:
    if req.rating not in ("up", "down"):
        return {"ok": False, "error": "rating must be 'up' or 'down'"}
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rating": req.rating,
        "comment": req.comment,
        "question": req.question,
        "answer": req.answer,
    }
    with FEEDBACK_FILE.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
