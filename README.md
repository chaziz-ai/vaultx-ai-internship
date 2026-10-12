# VaultX AI Internship

This repository contains my work for the **VaultX Cyber Tech AI/ML Engineering Internship (Summer 2026)**. Each week focuses on a different set of AI engineering skills, building toward real-world LLM-powered applications and automation systems.

**Intern:** Aziz ur Rehman

## Journey at a Glance

| Week | Topic | Main Result |
|------|-------|-------------|
| 1 | Foundations: API + prompts | Reusable `APIWrapper`, CLI summarizer |
| 2 | Prompt engineering + structured output | Classification/extraction tools, accuracy 55% to 93.33% |
| 3 | n8n automation | Inbox triage, content pipeline, error handling |
| 4 | RAG | ChromaDB pipeline, 83.3% eval, 100% grounding, FastAPI + Slack |
| 5 | RAG + tool-calling agent | Agent with calculator, doc search, web search, memory |
| 6 | Business automation | Vehicle service center WhatsApp booking bot |
| 7 | Final project | SolarFlow lead-to-quote pipeline (5 workflows) |

## Setup

1. Clone the repository:

```bash
git clone https://github.com/chaziz-ai/vaultx-ai-internship.git
cd vaultx-ai-internship
```

2. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root folder with your API keys:

```
OPENAI_API_KEY=your_api_key_here
```

Never commit `.env`. It is listed in `.gitignore`.

## Structure

```
vaultx-ai-internship/
├── week-01/   API wrapper, CLI summarizer, temperature experiments
├── week-02/   Prompt library, structured output, classifier, extractor
├── week-03/   n8n automations (inbox triage, content pipeline)
├── week-04/   RAG pipeline (ChromaDB, FastAPI, Slack via n8n)
├── week-05/   Tool-calling agent (FastAPI + n8n + Slack)
├── week-06/   Vehicle service center bot (Workflows/, README, report)
├── week-07/   SolarFlow final project (Workflows/, README, report)
├── requirements.txt
└── README.md
```

Each week folder has its own report named `VX_AI_W[N]_Aziz_ur_Rehman.pdf` where applicable.

---

## Week 1: Foundations

**Goal:** Set up the environment and talk to an LLM from code.

- Dev environment (Python, venv, VS Code, Git)
- AI glossary
- First API call and temperature experiments
- `api_wrapper.py`: reusable API wrapper class
- `summarizer.py`: CLI summarizer tool

**Skills:** Python, APIs, `.env` secrets, Git, LLM basics

## Week 2: Prompt Engineering and Structured Output

**Goal:** Make LLM output reliable and measurable.

- Prompt template library (5 patterns)
- Structured output with Pydantic
- Classification tool with an evaluation harness
- Extraction tool
- Prompt iteration: accuracy **55% to 93.33%**
- Reusable `vaultx_prompts` package with logging

**Skills:** Prompting, structured outputs, evaluation

## Week 3: n8n Automation

**Goal:** Move from scripts to workflow automation.

- Inbox triage: Gmail, OpenAI, Google Sheets
- Retry logic and error log
- Content pipeline: Google Sheets trigger, OpenAI, output sheet
- Runbook PDF and demo video

**Skills:** n8n, workflow design, error handling

## Week 4: RAG Pipeline

**Goal:** Answer questions from your own documents.

- PDF ingestion and chunking
- ChromaDB vector index (`text-embedding-3-small`)
- Retrieval plus grounded generation (`gpt-4o-mini`)
- Evaluation: **72.2% to 83.3%** (k=3 to k=5), **100% grounding**
- FastAPI service with Slack automation through n8n
- Guardrails: weak-retrieval check, hallucination check, structured sources

**Lesson:** Higher k helps retrieval, but chunk-boundary problems need a chunking change. Limitations are documented honestly.

## Week 5: RAG + Tool-Calling Agent

**Goal:** An agent that chooses between tools.

- Tools: calculator, document search (RAG), web search (Tavily)
- FastAPI backend, n8n orchestration, Slack delivery
- Conversation memory in Google Sheets
- WhatsApp integration attempted but blocked (ngrok port mismatch, Meta webhook compatibility); documented
- Bugs fixed: language detection, date/time accuracy, rate limiting

Run the API from inside `week-05/`:

```bash
cd week-05
uvicorn api:app --reload
```

## Week 6: Vehicle Service Center Booking Bot

**Goal:** Solve a real SME problem with AI and automation.

A WhatsApp bot (GreenAPI + n8n) that checks Google Calendar availability and Google Sheets parts inventory before confirming a booking.

- **Booking agent:** Webhook, date context, AI Agent (gpt-4o-mini, memory, 3 tools), WhatsApp reply
- **Low-stock alert:** scheduled workflow that messages the owner
- **Auto stock decrement** and Booking Log after each booking
- Friday-closed safety net in deterministic code

**Key lesson:** LLMs are unreliable for dates, weekdays, and business hours. Compute facts in code, use the LLM only for conversation.

**Known limitations:** occasional Roman Urdu reply to English message; cancelling does not restore stock; Booking Log date is log time; possible duplicate reply when a service uses 2 parts.

See `week-06/README.md` and `week-06/Workflows/`.

## Week 7: Final Project, SolarFlow

**Goal:** Real business, real problem, AI solution, automation, business value.

**Problem:** A solar installer cannot follow up with every lead, so sales are missed.

| Workflow | Purpose |
|----------|---------|
| WF1 Lead Estimate | WhatsApp message to AI extraction, code-based estimate, lead score, Leads sheet, reply |
| WF2 Quote PDF | Fills a Google Doc template, exports PDF, sends on WhatsApp |
| WF3 Follow-ups | Scheduled follow-up 1 and 2 (English or Roman Urdu) |
| WF4 Weekly Report | Monday email report to the owner |
| WF5 Error Handler | Logs failures to an Errors sheet |

Customer replies are classified (interested, negotiating, not interested, new estimate, other), stop follow-ups, and alert the owner by email.

**Design principle:** code does the calculations, AI does the conversation.

**Assumptions (honest note):** no real installer was interviewed. Rates other than the panel rate, the unit conversion, lead-score thresholds, quote terms, and company name are assumptions.

**Tech:** n8n, OpenAI gpt-4o-mini, GreenAPI, Google Sheets/Docs/Drive/Gmail, ngrok.

See `week-07/README.md` and `week-07/Workflows/`.

---

## Tech Stack

Python, FastAPI, ChromaDB, Pydantic, n8n, OpenAI API, Tavily, Slack, WhatsApp (GreenAPI), Google Workspace APIs, ReportLab, Git/GitHub.

## Key Lessons

1. Document limitations honestly instead of inflating results.
2. Measure prompts and RAG with evaluations, do not guess.
3. Deterministic code for facts, LLM for language.
4. Never commit or paste secrets. Exported workflows use `YOUR_API_TOKEN`.
5. Multiline or quoted text breaks raw JSON bodies, use field-based mode.
