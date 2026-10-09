# SolarFlow: AI Lead-to-Quote Automation (WhatsApp)

Week 7 final project of the VaultX Cyber Tech AI Internship.

A solar installer gets inquiries on WhatsApp but cannot estimate and follow up with every customer. SolarFlow does it automatically: it reads the customer's message, calculates an estimate, sends a PDF quotation, follows up, understands replies and alerts the owner.

**Real Problem -> AI Solution -> Automation -> Business Value**

## What it does

- Reads a WhatsApp message (English or Roman Urdu) and extracts bill, city, appliances and language
- Calculates system size, itemised cost and a lead score (hot / warm / cold) with code, not AI
- Sends the estimate and a PDF quotation, saves the lead in Google Sheets
- Sends timed follow-ups until the customer replies
- Classifies replies (interested, negotiating, not interested, new estimate, other), updates the status, replies in the customer's language and emails the owner
- Sends a weekly report and logs workflow errors

**Design rule:** AI handles the conversation, code handles the numbers.

## Workflows

| File | Purpose |
|---|---|
| `Workflows/FinalProject-WF1 - Lead Estimate.json` | Main flow: message -> estimate, lead row, reply handling |
| `Workflows/FinalProject-WF2 - Quote PDF.json` | Builds the PDF quotation from a Google Doc template and sends it |
| `Workflows/FinalProject-WF3 - Follow-ups.json` | Scheduled follow-up 1 and follow-up 2 |
| `Workflows/FinalProject-WF4 - Weekly Report.json` | Monday 9am report emailed to the owner |
| `Workflows/FinalProject-WF5 - Error Handler.json` | Writes failed runs to the Errors sheet |

## Tech stack

n8n (self-hosted), OpenAI gpt-4o-mini, GreenAPI (WhatsApp), ngrok, Google Sheets / Docs / Drive, Gmail

## Estimate logic

```
units = bill / 50
kW    = ceil((units / 120) * 2) / 2
total = panels + inverter + structure + installation + net metering
```

Example: bill 30,000 -> 5 kW -> Rs 455,000. Lead score: hot at 40,000 or more, warm at 20,000 or more, otherwise cold.
Only the panel price (40 PKR per watt) comes from a public source; the other rates are assumptions.

## Setup

1. Import the five workflow files into n8n.
2. Create a Google Sheet with three tabs:
   - `Leads`: `lead_id, created_at, name, phone, city, monthly_bill_pkr, load_details, system_size_kw, estimate_pkr, score, status, last_followup, language`
   - `Price_List`: `item, rate_pkr` with items `panel, inverter, structure, installation, net_metering`
   - `Errors`: `time, workflow, error_message`
3. Create a Google Doc quotation template and connect Google Sheets, Drive, Docs and Gmail credentials in n8n.
4. Create a GreenAPI instance and put its token in n8n. **The exported files contain the placeholder `YOUR_API_TOKEN`; never commit a real token.**
5. Start ngrok, set the public URL as the GreenAPI webhook, and publish all workflows.
6. Set WF5 as the error workflow of WF1.

## Limitations

- No real installer interview: rates other than the panel price, the score thresholds and the quotation terms are assumptions
- WhatsApp free plan allows only a few chats, so only a tester number is allowed through
- Follow-up timing in the demo is in minutes (real use: 1 and 3 days)
- Reply language comes from the language stored for the lead
- Runs locally; the free ngrok URL changes after a restart

## Report

See `VX_AI_W7_Aziz_ur_Rehman.pdf` for the full report with screenshots, tests and refinements.

**Author:** Aziz ur Rehman
