# B2B Lead Qualification & Outreach Tracker

A small Python tool that copies the daily work of a Business Development / SDR person:
**find leads → qualify them → write outreach emails → hand the best ones to sales → track the pipeline.**

It is built around a conversational CX / WhatsApp platform (like DoubleTick), with prospects from
BFSI, Real Estate, Travel, EdTech, Healthcare, Auto, Retail and FMCG.

## What it does

1. **Reads prospects** from `leads.csv` (company, contact, industry, lead source, pain point, etc.)
2. **Scores every lead out of 100 using BANT**
   | Factor | Points |
   |---|---|
   | Budget confirmed | 25 |
   | Talking to the decision maker (Authority) | 25 |
   | Need (High / Medium / Low) | 25 / 15 / 5 |
   | Timeline (≤1 month / ≤3 / ≤6) | 25 / 15 / 5 |
3. **Sorts leads** into Hot (75+), Warm (45–74) and Cold (<45), and gives a next action for each:
   - Hot → schedule a product demo with the Account Executive
   - Warm → send a case study and follow up with a call in 3 days
   - Cold → add to the monthly nurture email list
4. **Writes a personalised cold email** for every Hot and Warm lead, based on their industry and pain point
5. **Creates a pipeline report** showing leads by category, how well each channel works
   (LinkedIn, cold call, email, inbound), leads by industry, and the Hot leads to hand to sales

## How to run

You only need Python 3. No extra libraries.

```bash
python3 lead_tracker.py
```

Output (in the `output/` folder):
- `scored_leads.csv` – all leads with score, category and next action (a simple CRM sheet)
- `pipeline_report.md` – the pipeline summary
- `emails/` – one ready-to-send outreach email per qualified lead

## Sample result (16 sample leads)

- 11 of 16 leads qualified (69%); 7 Hot leads ready for a demo
- LinkedIn gave the most Hot leads (67%), cold calling came second (50%)

## Skills shown

Prospecting · Lead qualification (BANT) · Writing cold emails · Pipeline management ·
CRM-style record keeping · Comparing channels · Python · Excel/CSV

> Note: All companies and contacts in `leads.csv` are made up for this demo.
