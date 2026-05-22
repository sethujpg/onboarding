# NeoCognition Onboarding Assistant

A chat agent that helps new interns and hires get through their first days at NeoCognition. Built on Claude Sonnet 4.6 with the onboarding knowledge base loaded as a cached system prompt and served through a polished web UI.

![architecture](https://img.shields.io/badge/stack-FastAPI%20%2B%20vanilla%20JS-blue)
![model](https://img.shields.io/badge/model-claude--sonnet--4--6-purple)
![gateway](https://img.shields.io/badge/gateway-Portkey-orange)

## Features

- 💬 Streaming chat answers grounded in three onboarding docs
- ⚡ Anthropic prompt caching (~10× cheaper after the first turn in a session)
- 📋 Interactive **onboarding checklist** with 50 items across 9 categories — saves progress locally, click ⚡ on any item to ask the assistant about it
- 💾 **Conversation history** persists in `localStorage` across reloads, with a sidebar like ChatGPT
- 🌓 **Dark mode** — auto-detects OS preference, manual toggle in the header
- 🎨 Syntax-highlighted code blocks (highlight.js), copy-to-clipboard on every assistant message
- 👍 👎 **Feedback loop** — saves ratings + optional comments to `feedback.jsonl` for weekly review
- 🔐 Routes through **Portkey** (the company's LLM gateway) by default; falls back to direct Anthropic API if you set `ANTHROPIC_API_KEY` instead

## Files

| File | Role |
|---|---|
| `onboarding_notes.md` | Main knowledge base — Day 1 timeline, Industrious building, logins, benefits, Slack/Notion/Ramp |
| `modal_setup_guide.md` | Modal + VS Code developer setup reference |
| `gcp_setup_guide.md` | GCP VM setup reference |
| `server.py` | FastAPI backend — `/chat` (SSE streaming) + `/feedback` + `/health` |
| `index.html` | Single-page chat UI |
| `requirements.txt` | Python deps (4 packages) |
| `.env.example` | Template for `PORTKEY_API_KEY` (or `ANTHROPIC_API_KEY`) |
| `feedback.jsonl` | (Generated at runtime) one feedback entry per line — not committed |

---

## Run it locally

### Prerequisites

- **Python 3.10+** (3.12 recommended)
- A **Portkey API key** from https://app.portkey.ai/api-keys (sign in with `@neocognition.io`) — see "Why Portkey?" below
- OR a **personal Anthropic key** from https://console.anthropic.com/settings/keys (will hit free-tier rate limits)

### 1. Get the code

```sh
git clone https://github.com/sethujpg/onboarding.git
cd onboarding
```

### 2. Set up the environment

Pick **one** of the two options.

**Option A — Conda (recommended if you already have conda):**

```sh
conda create -n onboarding python=3.12 -y
conda activate onboarding
pip install -r requirements.txt
```

**Option B — venv:**

```sh
python3 -m venv .venv
source .venv/bin/activate     # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your API key

```sh
cp .env.example .env
```

Then edit `.env` and paste your key:

```
PORTKEY_API_KEY=<your-portkey-key>
```

(Or `ANTHROPIC_API_KEY=...` if you're using a personal Anthropic key instead.)

### 4. Start the server

```sh
python server.py
```

You should see uvicorn start on port 8000.

### 5. Open the UI

Visit **http://localhost:8000** in your browser. Done.

Next time, just `conda activate onboarding && python server.py` (or `source .venv/bin/activate && python server.py`).

---

## Why Portkey?

NeoCognition uses **Portkey** as the company LLM gateway. Don't use a personal Anthropic console key for company tools:

| Path | What it actually does |
|---|---|
| `console.anthropic.com` + company email | Creates a *personal* Anthropic account. Billing = whatever card you put on it (or free-trial limits → 10K tokens/min). |
| `app.portkey.ai` + company email | Joins the NeoCognition Portkey workspace. Routes through the company's paid Claude Team plan. No rate-limit headaches. |

Email identifies you; **billing follows the workspace the key was issued under**, not the email. See [`onboarding_notes.md`](onboarding_notes.md) section "Anthropic API access: use Portkey, NOT console.anthropic.com" for the full explanation.

The server auto-detects: if `PORTKEY_API_KEY` is set, it routes through Portkey. Otherwise it falls back to `ANTHROPIC_API_KEY`. The Portkey model identifier is `@anthropic-default/claude-sonnet-4-6` (note the `@anthropic-default/` provider prefix from the company's Model Catalog).

---

## How it works

```
                ┌─────────────────────┐
                │  Browser (UI + JS)  │
                │  · localStorage     │
                │  · Streaming fetch  │
                └──────────┬──────────┘
                           │  POST /chat (SSE)
                           ▼
                ┌─────────────────────┐
                │   FastAPI server    │
                │   server.py         │
                └──────────┬──────────┘
                           │
              system prompt = 3 cached .md files
                           │
                           ▼
                ┌─────────────────────┐         ┌────────────────────┐
                │  Portkey gateway    │ ──────► │   Anthropic API    │
                │  api.portkey.ai     │         │   Claude Sonnet    │
                └─────────────────────┘         └────────────────────┘
```

- On startup, `server.py` reads all three `.md` files and builds a single cached system prompt with strict-but-helpful guardrails (the agent answers only from the docs and routes unknowns to the right human).
- From turn 2 onward in a session, the ~16K-token system prompt is served from Anthropic's prompt cache at ~10% of the price — verifiable via the green ⚡ badge under each assistant message.
- Feedback (`/feedback` endpoint) appends one JSON line per submission to `feedback.jsonl`. Review weekly with `cat feedback.jsonl | jq .`.

## Customize the knowledge base

The agent's knowledge comes from `.md` files in the project root. **You don't need to touch code to add, edit, or remove knowledge.**

### Add a new topic

Drop a new `.md` file into the project root. That's it. The server **auto-detects** any `*.md` file in the root (except `README.md`) and includes it on the next request — no restart needed.

```sh
echo "# Pets policy\n\nDogs are welcome on Fridays..." > pets.md
# Next /chat request automatically picks it up
```

### Edit an existing topic

Just edit the file. The server watches file mtimes and **rebuilds the system prompt automatically** on the next chat request. The Anthropic prompt cache invalidates and writes a fresh entry, so the change takes effect immediately.

### Remove a topic

Delete the file (or move it out of the project root). Auto-detected on the next request.

### Files that are NOT part of the KB

These are excluded by name: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE.md`. If you want a markdown file to NOT be served as knowledge, name it one of those (or edit `KB_EXCLUDE` in `server.py`).

### Verify it worked

```sh
curl http://localhost:8000/health
```

Returns the list of `.md` files currently loaded. If your new file shows up there, you're good.

## Customize the checklist

The 50-item onboarding checklist lives in `index.html`, inside the `CHECKLIST` constant near the top of the `<script>` block. Add, remove, or edit items there — each needs a unique stable `id` (so localStorage progress survives) and a `label`. Group by category.

## Deploying it for others

The app is one FastAPI process plus three static markdown files. Any of these work:

- **Render / Railway / Fly.io** — set `PORTKEY_API_KEY` as an environment variable, point the start command at `python server.py`, expose `$PORT`.
- **Docker** — base image `python:3.12-slim`, `pip install -r requirements.txt`, `CMD ["python", "server.py"]`.
- **Behind company SSO** — put it behind any auth proxy that forwards requests to localhost:8000.

If you deploy publicly, **add Google SSO restricted to `@neocognition.io`** first — otherwise you're hosting an open LLM endpoint that anyone on the internet can drain.

## Future ideas

- Citations — make the agent emit which file/section the answer came from, render as footnotes with a side panel
- Suggested follow-ups after each answer
- Stop / regenerate button mid-stream
- Slack bot version (same backend, different frontend)
- Auto-summarize `feedback.jsonl` weekly and post to a Slack channel

## Author

Built by a NeoCognition intern as their onboarding project — for future interns.

## License

Internal — not for distribution outside NeoCognition.
