# Week 6 — AI Vehicle Service Center: Smart Booking + Parts-Aware Scheduler

A WhatsApp booking bot for a vehicle service center (bike and car). Customers chat in English or Roman Urdu. The bot checks calendar availability and parts stock before confirming a booking, and keeps the stock sheet up to date.

## Problem

A service center handles bookings manually over WhatsApp. This causes double bookings, bookings on closed days, and bookings for services whose parts are out of stock.

## Solution

An AI agent built in n8n that talks to the customer on WhatsApp, then:

1. Checks Google Calendar for free slots (2 parallel bays, 9am-6pm, Friday closed)
2. Checks Google Sheets for part availability
3. Creates the booking in Google Calendar only after the customer confirms
4. Reduces the used part's stock and logs the consumption in a "Booking Log" sheet
5. Sends a separate daily low-stock alert to the owner on WhatsApp

## Architecture

```
WhatsApp (customer)
   -> GreenAPI -> ngrok tunnel -> n8n Webhook
   -> Edit Fields (date table + current time, calculated by code, not by AI)
   -> AI Agent (OpenAI gpt-4o-mini + Simple Memory)
        tools: Google Calendar (get events), Google Sheets (get stock), Google Calendar (create event)
   -> Get many events -> Code (finds this customer's booking, part used, Friday check)
   -> If1 (Friday violation?) -> Delete event -> fixed cancellation message
   -> If (part used?) -> Split Out -> Get stock -> Calculate new quantity
        -> Update stock row -> Append Booking Log row
   -> HTTP Request (GreenAPI sendMessage) -> WhatsApp (customer)
```

Second workflow, `low-stock-alert-workflow`:
`Schedule Trigger (9am, 4pm) -> Get stock -> Filter (stock <= threshold) -> Code (build message) -> HTTP Request (WhatsApp to owner)`

## Tools

n8n (local), GreenAPI (WhatsApp), ngrok (public tunnel to local n8n), OpenAI API, Google Calendar, Google Sheets.

## Repository contents

```
week-06/
  README.md
  workflows/
    booking-agent-workflow.json
    low-stock-alert-workflow.json
  screenshots/
```

The workflow JSON files can be imported into n8n (Workflows -> Import from file). Credentials are not included. Secrets such as the GreenAPI token were replaced with `YOUR_API_TOKEN`.

## Setup

1. Start n8n locally (default port 5678).
2. In a second terminal run `ngrok http 5678` and copy the `https://...ngrok-free.dev` URL.
3. In the GreenAPI console, set the webhook URL to `<ngrok URL>/webhook/<webhook path from the n8n Webhook node (Production URL)>`.
4. Import both workflow JSON files into n8n.
5. Reconnect credentials: OpenAI, Google Calendar, Google Sheets.
6. Put your own GreenAPI instance ID and token in the HTTP Request nodes.
7. Publish (activate) both workflows.

Note: with the free ngrok plan the URL can change after a restart, so the GreenAPI webhook URL must be updated each time.

## Key lessons from building this

- **LLMs are unreliable at date arithmetic.** Relative dates ("kal", "3 din baad") and the Friday rule were moved out of the AI: an Edit Fields node builds a 30-day date table with `[CLOSED - FRIDAY]` tags, and the AI only looks values up. A code check also catches a wrongly booked Friday and cancels it.
- **n8n stops a branch when a node returns 0 items.** A "Get many events" node returning nothing for a plain greeting blocked the WhatsApp reply. Fixed with "Always Output Data".
- **`$json` only refers to the previous node.** Fields from earlier nodes must be read by node name, e.g. `$('Node name').item.json.field`.
- **Prompt text with `{{ }}` is evaluated by n8n.** Literal braces in the system prompt broke the agent.
- **Split Out creates multiple items**, and every later node runs once per item, which can cause duplicate WhatsApp replies.

## Known issues (not yet fixed)

- The bot sometimes replies in Roman Urdu to an English message despite the language rule in the system prompt.
- Cancelling a booking still reduces part stock; it should not (or should restore it).
- The "Date" column in Booking Log shows when the row was logged, not the booking's date and time.
- When a service uses 2 parts, the customer may receive the reply twice (one per Split Out item). Fix: combine items with an Aggregate node before the final HTTP Request.

## Status

Tested live on WhatsApp: booking flow, inventory check, Friday-closed rule, business-hours check, parts auto-decrement, Booking Log, low-stock alert.
