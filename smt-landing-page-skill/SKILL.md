---
name: smt-landing-page-skill
description: Create evidence-bound, single-file Southern Machinery landing pages for global SMT, THT, PCB assembly automation, feeder, board-handling, and factory-automation marketing.
---

# Southern Machinery Landing Page Skill

Use this Skill when a user asks for a Southern Machinery, SMThelp, or SMThelp.com B2B landing page, product page, campaign page, or sales-support microsite. The output is a directly-openable, single HTML file written in native HTML, CSS, and JavaScript.

Southern Machinery, SMThelp, and SMThelp.com refer to the same company. Taozi is a Southern Machinery sub-brand for solder robots and glue dispensing machines. Do not represent competitor brands or compatible third-party equipment as Southern Machinery products.

## Deliverable Contract

Create one descriptive `.html` file. It must work when double-clicked from a local filesystem:

- Put every HTML, CSS, and JavaScript block in the one file.
- Use no framework, bundler, package manager, build step, or module import.
- YouTube embeds may use `https://www.youtube-nocookie.com/embed/...`; product and logo images may use verified HTTPS URLs from `ph.smthelp.com`.
- Do not add trackers, analytics, form submissions, credentials, local absolute paths, or inaccessible dependencies.
- Use a clean `<!doctype html>`, UTF-8 meta tag, viewport meta tag, one meaningful `h1`, semantic landmarks, responsive layouts, keyboard-accessible controls, and `prefers-reduced-motion` behavior.

## Evidence Before Copy

1. Identify the intended channel, customer role, product or process, and primary CTA.
2. Use current Southern Machinery catalog/spec/manual/approved brand sources as the factual authority. A photo, filename, previous marketing page, social graphic, or video title is not proof of a specification.
3. Verify every model name, parameter, certification, price, capacity, ROI, delivery statement, compatibility claim, or customer claim. Omit unsupported claims or label them `To be confirmed with Southern Machinery engineering/sales`.
4. Use the product image library only for image matching. Verify that the selected image visibly matches the product/topic before placing it on the page.

Ask only the smallest useful set of questions when information is missing: application, monthly/shift volume, PCB size and component class, automation level, then inspection/traceability or special process needs.

## Required Southern Machinery Shell

Every new or materially revised page must include the following.

### Header Logo

Place this official Logo in the upper-left header with a descriptive alt text. It must link to the homepage or page root, have a constrained responsive height, and remain visible on narrow screens.

```html
<a class="brand" href="https://www.smthelp.com/" aria-label="Southern Machinery home">
  <img src="https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png" alt="Southern Machinery">
</a>
```

Use the approved brand colors as restrained accents: green `#90C641` and teal `#0AA5A5`. Maintain readable contrast; do not infer that a brand book's unsupported commercial claims are product facts.

### Footer CTA

Include this footer resource and contact block with `target="_blank" rel="noopener noreferrer"` on external links. Use an actual `mailto:` link for the email address.

```html
<nav aria-label="Southern Machinery social links">
  <a href="https://www.linkedin.com/company/smtmachine" target="_blank" rel="noopener noreferrer">LinkedIn Company Page</a>
  <a href="https://cn.linkedin.com/in/smtsupplier" target="_blank" rel="noopener noreferrer">LinkedIn Profile</a>
  <a href="https://twitter.com/smtspecialist" target="_blank" rel="noopener noreferrer">Twitter</a>
  <a href="https://www.facebook.com/autoinsertion" target="_blank" rel="noopener noreferrer">Facebook</a>
  <a href="https://www.youtube.com/c/Smthelping" target="_blank" rel="noopener noreferrer">YouTube Channel</a>
</nav>
<p>Browse our machine catalog at <a href="https://file.autoinsertion.com" target="_blank" rel="noopener noreferrer">file.autoinsertion.com</a> and find machine photos at <a href="https://ph.smthelp.com" target="_blank" rel="noopener noreferrer">ph.smthelp.com</a>.</p>
<p>Contact us: <a href="mailto:info@smthelp.com">info@smthelp.com</a></p>
```

### Fixed Support Widget

Embed the following Chatwoot loader verbatim, immediately before `</body>`. Do not add a duplicate custom chat bar. Reserve bottom space in the layout so it does not obscure page content. If an existing Chatwoot widget exists, preserve a single loader only and update it to this configuration.

```html
<script>
  window.chatwootSettings = {"position":"right","type":"standard","launcherTitle":"Southern Machinery Global Support"};
  (function(d,t) {
    var BASE_URL="http://chat.smthelp.com";
    var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
    g.src=BASE_URL+"/packs/js/sdk.js";
    g.async = true;
    s.parentNode.insertBefore(g,s);
    g.onload=function(){
      window.chatwootSDK.run({
        websiteToken: 'saMcpgSupcmd1VQwytgPLfbK',
        baseUrl: BASE_URL
      })
    }
  })(document,"script");
</script>
```

This explicit user-provided integration uses HTTP. Do not silently upgrade it, substitute a token, or add additional remote scripts; report mixed-content risk when the page will be served by HTTPS.

## Five-Image Product Hero Carousel

Replace any generic canvas, decorative animation, stock image, or generated hero art with a 5-image product carousel.

1. Derive one precise search phrase from the product name, model, or process. Search the public image library at `https://ph.smthelp.com/search/images/?q=<URL-encoded-keyword>`. Do not assume a WordPress Media REST API is available.
2. Inspect candidate metadata and thumbnails, select five distinct images that visibly match the product/process, and record their direct HTTPS image URLs in the file.
3. If fewer than five trustworthy matches are available, do not fill gaps with unrelated images. Use verified alternate views from the same product source, or stop and request/mark image confirmation.
4. Use a stable carousel aspect ratio, `object-fit: cover`, descriptive alt text, previous/next icon buttons, numbered accessible slide controls, an `aria-live="polite"` status, swipe support where practical, and autoplay that pauses on hover/focus and respects `prefers-reduced-motion`.
5. Use CSS transitions and plain JavaScript only. Prevent layout shift with explicit dimensions/aspect ratio. The hero copy and controls must remain usable on mobile and must not overlap the Chatwoot launcher.

The hero should state the verified application/value proposition first, then provide a real action such as `mailto:info@smthelp.com` or a validated request-form anchor. Avoid generic `#` CTAs.

## Recommended Page Order

1. Header with official Logo, concise navigation, and a real contact CTA.
2. Hero: evidence-bound product/process copy plus the five-image carousel.
3. Application/problem context and decision criteria.
4. Process or solution configuration, limited to verified equipment classes/models.
5. Technical/qualification inputs required for final model selection.
6. Contact CTA and required footer resources.
7. Chatwoot loader as the final page script.

## Adversarial Review Before Delivery

Check the contrary reading: could a buyer treat wording as an unsupported promise, a third-party/OEM claim, or a product specification? Correct it before handing off.

- Verify the file opens locally, has no script errors, and does not depend on a development server.
- Inspect desktop and narrow mobile layouts. Check carousel controls, keyboard navigation, focus ring, text wrapping, hero image loading, footer links, and Chatwoot clearance.
- Search the completed page for `{{`, `}}`, `${`, `TODO`, `FIXME`, placeholder URLs/text, credentials unrelated to the provided Chatwoot integration, and local absolute paths.
- Confirm exactly five direct, product-matched `ph.smthelp.com` hero image URLs, one official Logo URL, the required footer links, and one Chatwoot loader.
- State the file path, channel, factual sources, image-search phrase, five selected image URLs, validation results, and remaining `To be confirmed` items.

## Do Not Do These Things

- Do not invent technical figures, certifications, prices, delivery commitments, ROI, customer references, or third-party relationships.
- Do not use competitor products, generic stock imagery, or unrelated photo-library images as Southern Machinery evidence.
- Do not add frameworks, CDNs beyond the required direct image/YouTube/Chatwoot URLs, analytics, external form submission, or a second chatbot.
- Do not use a canvas-only hero, floating decorative cards, oversized marketing copy, or text CTAs without a real destination.
