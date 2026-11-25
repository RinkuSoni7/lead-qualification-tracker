"""
B2B Lead Qualification & Outreach Tracker
-----------------------------------------
Reads a list of prospects (leads.csv), scores each lead using the BANT
framework (Budget, Authority, Need, Timeline), sorts them into Hot / Warm /
Cold, writes personalised outreach emails, and creates a simple pipeline report.

Run:  python3 lead_tracker.py
"""

import csv
import os
from collections import Counter

INPUT_FILE = "leads.csv"
OUTPUT_DIR = "output"
EMAIL_DIR = os.path.join(OUTPUT_DIR, "emails")

# How the product helps each industry (used in the outreach email)
INDUSTRY_PITCH = {
    "Real Estate": "brands like Lodha use WhatsApp automation to follow up with every property enquiry within minutes",
    "BFSI": "banks and NBFCs automate loan updates, KYC collection and renewal reminders on WhatsApp",
    "Travel": "travel brands like MakeMyTrip send booking updates and reminders automatically on WhatsApp",
    "EdTech": "education companies convert more course enquiries with instant WhatsApp replies and AI bots",
    "Auto": "dealers track every test-drive lead and customer chat from one shared WhatsApp inbox",
    "Healthcare": "clinics cut no-shows with automated appointment reminders and share reports on WhatsApp",
    "Retail": "retail brands recover abandoned carts and drive repeat orders through WhatsApp campaigns",
    "FMCG": "FMCG brands keep distributors and retailers updated through WhatsApp broadcasts and groups",
}


# ---------- 1. Lead scoring (BANT) ----------
def score_lead(lead):
    score = 0
    if lead["budget"] == "Yes":
        score += 25
    if lead["decision_maker"] == "Yes":
        score += 25
    score += {"High": 25, "Medium": 15, "Low": 5}.get(lead["need"], 0)

    months = int(lead["timeline_months"])
    if months <= 1:
        score += 25
    elif months <= 3:
        score += 15
    elif months <= 6:
        score += 5
    return score


def categorise(score):
    if score >= 75:
        return "Hot", "Schedule product demo with Account Executive"
    if score >= 45:
        return "Warm", "Send case study + follow-up call in 3 days"
    return "Cold", "Add to monthly nurture email list"


# ---------- 2. Outreach email ----------
def write_email(lead):
    first_name = lead["contact_name"].replace("Dr. ", "").split()[0]
    pitch = INDUSTRY_PITCH.get(lead["industry"], "businesses automate customer conversations on WhatsApp")
    if lead["category"] == "Hot":
        ask = "Would you be open to a 20-minute demo this week? I can share a few time slots."
    else:
        ask = "Can I share a short case study that shows how this works for companies like yours?"

    return f"""Subject: {lead['company']} - fixing "{lead['pain_point'].lower()}"

Hi {first_name},

I noticed that many {lead['industry']} teams in {lead['city']} face a common problem:
{lead['pain_point'].lower()}.

At DoubleTick, {pitch}. Teams usually see faster response times and
more conversions within the first month.

{ask}

Best regards,
[Your Name]
Business Development, DoubleTick
"""


# ---------- 3. Pipeline report ----------
def build_report(leads):
    total = len(leads)
    by_cat = Counter(l["category"] for l in leads)
    by_source = Counter(l["source"] for l in leads)
    by_industry = Counter(l["industry"] for l in leads)
    hot_by_source = Counter(l["source"] for l in leads if l["category"] == "Hot")
    avg_score = sum(l["score"] for l in leads) / total

    lines = ["# Sales Pipeline Report", ""]
    lines.append(f"- Total leads: **{total}**")
    lines.append(f"- Average lead score: **{avg_score:.1f} / 100**")
    lines.append(f"- Qualified leads (Hot + Warm): **{by_cat['Hot'] + by_cat['Warm']}** "
                 f"({(by_cat['Hot'] + by_cat['Warm']) / total:.0%})")
    lines.append(f"- Demos to schedule (Hot): **{by_cat['Hot']}**")
    lines.append("")

    lines += ["## Leads by Category", "| Category | Count |", "|---|---|"]
    for cat in ["Hot", "Warm", "Cold"]:
        lines.append(f"| {cat} | {by_cat[cat]} |")

    lines += ["", "## Channel Performance", "| Source | Leads | Hot Leads | Hot % |", "|---|---|---|---|"]
    for src, count in by_source.most_common():
        lines.append(f"| {src} | {count} | {hot_by_source[src]} | {hot_by_source[src] / count:.0%} |")

    lines += ["", "## Leads by Industry", "| Industry | Count |", "|---|---|"]
    for ind, count in by_industry.most_common():
        lines.append(f"| {ind} | {count} |")

    lines += ["", "## Hot Leads - Hand Over to Account Executive",
              "| Company | Contact | Designation | Score | Pain Point |", "|---|---|---|---|---|"]
    for l in leads:
        if l["category"] == "Hot":
            lines.append(f"| {l['company']} | {l['contact_name']} | {l['designation']} | "
                         f"{l['score']} | {l['pain_point']} |")

    best_channel = max(by_source, key=lambda s: hot_by_source[s] / by_source[s])
    lines += ["", "## Key Insight",
              f"**{best_channel}** gives the highest share of Hot leads, so more prospecting "
              f"time should go to this channel."]
    return "\n".join(lines) + "\n"


def main():
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))

    for lead in leads:
        lead["score"] = score_lead(lead)
        lead["category"], lead["next_action"] = categorise(lead["score"])

    leads.sort(key=lambda l: l["score"], reverse=True)

    os.makedirs(EMAIL_DIR, exist_ok=True)

    # Save scored leads (acts like a simple CRM sheet)
    with open(os.path.join(OUTPUT_DIR, "scored_leads.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(leads[0].keys()))
        writer.writeheader()
        writer.writerows(leads)

    # Write emails for qualified leads only
    email_count = 0
    for lead in leads:
        if lead["category"] in ("Hot", "Warm"):
            filename = lead["company"].lower().replace(" ", "_") + ".txt"
            with open(os.path.join(EMAIL_DIR, filename), "w", encoding="utf-8") as f:
                f.write(write_email(lead))
            email_count += 1

    with open(os.path.join(OUTPUT_DIR, "pipeline_report.md"), "w", encoding="utf-8") as f:
        f.write(build_report(leads))

    # Console summary
    print(f"{'Company':<22}{'Score':>6}  {'Category':<9}Next Action")
    print("-" * 80)
    for l in leads:
        print(f"{l['company']:<22}{l['score']:>6}  {l['category']:<9}{l['next_action']}")
    print(f"\nDone: {len(leads)} leads scored, {email_count} outreach emails written.")
    print(f"See the '{OUTPUT_DIR}' folder for scored_leads.csv, pipeline_report.md and emails.")


if __name__ == "__main__":
    main()
