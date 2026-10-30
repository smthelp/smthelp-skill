# Email Deliverability Guide

## Why Deliverability Matters

You can write the perfect email but if it lands in spam or doesn't 
land at all, it doesn't matter. Deliverability = getting the email 
to the inbox, not spam.

---

## Core Deliverability Rules

### 1. Warm Up New Inboxes (Non-Negotiable)

**Never send cold email from a fresh inbox.**

Warmup protocol:
- Week 1: 5 emails/day to personal contacts (people who know you)
- Week 2: 10 emails/day, mix of warm and personal contacts
- Week 3: 20 emails/day
- Week 4: 30 emails/day (this is the maximum per inbox)
- Week 5+: Full campaign volume

**What happens without warmup:** New inbox → sends 100 cold emails → 
Gmail/Outlook flags as spam → all future emails from that inbox 
go to spam. Fix takes 4-8 weeks.

### 2. Domain Strategy

**Use a dedicated sending domain** for cold campaigns — not your main domain.

If your main domain is `smthelp.com`, use a separate domain like:
- `smt-solutions.co`
- `smtautomation.com`
- `smtline.tech`

This protects your main domain reputation if a campaign gets flagged.

**Current setup:** Using `3dsmt.com` and `smthelp.eu` domains for 
sending — these are separate from main business domain.

### 3. Inbox Rotation

Never send all volume from one inbox. Rotate across your 5 accounts:
- `sale@3dsmt.com` (primary)
- `service@3dsmt.com` (technical follow-ups)
- `info@3dsmt.com` (info/lead magnet campaigns)
- `support@3dsmt.com` (support-focused outreach)
- `info@smthelp.eu` (Europe campaigns)

Max per inbox per day: **30 emails**

### 4. Volume Ramp

| Week | Emails/Day/Account | Total/Day |
|------|-------------------|-----------|
| 1-2 | 5-10 | 25-50 |
| 3-4 | 15-20 | 75-100 |
| 5-8 | 25-30 | 125-150 |
| 9+ | 30 (max) | 150 |

### 5. List Hygiene

**Before any campaign:**
- Remove bounces immediately (do not re-send to bounced addresses)
- Verify emails with a verifier service (MillionVerifier, ZeroBounce)
- Remove role-based emails (info@, admin@, hello@)
- Remove unsubscribes (obvious, but track them)

### 6. Content Rules

**Gmail spam triggers (avoid these):**
- Em dashes (—) — use periods or commas instead
- ALL CAPS in subject or body
- Excessive punctuation (!!!, ???, $$$)
- "Free", "Act now", "Limited time" — obvious spam words
- Too many links (1 link max in cold email)
- "Click here" — use descriptive CTA text instead
- HTML heavy emails — plain text is safer for cold

**Subject line rules:**
- Keep under 50 characters
- No false urgency
- Personalization `[{{company}}]` helps inbox placement
- Avoid all caps and excessive punctuation

### 7. Authentication (Set Up Once)

Ensure your sending domains have:
- **SPF** (Sender Policy Framework) — authorizes your servers to send
- **DKIM** (DomainKeys Identified Mail) — cryptographically signs emails
- **DMARC** (Domain-based Message Authentication) — tells receivers what to do with unauthenticated emails

If using Zapmail or similar inbox providers, these are typically set up automatically.

### 8. Sending Time

**Best time to send:** 8:00 AM - 10:00 AM recipient local time

This maximizes the chance the email is seen when the recipient 
checks email first thing in the morning.

**Time zone reference:**
| Market | Time Zone | Send At |
|--------|-----------|---------|
| Mexico | CST (UTC-6) | 8:00 AM Mexico City |
| Vietnam | ICT (UTC+7) | 8:00 AM Hanoi/HCMC |
| India | IST (UTC+5:30) | 9:00 AM IST |
| Europe (Central) | CET (UTC+1) | 8:00 AM Frankfurt/Warsaw |
| Europe (Eastern) | EET (UTC+2) | 8:00 AM Bucharest/Kiev |

---

## Deliverability Monitoring

### What to Watch
- **Bounce rate:** Should stay under 3%. Above 5% = problem.
- **Spam complaint rate:** Should stay under 0.1%. Above 0.3% = risk.
- **Reply rate:** Your real metric (target: 3-8% positive reply rate)
- **Open rate:** Soft signal (not reliable as Gmail strips tracking pixels)

### If Deliverability Drops
1. Stop sending immediately
2. Check for bounces (remove bounced addresses)
3. Check spam complaint rate
4. Pause for 48 hours, then resume at 50% volume
5. If problem persists, investigate content (run through spam word checker)

---

## Quick Deliverability Checklist

Before any campaign launch:
- [ ] Inboxes warmed up minimum 2 weeks
- [ ] SPF/DKIM/DMARC configured on sending domains
- [ ] Email list verified and cleaned
- [ ] Role-based emails removed
- [ ] Bounced addresses suppressed
- [ ] Content scanned for spam words
- [ ] Test email sent to self (Gmail, Outlook, Yahoo)
- [ ] Sending volume ramped correctly (not cold start at high volume)
