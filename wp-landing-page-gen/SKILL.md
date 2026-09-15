---
name: wp-landing-page-gen
description: Create professional B2B English WordPress landing page HTML/CSS for Southern Machinery products. Use when the user invokes $wp-landing-page-gen, WP_Landing_Page_Gen, or asks to generate a WordPress landing page/page section for SMT, THT, auto insertion, pick-and-place, reflow oven, wave soldering, board handling, or PCB assembly equipment. The skill first guides the user to provide verified product technical parameters such as CPH, temperature zones, PCB size, machine dimensions, labor-saving claims, and support details, then drafts a technology-focused page emphasizing high efficiency, cost-effectiveness, and global technical support and spare-parts supply since 2011.
---

# WP Landing Page Gen

## Core Workflow

1. Normalize the request as a Southern Machinery WordPress landing page task.
2. Ask for missing product data before writing parameter-specific claims. Keep the question concise and practical.
3. Use only user-provided values or verified local catalog/manual values for specifications such as CPH, temperature zones, PCB size, dimensions, power, accuracy, labor replacement, ROI, delivery time, warranty, and price.
4. If a specification is missing, use neutral placeholder copy such as `To be confirmed` in tables or omit the claim from marketing copy.
5. Generate customer-facing copy in professional B2B English.
6. Output WordPress-friendly HTML/CSS that can be pasted into a Custom HTML block, theme page template, Elementor HTML widget, or static page draft.
7. Mention that all technical data should be reviewed before publishing when the page includes specifications.

## Intake Questions

When the user invokes this skill without enough details, ask for the most relevant items:

```text
Please share the product name/model and any verified technical parameters you want included, such as CPH/output, temperature zones, PCB size range, component range, machine dimensions, power, labor-saving data, target application, and optional CTA/contact details.
```

For a reflow oven, prioritize temperature zones, heating length, conveyor width, PCB width, power, and nitrogen option if applicable.

For an auto insertion or pick-and-place machine, prioritize CPH, component type/range, PCB size, feeder capacity, insertion/mounting accuracy, labor-saving data, and application industry.

For board handling equipment, prioritize PCB size, magazine capacity, transfer height, cycle time, dimensions, and line compatibility.

If the user provides partial data and asks to proceed, generate the page with explicit placeholders only in tables, not inflated narrative claims.

## Required Messaging

Make the page communicate these points naturally:

- `High-efficiency`: Use verified output, automation speed, reduced manual handling, faster line changeover, or stable continuous production.
- `Cost-effective`: Emphasize practical ROI, labor reduction, reduced rework, modular line integration, or strong value for EMS factories without inventing numbers.
- `Global support since 2011`: State that Southern Machinery has provided PCB assembly automation, technical support, and spare-parts supply to global customers since 2011.
- `Automation Partner, Not Supplier`: Position Southern Machinery as a solution partner for SMT/THT line planning, installation guidance, operator training, and after-sales support.

Use a confident but factual tone. Avoid hype such as `world-leading`, `guaranteed ROI`, `best price`, or unsupported superlatives.

## Page Architecture

Generate a complete sectioned page with this structure unless the user requests otherwise:

1. Hero section: product model/name, one-line B2B value proposition, two CTAs.
2. Trust strip: since 2011, Shenzhen manufacturing, global EMS customers, spare-parts supply.
3. Product overview: short explanation of the application and target factory profile.
4. Key advantages: efficiency, cost-effectiveness, production stability, service/support.
5. Technical specifications table: include provided parameters and mark missing values as `To be confirmed`.
6. Application scenarios: EMS, LED lighting, consumer electronics, industrial control, automotive electronics, or user-provided industries.
7. Line integration/support: sampling, technical consultation, installation training, after-sales guidance, spare parts.
8. CTA section: ask the visitor to send PCB/product details for a recommended solution.

## WordPress HTML/CSS Rules

Deliver a single self-contained snippet:

- Wrap content in one root container with a unique class such as `.sm-wp-landing`.
- Put CSS inside a `<style>` tag at the top of the snippet.
- Scope all selectors under the root class to avoid theme conflicts.
- Use semantic sections, responsive CSS grid/flex layouts, and accessible button/link text.
- Use a B2B technology style: clean layout, strong contrast, restrained blue/green/neutral accents, subtle borders, specification tables, and practical CTA blocks.
- Avoid JavaScript unless the user explicitly requests interactive behavior.
- Avoid external dependencies, remote fonts, tracking scripts, or plugin-specific shortcodes unless requested.
- Keep copy suitable for WordPress pages: polished, concise, and ready for human review.

## Output Format

Provide the result in this order:

1. A short note listing assumptions and any missing parameters.
2. The complete HTML/CSS snippet in a fenced `html` code block.
3. A short publishing note: review specifications before publishing, then paste into a WordPress Custom HTML block or page builder HTML widget.

## Contact Defaults

Use these Southern Machinery defaults unless the user provides alternatives:

```text
Email: jasonwu@smthelp.com
Website: www.smthelp.com
WhatsApp: +8613602562576
Company: Southern Machinery Co., Ltd.
Location: Shenzhen, China
```
