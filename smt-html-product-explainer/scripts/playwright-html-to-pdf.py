#!/usr/bin/env python3
"""Export a self-contained SMT/THT explainer HTML to a print-ready A4 PDF
using Playwright + the system Google Chrome.

Use this when the simpler chrome --headless --print-to-pdf CLI isn't enough —
specifically when you need to:
  - Inject custom @page / @media print CSS at render time
  - Mutate the DOM before printing (replace a live <form> with a static summary
    + READER ACTION callout so the PDF is a clean visual deliverable)
  - Use a single Python script as the deliverable (bash + heredoc is awkward
    for multi-step DOM mutation)

Why this is better than the CLI for lead-magnet PDFs:
  - Lets the same HTML ship BOTH as a live web page (with form) AND as a
    printable PDF (form replaced with summary + CTA) — no separate
    "PDF version" to maintain.
  - SVG storyboard panels render correctly (fixes the viewBox-only collapse
    bug that plagues Chrome's print pipeline when SVGs lack explicit width).
  - Single file, no venv, no shell quoting hell. Playwright is already in
    the Hermes venv. Just `python3 this_script.py`.

Usage:
  python3 playwright-html-to-pdf.py <input.html> [output.pdf] [--slug SLUG]
                                              [--no-form] [--no-callout]

Defaults:
  input:   /Users/jasonwu/<basename>.html
  output:  <input-with-.pdf>
  slug:    derived from basename (e.g. radial-feeder-comic -> radial-feeder-comic)
  form:    replaced (default for lead-magnet PDFs)
  callout: inserted (default for lead-magnet PDFs)

Pass --no-form to skip the form replacement (e.g. for a pure explainer without
a form, or when the user wants the form to actually render in the PDF).

Requires:
  - macOS with Google Chrome.app at the default install path
  - Playwright + Python 3.9+ in the active environment
  - poppler (`brew install poppler`) for the optional pdftoppm verification
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# CSS injected at render time. Equivalent to the @media print block in the
# SKILL.md, plus a few extras (form/page-break hardening, SVG safety net).
PRINT_CSS = """
@page { size: A4 portrait; margin: 10mm 8mm 10mm 8mm; }
html, body {
    background: #020617 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    color-adjust: exact !important;
}
.scene { page-break-inside: avoid; }
.footer { page-break-inside: avoid; }
.lead-form-section { page-break-inside: avoid; }
.scene-art, .scene-art-full {
    page-break-inside: avoid;
    display: block !important;
}
.scene-art svg, .scene-art-full svg {
    width: 100% !important;
    height: auto !important;
    page-break-inside: avoid;
}
"""


def build_form_replace_js(slug: str) -> str:
    """Build the JS that replaces the live form with a static summary + callout.

    The f-string interpolation is done at the Python level (slug) so the
    JS stays a clean string with the placeholders escaped properly.
    """
    return f"""
() => {{
    const formSection = document.querySelector('.lead-form-section');
    if (!formSection) return;

    const labels = formSection.querySelectorAll('label');
    const fields = [];
    labels.forEach(l => {{
        const t = l.textContent.trim().replace(/\\s+/g, ' ');
        if (t) fields.push(t);
    }});

    // Replace the form with a static 4-field summary
    formSection.innerHTML = `
        <div style="background:linear-gradient(135deg,#0a1428,#0f172a);padding:24px;border-radius:14px;border:1px solid rgba(34,211,238,0.4);page-break-inside:avoid;">
            <h2 style="color:#22d3ee;font-family:'Inter',sans-serif;font-size:22px;margin:0 0 8px 0;font-weight:700">Get the Free Line Layout + ROI Model</h2>
            <p style="color:#cbd5e1;font-size:13px;line-height:1.5;margin:0 0 16px 0">Send us 4 inputs. Our Shenzhen engineering team returns a <strong style="color:#fff">PCB line Layout + ROI model</strong> within 48 hours. <strong style="color:#fff">No cost, no obligation.</strong></p>
            <div style="background:#020617;padding:14px 18px;border-radius:8px;border:1px dashed rgba(34,211,238,0.4);margin-bottom:16px">
                <div style="color:#22d3ee;font-size:10px;letter-spacing:2.5px;margin-bottom:8px">FIELDS WE NEED (4)</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 18px;font-size:13px;color:#e2e8f0">
                    <div>▸ <strong>${{fields[0] || 'Full Name *'}}</strong></div>
                    <div>▸ <strong>${{fields[1] || 'Company *'}}</strong></div>
                    <div>▸ <strong>${{fields[2] || 'Business Email *'}}</strong></div>
                    <div>▸ <strong>${{fields[3] || 'Monthly PCBA Volume *'}}</strong></div>
                </div>
            </div>
        </div>
    `;

    // Insert the READER ACTION callout right BEFORE the footer.
    // The page-break-inside: avoid is what stops Chrome from splitting
    // the callout across two pages (the most common layout bug).
    const footer = document.querySelector('footer');
    if (footer) {{
        const callout = document.createElement('div');
        callout.className = 'reader-action-callout';
        callout.style.cssText = 'margin:24px auto 18px auto;padding:24px 20px;background:linear-gradient(135deg,#0e7490,#0891b2);border-radius:14px;text-align:center;color:#fff;page-break-inside:avoid;';
        callout.innerHTML = `
            <div style="font-size:11px;letter-spacing:2.5px;opacity:0.9;margin-bottom:10px">— READER ACTION —</div>
            <div style="font-size:21px;font-weight:700;margin-bottom:8px">Submit the form on our website</div>
            <div style="font-size:13px;opacity:0.95;margin-bottom:14px;line-height:1.5">We reply within 2 hours during business days. Mention this PDF for a same-day quotation.</div>
            <div style="font-size:16px;font-weight:600;background:#020617;padding:11px 18px;border-radius:8px;display:inline-block;font-family:'JetBrains Mono',ui-monospace,monospace;letter-spacing:0.5px;margin-bottom:12px">ph.smthelp.com/{slug}</div>
            <div style="margin-top:10px;font-size:12px;opacity:0.92;line-height:1.6">WhatsApp: <strong>+86-136-0256-2576</strong> &nbsp;&middot;&nbsp; Email: <strong>jasonwu@smthelp.com</strong></div>
        `;
        footer.parentNode.insertBefore(callout, footer);
    }}
}}
"""


async def export_pdf(html_path, pdf_path, slug, replace_form=True):
    from playwright.async_api import async_playwright

    if not os.path.exists(html_path):
        raise FileNotFoundError(f"Input HTML not found: {html_path}")
    if not os.path.exists(CHROME):
        raise FileNotFoundError(
            f"Google Chrome not found at {CHROME}. "
            f"Install Chrome from https://www.google.com/chrome/"
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=CHROME,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--font-render-hinting=none",
            ],
        )
        context = await browser.new_context(
            viewport={"width": 1240, "height": 1754},
            device_scale_factor=2,
        )
        page = await context.new_page()

        await page.goto(f"file://{html_path}", wait_until="networkidle", timeout=60000)
        try:
            await page.wait_for_load_state("networkidle", timeout=30000)
        except Exception:
            pass
        await page.wait_for_timeout(3000)  # let webfonts settle

        # === Fix 1: SVG width attribute (the viewBox-only collapse bug) ===
        await page.evaluate("""() => {
            document.querySelectorAll('svg').forEach(s => {
                s.setAttribute('width', '100%');
                s.setAttribute('height', 'auto');
                s.setAttribute('preserveAspectRatio', 'xMidYMid meet');
                s.style.width = '100%';
                s.style.height = 'auto';
                s.style.maxWidth = '100%';
                s.style.display = 'block';
            });
        }""")

        # === Fix 2: Inject print CSS ===
        await page.add_style_tag(content=PRINT_CSS)

        # === Fix 3: Switch to print emulation BEFORE DOM mutation ===
        await page.emulate_media(media="print")

        # === Fix 4: Optional form replacement + READER ACTION callout ===
        if replace_form:
            await page.evaluate(build_form_replace_js(slug))
            await page.wait_for_timeout(1000)

        # === Fix 5: Render to PDF ===
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "10mm", "right": "8mm", "bottom": "10mm", "left": "8mm"},
            prefer_css_page_size=True,
            display_header_footer=False,
        )

        await browser.close()


def verify_pdf(pdf_path):
    """Run page-count + size sanity check, and render all pages to PNG for
    visual verification (so the user can vision_analyze them)."""
    import subprocess

    if not os.path.exists(pdf_path):
        print(f"\u26a0 PDF not found: {pdf_path}")
        return

    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"\n\u2713 PDF written: {pdf_path} ({size_kb:.1f} KB)")

    # Try pdfinfo first (from poppler)
    try:
        r = subprocess.run(
            ["pdfinfo", pdf_path], capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0:
            for line in r.stdout.split("\n"):
                if any(k in line for k in ["Pages", "Page size", "PDF version"]):
                    print(f"  {line}")
    except FileNotFoundError:
        pass

    # Render all pages to PNG with pdftoppm for vision_analyze
    out_dir = "/tmp/pdf_preview"
    os.makedirs(out_dir, exist_ok=True)
    # Clean old previews of this name
    base = Path(pdf_path).stem
    for f in os.listdir(out_dir):
        if f.startswith(f"{base}-"):
            os.remove(os.path.join(out_dir, f))

    try:
        subprocess.run(
            ["pdftoppm", "-png", "-r", "110", pdf_path, f"{out_dir}/{base}"],
            check=True,
            timeout=60,
        )
        pages = sorted(
            f for f in os.listdir(out_dir) if f.startswith(f"{base}-")
        )
        print(f"\n\u2713 Rendered {len(pages)} pages to {out_dir}/")
        print(f"  \u2192 Run vision_analyze on page-1, mid-page, and last page to verify.")
    except FileNotFoundError:
        print("  (skip pdftoppm: install with `brew install poppler`)")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Path to input HTML file")
    parser.add_argument("output", nargs="?", help="Path to output PDF (default: <input>.pdf)")
    parser.add_argument("--slug", help="Slug for the live URL (default: derived from input basename)")
    parser.add_argument("--no-form", action="store_true", help="Skip form replacement (keep live form in PDF)")
    parser.add_argument("--no-callout", action="store_true", help="(reserved for future) skip READER ACTION callout")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    output_path = (
        os.path.abspath(args.output) if args.output else input_path.replace(".html", ".pdf")
    )
    slug = args.slug or Path(input_path).stem

    if not os.path.exists(input_path):
        print(f"Error: input not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    print(f"\u2192 Input:   {input_path}")
    print(f"  Output:  {output_path}")
    print(f"  Slug:    {slug}")
    print(f"  Replace form: {not args.no_form}")

    asyncio.run(
        export_pdf(
            html_path=input_path,
            pdf_path=output_path,
            slug=slug,
            replace_form=not args.no_form,
        )
    )
    verify_pdf(output_path)


if __name__ == "__main__":
    main()
