# Intake And Planning

## Contents

1. Discovery sequence
2. Required materials
3. Scope and acceptance criteria
4. Information architecture
5. Content planning
6. Access and security

## 1. Discovery Sequence

Start with files and evidence before asking broad questions.

1. Read repository instructions and current documentation.
2. Inventory logos, catalogs, price lists, product spreadsheets, product images, factory images, certificates, videos, and existing copy.
3. Inspect any existing site and reference sites page by page.
4. Identify the business model: catalog inquiry, quote-led projects, ecommerce, distributor acquisition, or mixed.
5. Identify the owner of the domain, DNS, VPS, WordPress, email, analytics, and advertising accounts.
6. Ask only for remaining decisions that materially change architecture, content, or launch safety.

Maintain an assumption log with `assumption`, `reason`, `risk`, `owner`, and `confirmation status`.

## 2. Required Materials

### Business

- Brand name and legal company name
- One-sentence positioning
- Products and priority categories
- Target countries, buyer types, and language
- OEM, ODM, custom, engineering, quality, export, and logistics capabilities
- Verified years, countries, clients, projects, exhibitions, certifications, and other claims
- Factory address and map location
- Sales email, telephone, WhatsApp, and inquiry recipient

### Visual

- Vector or high-resolution logo
- Brand colors or approved visual references
- Product hero images and galleries
- Factory exterior, workshop, assembly, inspection, packaging, warehouse, team, showroom, and exhibitions
- Certificates with approved public information
- Project images with usage rights
- Video platform URLs and thumbnails

### Product

- Stable model or SKU
- English title
- Category and subcategory
- Short description and full description
- Dimensions, power, voltage, materials, finish, crystal type, light source, installation, lead time, MOQ, packaging, warranty, and customization
- For equipment catalogs: model, equipment type, line role, board size range, component class, speed or capacity, power and air requirements, integration notes, and MOQ/lead time where available
- Main image and optional gallery files
- SEO title, description, focus phrase, and image alt text when available

### Technical

- Domain and registrar
- DNS provider and access status
- VPS provider, region, operating system, CPU, RAM, storage, IP, SSH port, and access method
- WordPress installation status and administrator access status
- Email provider and required DNS records
- Analytics, Search Console, Tag Manager, advertising, and translation accounts

Never collect secrets in the intake document. Record only whether access is available and how it will be transferred securely.

## 3. Scope And Acceptance Criteria

Define launch scope as a list of routes, content types, integrations, and operational workflows. Mark each item `launch`, `phase 2`, or `out of scope`.

Suggested launch acceptance criteria:

- All agreed routes exist and are linked from navigation or intentional internal links.
- Products have unique URLs and correct categories.
- Editors can create, update, unpublish, and remove products without code changes.
- Forms deliver to the intended mailbox and identify the referring product or page.
- Mobile and desktop layouts show no overlap or horizontal overflow.
- Core pages expose useful content below the first viewport.
- HTTPS, backups, sitemap, robots, canonical URLs, and metadata work.
- Ownership and renewal responsibilities are documented.

## 4. Information Architecture

Create a route table with:

| Route | Audience intent | Primary content | Primary CTA | Owner |
|---|---|---|---|---|
| Home | Understand supplier quickly | Positioning, products, proof, process | View products / request quote | Marketing |
| Collections | Browse product families | Categories, filters, product cards | Open product | Product team |
| Product | Evaluate a model | Images, specs, options, applications | Request quote / WhatsApp | Product team |
| Custom | Assess engineering ability | Process, inputs, samples, QC | Discuss a project | Sales |
| Projects | Validate application experience | Cases, applications, constraints | Submit project | Sales |
| About | Verify the factory | Story, factory evidence, capabilities | Contact factory | Management |
| News | Build topical authority | Guides, updates, exhibitions | Read / inquire | Marketing |
| Video | View products and production | Embedded videos and summaries | Watch / contact | Marketing |
| Contact | Start an inquiry | Address, contacts, map, form | Send inquiry | Sales |

Avoid empty pages created only to make the menu look larger.

## 5. Content Planning

Write English for international buyers, not as a literal translation of internal Chinese material.

- Lead with buyer decisions: specification, fit, customization, verification, delivery, and next step.
- Use concrete nouns and measurements instead of vague superlatives.
- Put one clear H1 on each page.
- Keep category and product introductions distinct.
- Use supplied facts for proof and mark unknown data for confirmation.
- Use News for articles and company updates; use Video for embedded video posts with searchable text summaries.
- Add internal links based on user intent, not a fixed number of links.

## 6. Access And Security

Use an access matrix:

| System | Owner | Access needed | Transfer method | Rotation needed |
|---|---|---|---|---|
| Domain registrar | Client | DNS or nameserver management | Delegated account | After project if shared |
| DNS provider | Client | Zone edit | Delegated account/token | Yes for temporary token |
| VPS | Client | SSH sudo | SSH key | Remove temporary key |
| WordPress | Client | Administrator | Temporary admin | Remove or downgrade |
| Email | Client | DNS values only | Provider instructions | No mailbox password |

If a credential appears in chat, logs, screenshots, or a committed file, treat it as exposed and recommend rotation.
