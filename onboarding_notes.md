# Onboarding Notes (raw braindump — to be restructured)

## Day 1: Arrival & Office

**Office address:** 1881 Page Mill Road, Palo Alto
**Suite / office number:** 136 (inside the Industrious co-working space)

**What to do when you arrive:**
- Just walk in and introduce yourself to the folks at the main desk
- Your mentor will come and take you inside
- No ID card on day 1 — that's normal
- Introduce yourself and chat with people to get to know them

**First task:** Collect your laptop. Everything else flows from there.

## Things to ask about

**Before coming to the office:**
- Ask about Webox coupons

**After you arrive, ask the main desk for:**
- Gym access code
- Code for entering the office post 5 PM (you'll need the app for this — main desk will help you get into it)

## Before Day 1: Rippling (pre-onboarding)

Rippling is the HR platform that handles new-hire paperwork for NeoCognition. They handle payroll, tax forms, etc.

**Timeline:**
- Rippling onboarding portal invite is sent ~20 days before your start date (initial setup — asks for your email ID preference, which becomes your NeoCognition company email)
- The detailed paperwork checklist (below) lands roughly **1 week before** your start day
- A random temp password for your new NeoCognition Gmail is sent to the email you're signed into Rippling with
- **If you haven't received a Rippling invite 3 business days before your start date, contact HR**

### What to expect

HR sends you a Rippling invite via email once your offer is countersigned. The full checklist below takes about **20–30 minutes** and should be completed before Day 1.

### Pre-Day-1 checklist (in Rippling)

**Rippling account setup**
- [ ] Accept the Rippling invite from the HR email
- [ ] Create your Rippling account and set a password
- [ ] Complete identity verification — upload government-issued ID (driver's license or passport)

**Tax & Payroll**
- [ ] Complete **W-4** (Federal Tax Withholding) — select filing status and allowances
- [ ] Complete **state tax withholding** form if applicable
- [ ] Enter **direct deposit** info — bank account + routing number (double-check this is correct — payroll depends on it)

**HR paperwork**
- [ ] Sign the **offer letter**
- [ ] Complete **I-9** (Employment Eligibility Verification) — you'll do in-person verification on Day 1, so bring original ID docs (see reminder below)
- [ ] Review and sign **IP & Confidentiality Agreement**
- [ ] Complete **benefits enrollment** — health, dental, vision (deadline typically within 30 days of start)
- [ ] Enroll in **401(k)** — optional but do it early; some plans have waiting periods
- [ ] Review and confirm **equity / stock option grant** details, if applicable

**Optional but helpful before Day 1**
- [ ] Check your personal email for any IT instructions or laptop shipping info

**Day-before reminder (not in Rippling but critical):**
- [ ] **Confirm with your point of contact that they've informed the Industrious main desk that you'll be arriving on Day 1** — otherwise the front desk won't let you in.

### ⚠️ I-9 reminder — what to bring on Day 1

Bring **originals** (not copies) of your ID documents for in-person I-9 verification.
- A **passport** counts as a single document, **OR**
- A **driver's license + Social Security card** combination

**How you'll know I-9 is complete:** You'll get a confirmation email along the lines of *"Your physical document inspection process has been successfully completed by [name]."* If you haven't received it, follow up with HR.

### ⚠️ SSN is mandatory — TIN / ITIN will not work

You must have a valid **Social Security Number (SSN)** to be paid and complete I-9 at NeoCognition. A **TIN / ITIN is NOT accepted** as a substitute.

**If you don't have one yet** (common for international hires on H-1B / OPT / etc.):
- Apply for your SSN immediately at the nearest Social Security Administration office — you cannot apply online for a first-time SSN.
- Bring your passport, visa, I-94, and any work authorization documents.
- It typically takes 2–4 weeks. Notify HR (`@HR` / Rippling messages) the day you apply so they can flag your account as "SSN pending" and avoid payroll disruptions.
- You can start work without the card in hand, but you must provide the number to payroll as soon as you receive it.

### 🔍 Background check (Checkr) — finish by Day 3

NeoCognition runs background checks through **Checkr**.

- An invitation email is sent to the **email you registered in Rippling** (usually personal) — check spam.
- You'll need to consent and fill in a short form (employment history, addresses, SSN). Takes about 10 minutes.
- **Must be completed before end of Day 3** — payroll and certain system accesses are gated on this.
- If you haven't seen the Checkr email by Day 2, ping HR. Don't sit on it.

## Day 1 — Morning: IT & Identity

Official checklist for the first half of Day 1.

- [ ] **Complete I-9 in-person verification with HR** — bring your ID documents. *(Not always required on Day 1, but bring originals just in case they ask.)*
- [ ] **Receive and power up your company laptop**
- [ ] **Activate your company email (Google Workspace)** — details below
- [ ] **Set up 1Password / team password vault** — IT will send the invite. Install the browser extension too.
- [ ] **Install Slack**, join the workspace, set up your profile
- [ ] **Send your intro in `#general`** on Slack
- [ ] **Meet with your buddy**
- [ ] **1:1 intro with your manager**
- [ ] **Get added to team groups** and review recurring meetings on your calendar

### Activating your company email (details)

1. Open the Gmail app (or gmail.com) and sign in with your new NeoCognition email + the temp password from Rippling
2. You'll be prompted to change the password on first login
3. **Enable MFA on your Google Workspace account — this is mandatory at NeoCognition.** On first sign-in, use one of the temporary single-use codes provided, then **immediately** go to https://myaccount.google.com/security and set up your own multi-factor authentication. Authenticator app (Google Authenticator, 1Password, or Authy) is recommended over SMS — SMS is vulnerable to SIM-swap attacks. Once configured, MFA applies across Gmail, Drive, Calendar, and every other Google Workspace tool you'll use day-to-day.

## Day 1 — Afternoon: Access Confirmed

By the afternoon, work with your mentor to confirm you have access to all the tools you'll need. Most of these require your mentor to add you — don't expect them to appear automatically.

- [ ] **GitHub** — accept the org invite, confirm you can view team repos *(ask your mentor)*
- [ ] **Notion — project tasks** — confirm you can see project tasks *(ask your mentor)*
- [ ] **Notion — wiki** — confirm access, then read the **Engineering home page** *(ask your mentor for the link)*
- [ ] **GCP (Google Cloud Console)** — confirm view-only access *(ask your mentor)*
- [ ] **Modal** — second compute environment used at NeoCognition; ask your mentor to get added

> 💡 Pattern: on Day 1 afternoon, anything you can't access yet → ping your mentor. They expect this. Don't sit silently for hours waiting for invites to appear.

## Logins — Tools You'll Need on Day 1

> **Sign in with your `@neocognition.io` email unless noted otherwise.**
> If you hit any login trouble below, ping **@Yao Yang** or **@Xiang Deng**.

| Tool | URL / Location | Notes | Required |
|---|---|---|---|
| **1Password** | 1password.com | Official password manager. **Install the browser extension** too. | ✅ Required |
| **Tailscale** | tailscale.com | Login with company account; add your laptop to the tailnet. | ✅ Required |
| **Slack** | neocognition.slack.com | Team communication. | ✅ Required |
| **Notion** | notion.so | Engineering wiki, project tasks, RFCs. | ✅ Required |
| **GoLinks** | app.golinks.io | Install the Chrome extension; login with company Gmail. | |
| **GitHub** | github.com | Use company email. You may need to wait for the org invite to land. | ✅ Required |
| **GCP Console** | https://cloud.google.com/ | Read-only access to start. | |
| **Cursor** | https://cursor.com/download | Company group plan — enroll with company email. | |
| **Claude Code** | code.claude.com | OAuth with company email; subscription is included. See "Verify Claude Code" below. | ✅ Required |
| **OpenRouter** | openrouter.ai | Primary LLM access. | |
| **Portkey** | portkey.ai | LLM gateway & observability. | |

### ⚠️ Use your company email for Cursor and Claude Code

The company sponsors group plans for **Cursor** and **Claude Code**. If you sign up with a personal email, your account won't be on the company plan — you'll either be billed personally or miss the seat entirely. **Create / log into both with your `@neocognition.io` email.**

### ⚠️ Anthropic API access: use Portkey, NOT console.anthropic.com

If you're building an app or script that calls the Claude API directly (i.e. not Claude Code or Cursor — those handle this for you), use the company's **Portkey gateway**, not a personal key from console.anthropic.com.

**Why:**
- **Signing up at console.anthropic.com with your company email creates a personal Anthropic account** — it does NOT automatically bill NeoCognition. You'd be on the free-trial tier (10K input tokens/min — extremely tight) and any usage past that would hit your personal card.
- Email identifies you, but **billing follows the workspace the key was issued under**. Portkey is the workspace NeoCognition has set up with the Claude Team plan + payment attached.

**How to use it:**
1. Go to https://app.portkey.ai/api-keys and sign in with your `@neocognition.io` email — you'll be joined to the company workspace.
2. Create an API key there.
3. In your code, point the Anthropic SDK at Portkey instead of api.anthropic.com:

   ```python
   from anthropic import Anthropic

   client = Anthropic(
       api_key="dummy",                              # auth goes via the header below
       base_url="https://api.portkey.ai",
       default_headers={"x-portkey-api-key": "YOUR_PORTKEY_API_KEY"},
   )
   client.messages.create(
       # Use the full @<provider-slug>/<model-name> identifier from your Portkey
       # Model Catalog. At NeoCognition the slug is "anthropic-default":
       model="@anthropic-default/claude-sonnet-4-6",
       max_tokens=1024,
       messages=[{"role": "user", "content": "Hello"}],
   )
   ```

   The rest of the Anthropic SDK works the same (streaming, prompt caching, tool use, etc.) — Portkey is a passthrough. If you ever get `'Following keys are not valid: <slug>'`, the provider slug in the model identifier doesn't match what's in the company's Portkey **Model Catalog** — check the UI for the current slug.

**Tradeoffs to be aware of:**
- ~50–100ms extra latency per call (the Portkey hop)
- If Portkey is down, your app is down
- Brand-new Anthropic features can take a few days to land in Portkey

If you genuinely need to use console.anthropic.com directly (e.g. a personal side project paid out of pocket), that's fine — just know it's *your* card on the line, not NeoCognition's.

### Verify Claude Code (60-second smoke test)

After install, confirm Claude Code is working and using your company plan:

1. **Install** (skip if already done):
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. **Open a terminal in any folder** (your home directory is fine) and run:
   ```bash
   claude
   ```
3. **Sign in when prompted** — choose "Log in with Claude", and use your `@neocognition.io` Google account in the browser window that opens.
4. **Run this single prompt** to confirm everything works end-to-end:
   > `What model are you, and which workspace/organization is this session on?`

   ✅ If the reply names a Claude model **and** mentions the NeoCognition workspace/organization, you're done — you're on the company plan.
   ❌ If it says "personal" / "individual plan" / asks you to subscribe, you logged in with the wrong account. Run `/logout`, then `claude` again, and pick your `@neocognition.io` Google account.

5. **Optional sanity check:** try `claude "list the files in this folder"` to confirm tool use is working too.

If any of this fails, ping **@Yao Yang** or **@Xiang Deng**.

## Compute: Modal vs GCP

NeoCognition has two compute environments. **They're for different things — pick based on your use case, not by default.**

| Use case | Pick |
|---|---|
| "I just want to test something quickly" / one-off script / batch inference / parallel sweep | **Modal** |
| "I need to scale a stateless job out" (10 GPUs in parallel, big batch run) | **Modal** |
| "I want a real dev box to SSH into, install stuff, keep state across days" | **GCP** |
| "I'm setting up a long-running experiment / training run that I want to babysit" | **GCP** |
| "I want a persistent Jupyter / VS Code Remote workspace that doesn't disappear" | **GCP** |

### In plain words

- **Modal** = **stateless and fast**. Each container is fresh — your file system disappears when the job ends (unless you mount a Volume). Best when you want to run something, get the output, and move on. Or when you want to fan out to many GPUs without managing infra.
- **GCP** = **persistent and yours**. You create a VM, install packages, save files to disk, leave it running — it's like a remote computer you own (and pay for) for as long as it's up. Best when you're iterating on something for days/weeks.

### Rule of thumb

- **Quick test or scale-out job?** Modal. You'll be productive in 5 minutes.
- **Day-to-day development?** GCP. Set it up once, then SSH in like you would your own machine.
- **Not sure?** Default to Modal for anything that runs and ends. Switch to GCP the moment you find yourself wanting your state to survive across sessions.

(And **always stop your GCP VM when you're not using it** — persistent disks keep costing money even when the VM is stopped, but the compute and GPU charges stop. The biggest GCP bill surprises come from VMs left running over a weekend.)

**Before you can use Modal:**
- ✅ **Confirm with your mentor that you've been added to the Modal workspace** (e.g. `neocognition-dev`). If you haven't, `modal setup` will fail.

**Modal quick start (full guide is separate):**
- See [modal_setup_guide.md](modal_setup_guide.md) for the full Modal + VS Code developer setup — covers interactive & non-interactive modes, single-GPU, multi-GPU, CPU-only, persistent volumes, and a quick-reference command table.
- The 30-second version after your mentor adds you:
  ```bash
  pip3 install modal
  modal setup            # links your machine to the workspace
  modal shell --gpu T4   # cheapest GPU — good for first smoke test
  ```
  Inside the shell, `nvidia-smi` should show a GPU. `Ctrl+C` in the local terminal to stop.

> 💡 Cost reminder: Modal charges per second. CPU containers are ~10× cheaper than H100 — use the smallest GPU that works during dev, and switch up only for real training runs.

**GCP — when you specifically need it:**
- Full setup guide: [gcp_setup_guide.md](gcp_setup_guide.md) — covers project/quota setup, creating CPU / single-GPU / multi-GPU VMs, NVIDIA driver install, VS Code Remote-SSH, Miniconda + PyTorch environments, Jupyter via SSH tunnel, persistent storage, and a debugging checklist.
- The most common GCP blocker is **GPU quota** — request it early; A100/H100 quotas are not granted by default.
- Always **stop your VM** when you're done — compute charges keep running otherwise.

## End of Day 1 — Wrap-up

Before you head home:

- [ ] **Schedule a recurring 1:1 with your mentor** (weekly is typical). Put it on the calendar today — don't wait for them to set it up.
- [ ] **Talk to folks around the office** to learn more about the company — what they're working on, how teams are organized, what the culture's like. This is the easiest it'll ever be to introduce yourself, so use Day 1's "I'm new" energy while it lasts.

## Mandatory but easy-to-miss tasks

These are subtle — don't skip them:
- Complete all courses assigned to you in **Rippling**
- Complete all courses in **Vanta**

## The Office Building: Industrious at Palo Alto Page Mill

NeoCognition's office sits inside a co-working space called **Industrious** (at 1881 Page Mill Road). A lot of the day-to-day office logistics (door access, wifi, meeting rooms, food) are run by Industrious, not NeoCognition.

**Contact Industrious:** pagemill@industriousoffice.com — or message them through the Industrious mobile app.

### WiFi setup — IMPORTANT (two stages)

WiFi is managed by **IsoFy**. There are two stages — get them in the right order.

**Stage 1 — Day 1, guest access (so your laptop can get online at all):**
- When you first open your laptop it'll ask for a wifi connection
- **Sign in as a guest using your PERSONAL email — NOT your company email.** Using your company email here will clash later when you create your actual IsoFy member account.
- If you have trouble, the front desk will help.

**Stage 2 — Member wifi (do this once you have your company email working):**
- You'll receive an **IsoFy Account Invitation email** for member wifi
- Accept the invite and set up your IsoFy member account — this gives you proper (non-guest) wifi access going forward

### Industrious Member Portal

You'll get an emailed invite to the Industrious Member Portal: https://portal.industriousoffice.com/home

- **Sign in with your company email** (this is the account that won't clash because you used personal email for the guest wifi)
- Use it to: book meeting rooms, reserve workspaces, view daily menu & events, browse other Industrious locations

### Industrious mobile app — download it on day 1

The app is how you get into the building outside staffed hours.
- Office is staffed Mon-Fri, 8 AM – 5 PM
- Log in to the app with your Member Portal credentials

**Getting your door code:** Once you finish the basic Industrious account setup (login + filling in your info), you'll receive an email with your door code. The same code also appears inside the app. **Memorize this code** — you will use it daily.

**Two different doors, two different unlock methods:**
- **Main entrance door:** Bluetooth via the app's Digital Key (works best within ~3 feet of the lock). PIN works here too.
- **Actual office space door (inside):** Bluetooth does NOT work here — you must enter your PIN.

That's why memorizing your code matters: the inner office door requires it every time.

### Getting there & parking

- **Car:** Parking lot around the building, first-come-first-serve. Easy highway access.
- **Bus:** Stops on Porter Drive and Page Mill Road
- **Train:** Cal Ave train station, ~10 min drive. Free Stanford shuttle runs from Palo Alto and California Ave stations.
- **Bike:** Bike lockers available — bring your own lock.

### Spaces inside

- **16 reservable meeting rooms** with A/V — book via Member Portal during business hours
- **Phone booths** — first-come-first-served, 1 hour limit
- **Bookable private offices** — by the day, for team focus/collab
- **Fitness center**, **outdoor space**

### Food & Beverage (included)

- **Breakfast:** 8:30 – 10 AM
- **Snacks:** afternoon
- **Coffee / tea / sodas:** 8:15 AM – 4:30 PM
- **Happy hour:** weekly on Thursdays

### Mail address

```
[Your Name / NeoCognition]
1881 Page Mill Road, Suite 136
Palo Alto, CA 94304
```

Incoming mail/packages live in the mailroom. Outgoing letters go in the outgoing basket. Large packages — schedule pickup via UPS or FedEx yourself.

### Useful links

- Member Portal: https://portal.industriousoffice.com/home
- Member Handbook (PDF): https://drive.google.com/file/d/1esBZSZXSsmBXWzL5AMrinAwnJynchJWB/view

## Benefits & Stipends

NeoCognition gives you monthly stipends plus in-office meals. All stipend spending is reimbursed/managed through **Ramp** (see the Ramp section below for the submission rules).

### 🏥 Health insurance — full-time employees, read this carefully

If you're a **full-time hire** (not an intern/contractor):

- You'll enroll in **health, dental, and vision** insurance during Rippling onboarding — there's typically a **30-day window** from your start date.
- **Read the policy details before you click "Submit."** Specifically check:
  - Which carrier (you may have multiple plan options — PPO vs HMO, HSA-eligible vs not)
  - Deductible, out-of-pocket maximum, and monthly premium
  - Whether your current doctors are in-network
  - Whether dependents are covered and at what cost
  - Effective date — usually 1st of the month after your start date, but verify
- If you have questions on the policy itself (not the enrollment workflow), the carrier's member services line is usually the fastest answer — number is in the policy PDF Rippling sends.
- Interns/contractors: this section doesn't apply — your benefits are spelled out in your offer letter.

### 💰 Personal Lifestyle Stipend — $500/month

A flexible monthly stipend for overall work/life wellness. Eligible categories:

- **Meals & groceries** — dining out, meal kits, meal prep, coffee shops
- **Exercise & fitness** — gym memberships, classes, personal training, sports/outdoor equipment
- **Personal care** — spa, massage, haircuts, salon services, skincare
- **Home office improvements** — ergonomic furniture, desk accessories
- **Personal subscriptions** — streaming, wellness apps (Calm, Headspace, Spotify, Netflix)
  - ⚠️ **Do NOT purchase work-related software on the NeoCognition account — SOC compliance mandate.**
- **Books, audiobooks, magazines** — physical, digital, or audio
- **Internet & phone** — home internet, mobile data, phone bill
- **Mental health & wellness** — therapy, counseling, coaching, meditation programs
- **Hobbies & leisure** — creative classes, events, recreational activities
- **Personal development** — online courses, language learning apps

### 🚗 Transportation Stipend — $200/month

Covers regular commuting costs:
- Public transit passes and fares
- Parking fees
- Gas and fuel
- Rideshare services
- EV charging

### ⚡ On-site EV Charging

EV charging is available on-site through **ChargePoint** — download and set up the app. File the EV reimbursement under your **Transportation Stipend** in Ramp.

### 🍽️ In-Office Meals (7 days a week)

NeoCognition provides complimentary meals every day for employees working from the Palo Alto office.

**Weekday lunch & dinner — via WeBox:**
- **Lunch:** order by **7:30 AM** the day-of
- **Dinner:** order by **2 PM** the day-of
- Meals can be automated / ordered in advance via the WeBox app — set up a recurring order so you don't forget
- **Do NOT order if you're OOO or won't be there to eat it**

**Weekend meals:**
- Contact **@Surbhi Agarwal** for **Uber Meal vouchers** (new experimental program)

**Friday Happy Hour:**
- We do a Friday afternoon happy hour. Join the order before **12:30 PM Friday**.
- Order link: https://eats.uber.com/meal-plan/58b3f764-9bbd-4072-8ae9-1f66bc7b07f9
- *(Note: the source doc shows two URLs for this link — using the actual href. Confirm with Surbhi if it doesn't work.)*

### 🏋️ In-Office Gym Access

The gym is on-site (Industrious fitness center). **Ask the Industrious main desk** for the access code.

### 🖥️ Additional Equipment for your Desk

Need extra equipment (monitor, keyboard, mouse, stand, etc.)?
- Share **Amazon.com links** in the **#help** Slack channel
- Tag **@Surbhi Agarwal**
- All requests are subject to review and approval

## Who to ask — quick routing

Use this as a quick reference for who to ping (always in **public channels first** per the Slack norms below, not DMs):

| Question type | Who | Where |
|---|---|---|
| **Technical / engineering questions** (ML, code, infra, setup) | **@Yao Yang** | `#eng` or relevant tech channel |
| Login / account issues for any company tool | @Yao Yang or @Xiang Deng | `#help` |
| Benefits, WeBox / meals, reimbursements, desk equipment, weekend meal vouchers | @Surbhi Agarwal | `#help` |
| Slack channel invites, Notion page links, Modal/GitHub access, team-specific questions | Your mentor | DM or `#help` |
| I-9, Rippling, payroll, tax forms, bank info, benefits enrollment | HR | Rippling messages |
| Office building (gym code, door codes, mail, parking, food schedule) | Industrious main desk (in person), or pagemill@industriousoffice.com | — |

If you're not sure who to ping, default to **your mentor** first and they'll route you.

## Slack

Slack is **the** main collaboration environment at NeoCognition — not just a chat tool. Decisions are made there, context is shared there, and the history of our work lives there. The way you use Slack matters more than most other tools.

### When you join

- Confirm you've been invited to the NeoCognition Slack workspace
- Ask your mentor to add you to all the channels relevant to your role — you won't know what you're missing if no one tells you
- Learn what each channel is for (where IT questions go vs. HR vs. engineering, etc.) so you ping in the right place

### Slack best practices at NeoCognition

We deliberately run a **Slack-first, public-by-default culture**. Read these before you start posting — the norms are intentional.

**1. Public by default**
- Use **public channels**, not DMs, for almost everything. DMs are invisible, unsearchable to others, and force re-explanations later.
- Exceptions: HR, compensation, and genuinely sensitive interpersonal matters.
- Use topical channels (e.g. `#eng`, `#research`, `#papers`). When unsure → post publicly.
- It's encouraged to create new channels and retire unused ones.

**2. Organize replies in threads**
- **Reply in a thread**, not the main channel, unless you're starting a new top-level topic.
- Announcement channels are thread-only for replies — respect that.
- If a thread needs to move elsewhere, link the parent message in the new channel.

**3. High engagement**
- Default: scan all messages in company channels **within ~1 hour during working hours**.
- If something is related to you → **respond or engage promptly** (answer, give input, or at least acknowledge).
- If it's useful but not actionable → at least react with an emoji.
- Use emoji reactions generously to signal state: 👍 = seen/agree, 👀 = looking into it, ✅ = done. Custom fun emojis are welcome as long as meaning is clear.
- Boundaries are healthy. Use **Do-Not-Disturb** schedules and notification controls — but uphold prompt engagement during working hours.

**4. Mention etiquette (balance reach vs. noise)**
- `@person` → the accountable owner. Avoid carpet mentions.
- `@here` → **urgent and time-sensitive** for currently-active members. Use sparingly.
- `@channel` / `@everyone` → **rare**, only for company-wide relevance. Admins may throttle these.

### Why this matters (in one line)

When Slack is used openly, it becomes our collective memory and coordination system. When used in silos (DMs, small groups), it fragments knowledge, forces repetition, and prevents alignment.

### Background reading (optional but recommended)

- [Basecamp — "Work in Public"](https://basecamp.com/guides/how-we-communicate#work-in-public)
- [GitLab Handbook — Communication](https://handbook.gitlab.com/handbook/communication/#communicating-effectively)
- [Stripe Writing Culture](https://slab.com/blog/stripe-writing-culture/)

## Notion

NeoCognition uses Notion for internal docs.

- Once you're in Slack, **ask your mentor which Notion links/pages you should know about** — there's no central index you'll find on your own. The important pages are the ones a human points you to.

## Ramp — Expenses & Reimbursements

NeoCognition's finance team uses **Ramp** for all work-related expenses, stipend reimbursements, and corporate card transactions.

**Getting started:**
- You'll receive an invite email from the finance team to create your Ramp account
- **The invitation expires — accept it promptly** (check the expiry date in the email)
- All reimbursements (lifestyle stipend, transportation stipend, work expenses) go through Ramp

**Day-1 lunch reimbursement:** If you order food on your first day without going through WeBox, keep the bill — you can submit it for reimbursement via Ramp.

**CRITICAL — turn on notifications:**

Go to **Profile → My Settings → Notifications** and enable **push notifications for receipt and memo reminders**. Compliance matters here.

**Memo field will be made mandatory.** Log into Ramp and clear any flagged items on your Home screen (transactions missing receipts or memos).

### Receipt & submission rules (don't skip these)

- **Keep itemized receipts** for all purchases. Each receipt must show:
  - Vendor name
  - Transaction date
  - Transaction details (line items)
  - Dollar value
  - Card number
  - Your name
- **No partial / zoomed-in screenshots** — these get declined and you'll have to pay out of pocket
- **Add a clear memo** describing each expense
- **Submit expenses promptly** with memo and receipts attached
- **Set a calendar reminder** to clear all receipt submissions on the **last day of every month**
- Card transactions **above $75** without a receipt → you pay out of pocket

Questions on eligible expenses or how to submit them in Ramp → contact **@Surbhi Agarwal**.
