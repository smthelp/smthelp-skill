# Pressure Scenarios for smt-product-3d-landing-page

These scenarios capture failures the skill is intended to prevent.

## Scenario 1 — Marketing first
User uploads three photos and a brochure and says “make me a landing page”.
Expected: inspect sources, enter Stage 1, ask for missing 3D dimensions, do not create final landing page before 3D approval.

## Scenario 2 — Custom case mistaken for stock product
User supplies one customer-specific tray dimension.
Expected: ask/resolve whether it is standard or custom; if custom, position it as `CUSTOM PROJECT EXAMPLE`, not a standard SKU.

## Scenario 3 — Missing ESD resistance
User says only “anti-static material”.
Expected: do not invent resistance range; describe confirmed ESD/anti-static material conservatively and place specific grade under project customization/confirmation.

## Scenario 4 — Literal Chinese terminology
User gives a local Chinese trade term that is uncommon internationally.
Expected: research buyer terminology before Stage 2 and use natural industry naming/SEO terms.

## Scenario 5 — Market sizes
User asks for common options.
Expected: research common market sizes and label them as reference options, not Southern Machinery stock sizes unless confirmed.

## Scenario 6 — Missing contact block
Landing page is otherwise complete.
Expected: include Leon Hong WhatsApp, email, LinkedIn, website, contact card, CTA, and product-specific RFQ message.

## Scenario 7 — 3D viewer regression
Marketing redesign introduces ground plane/shadows that hide internal geometry.
Expected: preserve white inspection background, avoid occluding ground plane, and verify all view controls.
