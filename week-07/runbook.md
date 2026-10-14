# SolarFlow Runbook

A runbook answers one question: **something is wrong, what do I do?**
Each section: Symptom -> Likely cause -> Check -> Fix.

## System at a glance

- Host: n8n Cloud (14-day free trial, limit 1000 executions)
- Workflows: WF1 Lead Estimate, WF2 Quote PDF, WF3 Follow-ups, WF4 Weekly Report, WF5 Error Handler
- Services: GreenAPI (WhatsApp), OpenAI gpt-4o-mini (WF1 only), Google Sheets (Leads, Price_List, Errors), Gmail
- Architecture: see `docs/architecture.md`

## 1. Customer sends a WhatsApp message and gets no reply

| | |
|---|---|
| Likely cause 1 | WF1 is not Published (inactive) |
| Check | n8n Cloud -> WF1 -> is the Published/Active toggle on? |
| Fix | Publish WF1 |
| Likely cause 2 | GreenAPI webhook URL does not point to the n8n Cloud webhook |
| Check | GreenAPI console -> instance settings -> webhook URL; compare with the Webhook node's **Production URL** in WF1 |
| Fix | Paste the correct Production URL into GreenAPI. (This was needed when moving from local n8n + ngrok to n8n Cloud.) |
| Likely cause 3 | GreenAPI instance not authorized / console down |
| Check | GreenAPI console shows instance status |
| Fix | Re-authorize the instance, then send a test message |
| Likely cause 4 | **Allowlist (known limitation).** WF1 node `Filter1` only lets ONE WhatsApp number through (the test number). Messages from any other number are silently dropped |
| Check | WF1 -> Filter1 -> value on the right side of "equals" |
| Fix | Put the correct `<number>@c.us` there, or remove Filter1 before a real launch |
| Last check | n8n -> Executions -> did WF1 run? If yes, open it and find the red node |

## 1b. After importing a workflow JSON from the repo

The JSON files in the repo contain **placeholders**, not real values. After import, replace:

| Placeholder | Where | Replace with |
|---|---|---|
| `YOUR_GREENAPI_TOKEN` | GreenAPI HTTP Request nodes (URL) | your real apiTokenInstance |
| `YOUR_TEST_NUMBER@c.us` | WF1 `Filter1` | the allowed WhatsApp number |
| `YOUR_OWNER_EMAIL` | WF1 Gmail "Notify Owner..." nodes | the owner's email |

Until these are replaced the workflow will not work (for example, the filter will block every message). Also re-select the Google Sheets, Gmail and OpenAI credentials in each node.

## 2. Estimate arrives but the Quote PDF does not

Tested failure (bad GreenAPI token in WF2, on purpose).

| | |
|---|---|
| What the system does by itself | Send Quote PDF retries **3 times** (2000 ms apart). If all fail, a **fallback WhatsApp text** is sent and the workflow stops with an error |
| What you receive | Gmail **ALERT** email + a new row in the **Errors** sheet (both come from WF5) |
| Likely cause | Wrong or expired GreenAPI token, or GreenAPI is down |
| Check | Open the failed execution in WF2 -> read the error on Send Quote PDF |
| Fix | Correct the token in the credential, then trigger a new lead to confirm estimate + `Quote_Q-xxxxx.pdf` both arrive |

## 3. I received an ALERT email

1. Read the email: subject says `ALERT: <workflow name> failed`, body has the workflow name and a **link to the failed execution** (it does not include the error text).
2. Open the **Errors** sheet and find the matching row (same time): it has columns `time`, `workflow`, `error_message`.
3. Click the execution link (or n8n -> Executions -> the failed run) and look at the red node.
4. Fix the cause (usually credentials, quota, or a service outage).
5. Re-test with one real WhatsApp message.

## 4. Follow-ups are not sent (or sent twice)

| | |
|---|---|
| Not sent: cause | WF3 is not Published, or the schedule is set to once a week (current setting, to save executions) |
| Check | WF3 -> Schedule Trigger interval + Published toggle |
| Fix for demo | Set the interval to 1 minute, Publish, run the demo, **then set it back to weekly** |
| Sent twice: known issue | An earlier test with 5 lead rows sent each follow-up stage twice. **Root cause not found.** A clean test with a single lead row worked correctly (followup1, followup2, then not_interested reply) |
| Workaround | Keep the Leads sheet clean before demos (no old test rows) |
| **Demo thresholds** | The Code node in WF3 uses `T1 = 1` and `T2 = 2` **minutes** (demo values). Its own comment says real use would be 1 day / 3 days. Production values are NOT set yet; change T1 and T2 before real use |
| **Design risk** | WF3 sends the WhatsApp message first and updates the Leads row after. If the update fails, the row keeps its old status and the next run can send the same follow-up again. This is a design observation, not a proven cause of the duplicate issue above |
| **Who gets messages** | WF3 reads every row in Leads; it has no allowlist. With real leads in the sheet, real people would receive follow-ups |

## 4b. The weekly report email did not arrive (WF4)

| | |
|---|---|
| Schedule (from the exported JSON) | Weekly, Monday, 09:00. The JSON does not state a timezone, so it follows the n8n account/workflow timezone |
| Likely cause | WF4 is not Published, or the Gmail credential expired |
| Check | WF4 -> Published toggle; Executions list for Monday 09:00; open a failed run to see the red node |
| Fix | Publish WF4 / reconnect Gmail credential, then use **Execute workflow** once to test |
| How to read the numbers | The report counts leads created in the last 7 days. "Follow-up 1/2 sent" actually counts leads **currently** in status followup1/followup2, so a lead that later moved to interested or not_interested is no longer counted |

## 5. Executions or credits are running out

- n8n Cloud trial limit: 1000 executions. A WF3 schedule of every 1 minute burns executions fast.
- Check: n8n Cloud usage page.
- Fix: set WF3 to weekly (or 30 min at most) outside demos.
- OpenAI: project spend limit is **$5**, alerts at 80% and 100%. If OpenAI calls fail with a quota error, check the OpenAI project Limits page.

## 6. The n8n trial ended

- The trial lasts 14 days from 2026-10-13. **TODO: confirm exact end date in the n8n Cloud account.**
- After it ends the workflows stop. Options: upgrade (Starter plan, see the Cost & Scaling sheet) or export all workflow JSONs and re-import elsewhere.
- After moving to any new n8n URL, **update the GreenAPI webhook URL** (section 1) and re-add credentials.

## 7. Secrets

- API keys and tokens live only in n8n **Credentials**, never inside workflow JSON files or Git.
- If a key may have leaked: revoke it in the provider's console, create a new one, update the n8n credential.

## TODO before submission (verify, do not guess)

- [x] WF4: active, weekly Monday 09:00 (from exported JSON)
- [x] WF1, WF2, WF3, WF4 all have the same errorWorkflow id set in their JSON settings
- [x] Confirmed: that id (jvfPVHKcTMM3BeGB) is WF5's own id in its JSON, so WF1-WF4 all report failures to WF5

## Known limits of the error handler (WF5)

- WF5 itself has no error workflow. If WF5 fails, nobody is alerted.
- The ALERT email and WF4's report both use the same Gmail credential. If that credential expires, no email alerts arrive. The Errors sheet row is written in parallel, so check the **Errors** sheet regularly as a backup.
- [ ] Exact trial end date
- [ ] Add a screenshot or two as evidence (alert email, Errors sheet row)
