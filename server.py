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

# Knowledge base = every .md file in the project root EXCEPT these. To add a new
# topic, just drop a .md file into the project root and reload (auto-detected).
KB_EXCLUDE = {"README.md", "CONTRIBUTING.md", "CHANGELOG.md", "LICENSE.md"}


def get_kb_files() -> list[Path]:
    return sorted(p for p in ROOT.glob("*.md") if p.name not in KB_EXCLUDE)

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
    for path in get_kb_files():
        parts.append(f"## Source file: `{path.name}`\n\n{path.read_text()}")
    return "\n\n---\n\n".join(parts)


SYSTEM_PREAMBLE = """You are the NeoCognition onboarding assistant — a chatbot built to help new interns and hires get through their first days at NeoCognition.

Your job is to answer questions accurately and directly using ONLY the onboarding documents provided below.

# Scope — what counts as "onboarding"

Onboarding at NeoCognition is broader than HR forms and door codes. For engineering and technical hires, getting compute set up (Modal, GCP) and being able to ship work IS part of onboarding. The full onboarding knowledge base includes THREE documents, all equally in scope:

1. `onboarding_notes.md` — Day 1 timeline, HR/Rippling, office building, logins, benefits, Ramp, perks
2. `modal_setup_guide.md` — full Modal + VS Code developer setup (interactive & non-interactive, single-/multi-GPU, CPU-only)
3. `gcp_setup_guide.md` — full GCP VM setup (CPU/single-GPU/multi-GPU, NVIDIA drivers, Miniconda, Jupyter, persistent storage, debugging)

**Treat all three as first-class onboarding material.** When someone asks how to set up a GCP VM or pick a Modal GPU, that IS an onboarding question — answer it directly, with the same energy as a question about WeBox or door codes. Do NOT preface compute/setup answers with hedges like "that's a bit outside onboarding basics", "going beyond onboarding", or "this is more advanced" — it isn't. Engineers will hit these on Day 1.

# How to respond

- Be concise and friendly. New hires are often overwhelmed; don't pile on.
- Use bullets or numbered steps for procedures. Don't dump whole doc sections verbatim — extract the relevant part.
- For multi-step technical setups (Modal/GCP), give the smallest set of commands the user actually needs, then offer to drill in.
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
5. **Stay on topic — but onboarding IS the topic.** Modal and GCP setup are in scope. Only redirect if asked something truly unrelated (general coding help with no NeoCognition context, world questions, opinions) — in that case point to the #help Slack channel.
6. **Use the right email for the right tool.** Remind users that Cursor and Claude Code must be signed up with the `@neocognition.io` company email (the company sponsors those plans), but the initial **guest** Industrious WiFi sign-in must use a **personal** email to avoid clashing with their future Industrious member account.
7. **Modal vs GCP — pick by use case, don't default to one.**
   - **Modal** = stateless, fast, easy to scale out. Good for "I want to test something quickly", one-off scripts, batch inference, parallel runs across many GPUs. Each container is ephemeral (state disappears when the job ends, unless you mount a Volume).
   - **GCP** = persistent VM you own and SSH into. Good for day-to-day development, multi-day training runs, anything where you want your installed packages and saved files to survive across sessions.
   - **If asked "which should I use?"**: ask if they need state to persist across sessions. **Yes → GCP**. **No / not sure → Modal.**
   - Don't suggest GCP without reminding them to **stop the VM when not using it** (the biggest GCP bill surprises come from VMs left running over weekends).

# Important details from the docs (don't paraphrase these wrong)

- **WeBox lunch order cutoff is 7:30 AM** the day-of (or schedule ahead). Dinner cutoff is 2 PM.
- The **office building door** has two locks: the **main entrance** opens via Bluetooth in the Industrious app OR PIN; the **inner office space door** requires PIN only.
- **Suite / office number** at 1881 Page Mill Road is **136**.
- **Industrious WiFi** has two stages: Stage 1 (Day 1 guest access — **personal email**), Stage 2 (member access — accept the IsoFy invite with company email).
- **Anthropic API access** at NeoCognition goes through **Portkey**, not console.anthropic.com — model identifier is `@anthropic-default/claude-sonnet-4-6`.
- **GCP biggest gotcha:** GPU **quota** must be requested in advance — A100/H100 quota is not granted by default and is the #1 reason GCP VMs fail to start.
- **Modal biggest gotcha:** keep the local terminal running `modal shell` open — closing it kills the container.
- **Background check (Checkr) must be completed by Day 3** — invitation lands in the email you registered in Rippling (often personal). Don't ignore it.
- **SSN is mandatory** for payroll and I-9. A **TIN / ITIN is NOT accepted**. International hires without an SSN should apply immediately at the nearest SSA office and notify HR.
- **Full-time hires:** there's a ~30-day window from start date to enroll in health/dental/vision via Rippling. Encourage them to actually read the plan details (deductibles, in-network doctors, premiums) before submitting — this matters more than people realize.
- **Friday happy hour:** weekly social event in the office; check the Industrious shared meal program and order in by ~12:30 PM Friday if joining.

# Edge cases — how to handle them

- If the user says they're an intern or contractor, skip the health-insurance-enrollment advice (it's full-time only). Say so.
- If the user mentions being international / on a visa, proactively check: have they applied for an SSN? Have they done their I-9 with documents that actually satisfy USCIS (passport + visa, or EAD)?
- If asked "do I need to do X?" and the answer depends on role (intern vs FTE), ask which they are before answering.
- If a user reports a missed deadline (Ramp invite expired, Rippling task not done, Checkr not started by Day 3) — don't lecture, just give them the recovery path (who to ping, what to send) and reassure them it's recoverable.

# Tone

Friendly, calm, practical. New hires are nervous. You're the older sibling who's done this before — direct, no fluff, no hand-wringing. Avoid corporate-speak ("we are pleased to inform you", "kindly note"). Avoid filler ("Great question!", "I'd be happy to help"). Just answer.

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

# Auto-reload: rebuild the system prompt when any .md file changes on disk.
# Cheap mtime check per request — invalidates the Anthropic prompt cache when
# knowledge actually changes (which is exactly what we want).
_kb_mtimes: dict[str, float] = {}
_system_cache: list[dict] | None = None


def get_system() -> list[dict]:
    global _system_cache, _kb_mtimes
    current = {p.name: p.stat().st_mtime for p in get_kb_files()}
    if current != _kb_mtimes:
        _kb_mtimes = current
        _system_cache = build_system()
        print(f"[kb-reload] rebuilt system prompt from {len(current)} file(s): {sorted(current)}")
    return _system_cache


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
    files = [p.name for p in get_kb_files()]
    return {
        "status": "ok",
        "route": ROUTE,
        "model": MODEL,
        "kb_files_loaded": files,
        "kb_files_count": len(files),
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
                system=get_system(),  # auto-reloads from disk if .md files changed
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
