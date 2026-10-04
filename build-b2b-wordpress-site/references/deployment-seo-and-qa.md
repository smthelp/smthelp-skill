# Deployment, SEO, And QA

## Contents

1. Deployment sequence
2. DNS and email DNS
3. Security and backups
4. SEO and paid traffic readiness
5. Test matrix
6. Launch and maintenance

## 1. Deployment Sequence

1. Record current server, DNS, WordPress, and email state.
2. Create backups before changes.
3. Prepare the server using supported operating system packages.
4. Configure the web server, PHP, database, WordPress salts, file permissions, firewall, and automatic security updates.
5. Deploy the theme and companion plugin to staging or a temporary hostname.
6. Import content and verify editor workflows.
7. Test by temporary hostname or local hosts mapping.
8. Lower DNS TTL when needed.
9. Change only the required web records.
10. Issue TLS certificates and force HTTPS after both hostnames resolve correctly.
11. Verify production and keep rollback artifacts until acceptance.

For small catalog sites, a modest VPS may be sufficient, but size it from expected PHP workers, image processing, plugins, backups, traffic, and database load. Add swap only as a stability aid, not a substitute for sufficient memory.

## 2. DNS And Email DNS

Common web records:

- Apex `A` or `AAAA` to the server
- `www` CNAME to the apex or corresponding address

Do not delete unrelated records. Preserve and verify:

- MX
- SPF TXT
- DKIM TXT or CNAME
- DMARC TXT
- Provider verification records
- ACME challenge records in active use

Cloudflare or another proxy can be added before or after launch. Start DNS-only while validating origin TLS and application behavior, then enable proxy features deliberately.

## 3. Security And Backups

- Disable direct root password login where appropriate after SSH key access is proven.
- Use a non-root sudo account for routine administration.
- Apply least privilege to database and WordPress users.
- Restrict writable directories and protect configuration files.
- Keep WordPress core, themes, and plugins updated through a tested maintenance process.
- Limit login abuse and add MFA for privileged accounts when supported.
- Exclude secrets and personal data from logs.
- Back up database, uploads, theme, plugin, and critical server configuration.
- Keep at least one off-server copy.
- Test a restore; an untested backup is not a verified recovery plan.

## 4. SEO And Paid Traffic Readiness

### Keyword Mapping

Assign a primary intent and supporting phrases to each page. Category pages target category searches, product pages target specific models and attributes, service pages target custom or manufacturing intent, and articles answer buying or specification questions.

Avoid making every page target the same broad phrase. This creates internal competition and thin relevance.

### On-Page Requirements

- Unique title and meta description
- One clear H1
- Useful opening copy
- Descriptive URL
- Internal links and breadcrumbs
- Relevant alt text
- Canonical URL
- Indexability decision
- Appropriate structured data

### Technical Requirements

- XML sitemap
- Robots policy
- HTTPS and one preferred hostname
- Clean redirects with no loops
- Correct status codes
- Mobile usability
- Reasonable Core Web Vitals
- Search Console and analytics ownership
- Conversion events for successful inquiries, calls, WhatsApp clicks, and catalog downloads as agreed

### Google Ads

Before sending paid traffic, verify landing-page message match, mobile speed, form delivery, thank-you or success tracking, consent requirements, contact accuracy, and campaign URL persistence through language or redirect behavior.

## 5. Test Matrix

### Functional

- Every navigation and footer link
- Dropdown and mobile menus
- Search, filters, pagination, and breadcrumbs
- Unique product card links
- Forms and error states
- WhatsApp, email, telephone, map, video, and download links
- WordPress create/edit/unpublish workflows

### Visual

- 360px narrow mobile
- Common mobile width
- Tablet portrait and landscape
- Laptop
- Standard desktop
- Wide desktop

Check text fitting, image framing, centering, grid consistency, blank space, fixed controls, sticky headers, and plugin widgets.

### Technical

- HTTP to HTTPS
- Apex and `www` normalization
- 404 page
- Sitemap and robots
- Canonicals and metadata
- Structured data validation
- Cache hit and bypass behavior
- Image loading after scroll
- Console errors and failed network requests
- Backup completion and restore notes

### Content

- Company and contact accuracy
- Consistent English terminology
- No placeholder text or competitor names
- Claims supported by owner confirmation
- Correct product specifications and categories
- Licensed or owned media

## 6. Launch And Maintenance

Launch only after a signed or recorded acceptance checklist. Immediately after DNS cutover, repeat the production smoke test from an uncached network and mobile device.

Suggested maintenance cadence:

- Daily: automated backups and uptime checks
- Weekly: form delivery and security review
- Monthly: updates, broken links, performance, Search Console, and backup restore sample
- Quarterly: content freshness, conversions, plugin inventory, user access, and SEO mapping
- Annually: domain, VPS, certificates, email, plugin licenses, privacy text, and ownership review

Keep a change log for production deployments, content imports, plugin changes, DNS changes, and restore events.
