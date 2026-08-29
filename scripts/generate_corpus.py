"""Generate 33 synthetic NovaTel corpus documents."""

from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent.parent / "data" / "corpus"

DOCUMENTS = {
    "novatel_start_lite.md": """# NovaTel Start Lite Plan

## Overview
NovaTel Start Lite is an entry-level mobile plan for light users.

## Pricing

### Monthly Subscription
**Clause ID:** PLAN-001-PRICE-01
**Section:** Pricing
Monthly price: $15.00 per month (excluding taxes and fees).

### Activation Fee
**Clause ID:** PLAN-001-FEE-01
**Section:** Pricing
One-time activation fee: $10.00 for new lines.

## Data Allowance

### Included Data
**Clause ID:** PLAN-001-DATA-01
**Section:** Data
Included data: 10 GB per month at full speed.

### Post-Allowance Speed
**Clause ID:** PLAN-001-DATA-02
**Section:** Data
After 10 GB, speeds are reduced to 512 Kbps for the remainder of the billing cycle.
""",
    "novatel_move_plus.md": """# NovaTel Move Plus Plan

## Overview
NovaTel Move Plus is a mid-tier mobile plan for active users who need more data.

## Pricing

### Monthly Subscription
**Clause ID:** PLAN-002-PRICE-01
**Section:** Pricing
Monthly price: $25.00 per month (excluding taxes).

## Data Allowance

### Included Data
**Clause ID:** PLAN-002-DATA-01
**Section:** Data
Included data: 35 GB per month at full speed.

### Post-Allowance Speed
**Clause ID:** PLAN-002-DATA-02
**Section:** Data
After 35 GB consumption in a billing cycle, speeds are reduced to 1 Mbps for the remainder of the cycle.

## Roaming Inclusion
**Clause ID:** PLAN-002-ROAM-01
**Section:** Roaming
EU roaming is charged per the EU Roaming Tariff document; not included in base plan.
""",
    "novatel_premium_unlimited.md": """# NovaTel Premium Unlimited Plan

## Overview
NovaTel Premium Unlimited offers unlimited data with fair-usage protections.

## Pricing
**Clause ID:** PLAN-003-PRICE-01
**Section:** Pricing
Monthly price: $55.00 per month.

## Data
**Clause ID:** PLAN-003-DATA-01
**Section:** Data
Unlimited data subject to fair-usage policy. See Premium Fair Usage Policy document.

## Premium Benefits
**Clause ID:** PLAN-003-BENEFIT-01
**Section:** Benefits
Includes priority network access and 100 GB hotspot allowance.
""",
    "novatel_family_share.md": """# NovaTel Family Share Plan

## Overview
Share data across up to 4 lines on one account.

## Pricing
**Clause ID:** PLAN-004-PRICE-01
**Section:** Pricing
Base monthly price: $45.00 for primary line plus $15.00 per additional line.

## Shared Data
**Clause ID:** PLAN-004-DATA-01
**Section:** Data
Shared pool: 80 GB per month across all lines.
""",
    "novatel_student_plan.md": """# NovaTel Student Plan

## Overview
Discounted plan for verified students.

## Pricing
**Clause ID:** PLAN-005-PRICE-01
**Section:** Pricing
Monthly price: $18.00 with valid student ID.

## Data
**Clause ID:** PLAN-005-DATA-01
**Section:** Data
Included data: 20 GB per month.
""",
    "novatel_senior_plan.md": """# NovaTel Senior Plan

## Overview
Simplified plan for customers aged 65 and over.

## Pricing
**Clause ID:** PLAN-006-PRICE-01
**Section:** Pricing
Monthly price: $12.00 per month.

## Data
**Clause ID:** PLAN-006-DATA-01
**Section:** Data
Included data: 5 GB per month with unlimited 2G fallback.
""",
    "novatel_business_basic.md": """# NovaTel Business Basic

## Overview
Small business mobile plan with pooled minutes.

## Pricing
**Clause ID:** PLAN-007-PRICE-01
**Section:** Pricing
Monthly price: $30.00 per line (minimum 2 lines).

## Data
**Clause ID:** PLAN-007-DATA-01
**Section:** Data
Included data: 25 GB per line per month.
""",
    "novatel_business_pro.md": """# NovaTel Business Pro

## Overview
Advanced business plan with SLA support.

## Pricing
**Clause ID:** PLAN-008-PRICE-01
**Section:** Pricing
Monthly price: $65.00 per line.

## Data
**Clause ID:** PLAN-008-DATA-01
**Section:** Data
Included data: 100 GB per line with priority routing.
""",
    "eu_roaming_tariff.md": """# EU Roaming Tariff

## Overview
Roaming charges for European Union destinations.

## Voice Calls
**Clause ID:** ROAM-EU-VOICE-01
**Section:** EU Roaming
Outgoing voice calls in EU: $0.15 per minute.

## SMS
**Clause ID:** ROAM-EU-SMS-01
**Section:** EU Roaming
Outgoing SMS in EU: $0.05 per message.

## Data
**Clause ID:** ROAM-EU-DATA-01
**Section:** EU Roaming
Data usage in EU: $2.50 per GB after included allowance.

## Fair Usage
**Clause ID:** ROAM-EU-FAIR-01
**Section:** EU Roaming
Extended roaming beyond 30 days may incur surcharges per fair-usage rules.
""",
    "uk_roaming_tariff.md": """# UK Roaming Tariff

## Overview
Roaming charges for United Kingdom.

## Voice
**Clause ID:** ROAM-UK-VOICE-01
**Section:** UK Roaming
Outgoing voice: $0.20 per minute.

## Data
**Clause ID:** ROAM-UK-DATA-01
**Section:** UK Roaming
Data: $3.00 per GB.
""",
    "us_roaming_tariff.md": """# US Roaming Tariff

## Overview
Roaming charges for United States.

## Voice
**Clause ID:** ROAM-US-VOICE-01
**Section:** US Roaming
Outgoing voice: $0.25 per minute.

## Data
**Clause ID:** ROAM-US-DATA-01
**Section:** US Roaming
Data: $5.00 per GB.
""",
    "asia_roaming_tariff.md": """# Asia Roaming Tariff

## Overview
Roaming charges for select Asian destinations.

## Voice
**Clause ID:** ROAM-ASIA-VOICE-01
**Section:** Asia Roaming
Outgoing voice: $0.35 per minute.

## Data
**Clause ID:** ROAM-ASIA-DATA-01
**Section:** Asia Roaming
Data: $6.00 per GB.
""",
    "fair_usage_policy.md": """# NovaTel Fair Usage Policy

## Overview
General fair-usage rules for unlimited and high-data plans.

## Standard Limit
**Clause ID:** FUP-GEN-01
**Section:** Fair Usage
Standard plans: no specific fair-usage cap beyond stated data limits.

## Monitoring
**Clause ID:** FUP-GEN-02
**Section:** Fair Usage
NovaTel may throttle abusive usage patterns affecting network quality.
""",
    "premium_fair_usage.md": """# Premium Fair Usage Policy

## Overview
Fair-usage limits for NovaTel Premium Unlimited plan.

## Premium Limit
**Clause ID:** FUP-PREM-01
**Section:** Premium Fair Usage
Fair-usage limit for premium plan: 500 GB per month at full speed.

## After Limit
**Clause ID:** FUP-PREM-02
**Section:** Premium Fair Usage
Beyond 500 GB, speeds reduced to 3 Mbps until next billing cycle.
""",
    "sms_addon_catalog.md": """# SMS Add-On Catalog

## Overview
Optional SMS bundles.

## 100 SMS Pack
**Clause ID:** ADDON-SMS-100-01
**Section:** SMS Add-Ons
100 domestic SMS: $5.00 per month.

## 500 SMS Pack
**Clause ID:** ADDON-SMS-500-01
**Section:** SMS Add-Ons
500 domestic SMS: $15.00 per month.
""",
    "data_addon_catalog.md": """# Data Add-On Catalog

## Overview
Extra data packs for all mobile plans.

## 5 GB Pack
**Clause ID:** ADDON-DATA-5GB-01
**Section:** Data Add-Ons
Additional 5 GB: $10.00 (one-time, valid 30 days).

## 20 GB Pack
**Clause ID:** ADDON-DATA-20GB-01
**Section:** Data Add-Ons
Additional 20 GB: $25.00 (one-time, valid 30 days).
""",
    "international_calling.md": """# International Calling Tariff

## Overview
Rates for international calls from home country.

## Europe
**Clause ID:** INTL-EU-01
**Section:** International Calling
Calls to EU landlines: $0.10 per minute.

## North America
**Clause ID:** INTL-NA-01
**Section:** International Calling
Calls to US/Canada: $0.08 per minute.
""",
    "terms_and_conditions.md": """# NovaTel Terms and Conditions

## Overview
General terms of service for all NovaTel customers.

## Contract Length
**Clause ID:** TNC-CONTRACT-01
**Section:** Contract
Minimum contract period: 12 months unless stated otherwise.

## Billing
**Clause ID:** TNC-BILLING-01
**Section:** Billing
Bills issued monthly in advance. Late payment fee: $5.00.
""",
    "privacy_policy.md": """# NovaTel Privacy Policy

## Overview
How NovaTel handles customer data.

## Data Collection
**Clause ID:** PRIV-COLLECT-01
**Section:** Privacy
We collect account, usage, and billing data for service delivery.

## Retention
**Clause ID:** PRIV-RETAIN-01
**Section:** Privacy
Usage records retained for 24 months.
""",
    "broadband_home_lite.md": """# NovaTel Home Lite Broadband

## Overview
Entry-level home broadband service.

## Pricing
**Clause ID:** BB-001-PRICE-01
**Section:** Broadband Pricing
Monthly price: $35.00.

## Speed
**Clause ID:** BB-001-SPEED-01
**Section:** Broadband Speed
Download speed: up to 50 Mbps.
""",
    "broadband_home_max.md": """# NovaTel Home Max Broadband

## Overview
High-speed fibre broadband for households.

## Pricing
**Clause ID:** BB-002-PRICE-01
**Section:** Broadband Pricing
Monthly price: $60.00.

## Speed
**Clause ID:** BB-002-SPEED-01
**Section:** Broadband Speed
Download speed: up to 500 Mbps.
""",
    "fibre_upgrade_policy.md": """# Fibre Upgrade Policy

## Overview
Rules for upgrading to fibre service.

## Eligibility
**Clause ID:** FIBRE-ELIG-01
**Section:** Fibre Upgrade
Fibre available only in covered postcodes listed on novaTel coverage map.

## Installation Fee
**Clause ID:** FIBRE-INSTALL-01
**Section:** Fibre Upgrade
Standard installation: $0.00 for 24-month contracts.
""",
    "porting_policy.md": """# Number Porting Policy

## Overview
Keep your number when switching to NovaTel.

## Processing Time
**Clause ID:** PORT-TIME-01
**Section:** Porting
Porting completes within 1-3 business days.

## Fee
**Clause ID:** PORT-FEE-01
**Section:** Porting
Number porting is free of charge.
""",
    "cancellation_policy.md": """# Cancellation Policy

## Overview
How to cancel NovaTel services.

## Notice Period
**Clause ID:** CANCEL-NOTICE-01
**Section:** Cancellation
30 days written notice required for business plans.

## Early Termination
**Clause ID:** CANCEL-ETF-01
**Section:** Cancellation
Early termination fee: remaining contract value up to $200.
""",
    "payment_terms.md": """# Payment Terms

## Overview
Accepted payment methods and schedules.

## Methods
**Clause ID:** PAY-METHOD-01
**Section:** Payment
Accepted: credit card, direct debit, bank transfer.

## Due Date
**Clause ID:** PAY-DUE-01
**Section:** Payment
Payment due within 14 days of invoice date.
""",
    "device_installment.md": """# Device Installment Plan

## Overview
Pay for devices in monthly installments.

## Terms
**Clause ID:** DEVICE-INST-01
**Section:** Device Installment
Installment period: 24 months at 0% APR when bundled with plan.

## Early Payoff
**Clause ID:** DEVICE-PAYOFF-01
**Section:** Device Installment
Remaining balance due in full upon early plan cancellation.
""",
    "loyalty_rewards.md": """# Loyalty Rewards Program

## Overview
Earn points on monthly bills.

## Earning Rate
**Clause ID:** LOYAL-EARN-01
**Section:** Loyalty
Earn 1 point per $1 spent on eligible charges.

## Redemption
**Clause ID:** LOYAL-REDEEM-01
**Section:** Loyalty
100 points = $1 credit toward bill.
""",
    "emergency_services.md": """# Emergency Services

## Overview
Access to emergency numbers.

## Availability
**Clause ID:** EMERG-AVAIL-01
**Section:** Emergency
Emergency calls to 112 and 999 are free on all active plans.

## Location
**Clause ID:** EMERG-LOC-01
**Section:** Emergency
Location data shared with emergency services when required by law.
""",
    "network_coverage.md": """# Network Coverage Policy

## Overview
Coverage expectations and limitations.

## Indoor Coverage
**Clause ID:** COV-INDOOR-01
**Section:** Coverage
Indoor coverage not guaranteed; depends on building materials.

## Rural Areas
**Clause ID:** COV-RURAL-01
**Section:** Coverage
Rural coverage maps updated quarterly on novaTel website.
""",
    "5g_access_policy.md": """# 5G Access Policy

## Overview
5G network access by plan type.

## Premium 5G
**Clause ID:** 5G-PREM-01
**Section:** 5G Access
Premium Unlimited includes full 5G access where available.

## Standard 5G
**Clause ID:** 5G-STD-01
**Section:** 5G Access
Move Plus and above include 5G at no extra charge.
""",
    "voicemail_tariff.md": """# Voicemail Tariff

## Overview
Voicemail service charges.

## Basic Voicemail
**Clause ID:** VM-BASIC-01
**Section:** Voicemail
Basic voicemail: $2.00 per month.

## Visual Voicemail
**Clause ID:** VM-VISUAL-01
**Section:** Voicemail
Visual voicemail: $4.00 per month on supported devices.
""",
    "premium_support_addon.md": """# Premium Support Add-On

## Overview
Priority customer support package.

## Pricing
**Clause ID:** SUPPORT-PREM-01
**Section:** Premium Support
Premium support: $8.00 per month per account.

## SLA
**Clause ID:** SUPPORT-SLA-01
**Section:** Premium Support
Guaranteed callback within 2 hours for priority tickets.
""",
    "travel_pass_catalog.md": """# Travel Pass Catalog

## Overview
Daily roaming passes for frequent travelers.

## Europe Pass
**Clause ID:** TRAVEL-EU-01
**Section:** Travel Pass
Europe daily pass: $5.00 per day includes 500 MB and 30 minutes.

## Global Pass
**Clause ID:** TRAVEL-GLOBAL-01
**Section:** Travel Pass
Global daily pass: $12.00 per day includes 200 MB in 50 countries.
""",
}


def main() -> None:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    for filename, content in DOCUMENTS.items():
        path = CORPUS_DIR / filename
        path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Generated {len(DOCUMENTS)} documents in {CORPUS_DIR}")


if __name__ == "__main__":
    main()
