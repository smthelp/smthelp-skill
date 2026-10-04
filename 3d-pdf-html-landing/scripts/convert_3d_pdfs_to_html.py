#!/usr/bin/env python3
"""Batch-convert 3D PDF product assets into single-file HTML SEO landing pages.

The generated WebGL model is a lightweight browser reconstruction based on the
source filename/category. It does not decode PRC/U3D geometry.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


THREE_D_MARKERS = [
    b"/Subtype/3D",
    b"/Subtype /3D",
    b"/3DD",
    b"/3DA",
    b"/Subtype/PRC",
    b"/Subtype /PRC",
    b"/Subtype/U3D",
    b"/Subtype /U3D",
    b"/RichMedia",
    b"%PRC",
    b"U3D",
]

LOGO_URL = "https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png"

SOCIAL_LINKS = [
    ("LinkedIn Company Page", "https://www.linkedin.com/company/smtmachine"),
    ("LinkedIn Profile", "https://cn.linkedin.com/in/smtsupplier"),
    ("Twitter", "https://twitter.com/smtspecialist"),
    ("Facebook", "https://www.facebook.com/autoinsertion"),
    ("YouTube Channel", "https://www.youtube.com/c/Smthelping"),
]

CATEGORY_RULES = [
    (
        "radial-insertion",
        ["radial", "s3010", "s3020", "radial insertion", "radialinserter"],
        "Radial Component Insertion Automation",
        "Inspect the feeder bank, PCB lane, insertion head, and clinch zone for radial THT automation planning.",
        "insertion",
    ),
    (
        "axial-insertion",
        ["axial", "s4000", "s4020"],
        "Axial Component Insertion Automation",
        "Review axial taped component feeding, board transfer, and under-board forming logic in a browser-native viewer.",
        "insertion",
    ),
    (
        "oddform-insertion",
        ["oddform", "odd form", "oddfrom", "oddfrom", "s7000", "s7030", "s7040", "s70od"],
        "Odd-form Component Insertion Automation",
        "Show bowl feeding, robotic insertion, access zones, and line integration for odd-form THT components.",
        "oddform",
    ),
    (
        "pin-eyelet-insertion",
        ["pin eyelet", "eyelet", "pin inserter", "pin insertion", "s700p", "s7000p"],
        "Pin and Eyelet Insertion Automation",
        "Present pin or eyelet feeding, insertion tooling, and downstream board handling in a compact 3D scene.",
        "pin",
    ),
    (
        "smt-mounter",
        ["mounter", "pick n place", "pick and place", "chip mounter", "label mounter", "universal", "fuji nxt", "gsm"],
        "SMT Pick-and-place Automation",
        "Explain SMT placement, feeder-side access, board transport, and production-line fit for PCB assembly buyers.",
        "mounter",
    ),
    (
        "feeder",
        ["feeder", "bowl", "vibration", "tube", "stick", "tray", "tape feeder", "label feeder"],
        "SMT/THT Feeder and Component Supply",
        "Help buyers inspect feeder body layout, component path, reel or tube loading, and compatibility questions.",
        "feeder",
    ),
    (
        "nozzle",
        ["nozzle", "gripper", "chuck", "minichuck"],
        "Customized SMT/THT Nozzle and Gripper Tooling",
        "Show gripping, vacuum, and contact geometry concepts for customized SMT and THT handling tools.",
        "nozzle",
    ),
    (
        "board-handling",
        ["loader", "unloader", "conveyor", "shuttle", "flipper", "turn", "buffer", "ngok", "bhs", "magazine", "cassette", "destacker"],
        "PCB Board Handling Equipment",
        "Visualize board loading, unloading, transfer, buffering, flipping, or routing inside SMT/THT production lines.",
        "handling",
    ),
    (
        "wave-soldering",
        ["wave soldering", "soldering", "reflow", "printer", "cleaning", "lead cutter", "robot solder"],
        "PCB Assembly Process Equipment",
        "Present supporting process equipment for soldering, printing, cleaning, cutting, or line preparation.",
        "process",
    ),
    (
        "pcba-demo",
        ["pcba", "pcb board", "pcb assembly", "mobile charger", "raspberry", "power converter", "camera pcba"],
        "PCB Assembly Sample and Product Demo",
        "Use a 3D PCBA display to explain application fit, component density, and automation review inputs.",
        "pcba",
    ),
]


@dataclass
class PdfAsset:
    path: Path
    rel_path: str
    title: str
    slug: str
    category: str
    category_label: str
    summary: str
    model_profile: str
    markers: list[str]
    size_bytes: int
    model_hint: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Folder containing PDF assets.")
    parser.add_argument("--output", required=True, help="Output folder for generated pages.")
    parser.add_argument("--brand", default="southern-machinery", choices=["southern-machinery"])
    parser.add_argument("--limit", type=int, default=0, help="Limit number of detected assets.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing pages.")
    parser.add_argument("--sort", choices=["name", "size"], default="name", help="Processing order for detected PDFs.")
    parser.add_argument("--geo-seo", action="store_true", help="Add GEO/AI-search answer blocks, FAQ, and FAQ schema.")
    parser.add_argument("--include-all-pdfs", action="store_true", help="Generate pages for PDFs even without detected 3D markers.")
    parser.add_argument("--manifest-name", default="manifest.json", help="Manifest filename.")
    return parser.parse_args()


def normalized_text(value: str) -> str:
    value = re.sub(r"\.[Pp][Dd][Ff]$", "", value)
    value = value.replace("_", " ")
    value = re.sub(r"\b3d\b", "3D", value, flags=re.I)
    value = re.sub(r"\bpdf\b", "PDF", value, flags=re.I)
    value = re.sub(r"\s+", " ", value).strip(" -_")
    return value or "3D PDF Product"


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:110].strip("-") or "3d-pdf-product"


def human_title(path: Path) -> str:
    raw = normalized_text(path.name)
    words = []
    acronyms = {"smt", "tht", "pcb", "pcba", "bga", "aoi", "ngok", "led", "fuji", "juki", "uic", "nxt", "gsm"}
    for word in raw.split(" "):
        clean = re.sub(r"[^A-Za-z0-9-]", "", word)
        if not clean:
            continue
        if clean.lower() in acronyms or re.match(r"^[A-Za-z]*\d", clean):
            words.append(clean.upper())
        elif clean.upper() in {"PDF", "3D"}:
            words.append(clean.upper())
        else:
            words.append(clean[:1].upper() + clean[1:].lower())
    return " ".join(words).replace(" 3D PDF", " 3D")


def detect_markers(path: Path) -> list[str]:
    found: list[str] = []
    lower_found = set()
    overlap = 64
    previous = b""
    try:
        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                haystack = previous + chunk
                for marker in THREE_D_MARKERS:
                    if marker.lower() in lower_found:
                        continue
                    if marker in haystack:
                        found.append(marker.decode("latin1"))
                        lower_found.add(marker.lower())
                previous = haystack[-overlap:]
    except OSError:
        return found
    return found


def classify(path: Path) -> tuple[str, str, str, str]:
    text = path.name.lower()
    compact = re.sub(r"[^a-z0-9]+", "", text)
    for category, keywords, label, summary, profile in CATEGORY_RULES:
        for keyword in keywords:
            k = keyword.lower()
            if k in text or re.sub(r"[^a-z0-9]+", "", k) in compact:
                return category, label, summary, profile
    return (
        "generic-equipment",
        "PCB Assembly Automation Equipment",
        "Explore this 3D product asset as a browser-native marketing viewer for PCB assembly automation discussions.",
        "generic",
    )


def model_hint_from_filename(path: Path, category: str) -> str:
    text = path.name.lower()
    if "line" in text or "loader" in text and "unloader" in text:
        return "production-line"
    if "pcba" in text or "pcb board" in text:
        return "with-pcba"
    if "feeder" in text:
        return "feeder-detail"
    if "nozzle" in text or "gripper" in text:
        return "tooling-detail"
    return category


def iter_pdfs(root: Path, output: Path) -> Iterable[Path]:
    output_resolved = output.resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name.startswith("._"):
            continue
        if path.suffix.lower() != ".pdf":
            continue
        try:
            if output_resolved in path.resolve().parents:
                continue
        except OSError:
            pass
        yield path


def collect_assets(root: Path, output: Path, include_all: bool, limit: int, sort_mode: str) -> list[PdfAsset]:
    assets: list[PdfAsset] = []
    used_slugs: dict[str, int] = {}
    for path in sorted(iter_pdfs(root, output), key=lambda p: str(p).lower()):
        markers = detect_markers(path)
        if not markers and not include_all:
            continue
        category, label, summary, profile = classify(path)
        title = human_title(path)
        base_slug = slugify(title)
        count = used_slugs.get(base_slug, 0)
        used_slugs[base_slug] = count + 1
        slug = base_slug if count == 0 else f"{base_slug}-{count + 1}"
        rel_path = os.path.relpath(path, root)
        assets.append(
            PdfAsset(
                path=path,
                rel_path=rel_path,
                title=title,
                slug=slug,
                category=category,
                category_label=label,
                summary=summary,
                model_profile=profile,
                markers=markers,
                size_bytes=path.stat().st_size,
                model_hint=model_hint_from_filename(path, category),
            )
        )
    if sort_mode == "size":
        assets.sort(key=lambda asset: (asset.size_bytes, asset.rel_path.lower()))
    else:
        assets.sort(key=lambda asset: asset.rel_path.lower())
    if limit:
        assets = assets[:limit]
    return assets


def product_model(title: str) -> str:
    match = re.search(r"\bS[- ]?\d{3,4}[A-Z]*\b", title, re.I)
    if match:
        return match.group(0).replace(" ", "-").upper()
    match = re.search(r"\b[A-Z]{2,5}\d{2,5}[A-Z]*\b", title, re.I)
    return match.group(0).upper() if match else "Custom 3D PDF Asset"


def page_features(asset: PdfAsset) -> list[tuple[str, str]]:
    common = [
        ("3D source traceability", f"Generated from {asset.rel_path}; detected markers: {', '.join(asset.markers) if asset.markers else 'not detected'}."),
        ("Browser-native interaction", "Drag to rotate, use the view buttons, and inspect the product without requiring Adobe 3D PDF playback."),
    ]
    by_category = {
        "radial-insertion": [
            ("Feeder-side selling", "Show radial taped component supply and changeover planning before the technical call."),
            ("THT automation fit", "Guide discussion around PCB size, radial component list, output target, and manual labor reduction."),
        ],
        "axial-insertion": [
            ("Axial component path", "Explain taped axial component feeding, insertion sequence, and line layout requirements."),
            ("Board-level qualification", "Prompt buyers to share PCB, BOM, pitch, and lead-forming requirements."),
        ],
        "oddform-insertion": [
            ("Odd-form handling", "Use the viewer to discuss bowl feeding, gripper tooling, and custom component presentation."),
            ("Custom review flow", "Encourage sample testing before confirming fixture, tooling, and output assumptions."),
        ],
        "pin-eyelet-insertion": [
            ("Pin insertion logic", "Present the insertion zone, tooling side, and feeding concept for pin or eyelet applications."),
            ("Application qualification", "Collect board holes, terminal type, insertion force, and downstream process information."),
        ],
        "smt-mounter": [
            ("SMT line context", "Show feeder access, board transfer, placement area, and integration with printer/reflow/AOI."),
            ("Application-led CTA", "Ask for product type, PCB size, component mix, and monthly production volume."),
        ],
        "feeder": [
            ("Compatibility discussion", "Use the page to qualify machine brand, component packaging, pitch, and feeding direction."),
            ("Detail-focused presentation", "Give buyers a fast visual reference for feeder structure and handling concept."),
        ],
        "nozzle": [
            ("Tooling detail", "Explain vacuum, gripping, contact surface, and component-specific customization questions."),
            ("Sample-driven engineering", "Guide prospects to send component photos, dimensions, and placement process details."),
        ],
        "board-handling": [
            ("Line balancing", "Discuss loader, conveyor, buffer, flipper, shuttle, and unloader positions in the full line."),
            ("Factory layout readiness", "Prompt buyers to share board size, flow direction, line height, and upstream/downstream equipment."),
        ],
        "wave-soldering": [
            ("Process integration", "Position the equipment as part of a complete SMT/THT assembly workflow."),
            ("Technical confirmation", "Collect board size, process target, factory utilities, and inspection requirements."),
        ],
        "pcba-demo": [
            ("Application storytelling", "Use the PCBA scene to explain product category, component density, and assembly flow."),
            ("Solution matching", "Move the conversation from board example to suitable SMT/THT automation configuration."),
        ],
    }
    return by_category.get(asset.category, [
        ("Product inspection", "Provide a fast interactive preview for sales conversations and catalog browsing."),
        ("Qualification CTA", "Ask for application, board size, component type, and production target."),
    ]) + common


def process_steps(asset: PdfAsset) -> list[tuple[str, str, str]]:
    return [
        ("Input", "Share PCB and component data", "Send board drawing, BOM, component photos, packaging type, and monthly volume."),
        ("Check", "Confirm automation feasibility", "Review component presentation, board handling direction, tooling risk, and line fit."),
        ("Plan", "Match the production cell", "Select the right machine, feeder, conveyor, and upstream/downstream equipment."),
        ("ROI", "Calculate payback transparently", "Use labor count, shifts, output target, wage cost, and equipment scope."),
    ]


def geo_answer(asset: PdfAsset) -> str:
    return (
        f"{asset.title} is positioned as {asset.category_label.lower()} for PCB assembly automation buyers. "
        f"The page gives EMS engineers a fast answer to what the asset is, where it fits in SMT/THT production, "
        f"which information Southern Machinery needs for technical review, and why the original 3D PDF has been "
        f"rebuilt as a browser-native WebGL viewer for sales and SEO use."
    )


def qualification_questions(asset: PdfAsset) -> list[str]:
    category_specific = {
        "radial-insertion": "Which radial taped components, pitches, polarity requirements, and current manual insertion steps are used?",
        "axial-insertion": "Which axial taped components, lead-forming requirements, and board hole patterns need to be reviewed?",
        "oddform-insertion": "Which odd-form components require bowl feeding, gripper tooling, or custom presentation?",
        "pin-eyelet-insertion": "What pin or eyelet type, insertion force, hole size, and board thickness must be confirmed?",
        "smt-mounter": "What PCB size, component mix, placement speed target, and upstream printer/reflow setup are planned?",
        "feeder": "Which host machine brand, component package, pitch, tape/tube/tray format, and feeding direction are required?",
        "nozzle": "What component dimensions, surface finish, gripping/vacuum area, and placement tolerance should the tooling support?",
        "board-handling": "What board size, line height, flow direction, magazine size, and upstream/downstream machines define the layout?",
        "wave-soldering": "What soldering, printing, cleaning, or process target needs to be matched with the PCB and factory utilities?",
        "pcba-demo": "What product family, monthly volume, SMT/THT mix, and quality bottleneck should the automation plan solve?",
    }
    return [
        category_specific.get(asset.category, "What PCB, component, volume, and process bottleneck should this equipment solve?"),
        "What is the monthly production volume and target output per shift?",
        "How many operators are involved in the current manual or semi-automatic process?",
        "Is the priority labor reduction, speed improvement, quality stability, or new line capacity?",
        "What timeline and budget range should Southern Machinery consider for the automation proposal?",
    ]


def faq_items(asset: PdfAsset) -> list[tuple[str, str]]:
    return [
        (
            f"What is {asset.title} used for?",
            f"It is presented as {asset.category_label.lower()} for PCB assembly automation discussions. Final application fit depends on the buyer's PCB, component package, process flow, and output target.",
        ),
        (
            "Is the WebGL model the original PRC or U3D geometry from the PDF?",
            "No. Browsers do not natively render PRC or U3D streams embedded in 3D PDFs. This page uses a lightweight WebGL reconstruction derived from the 3D PDF source for marketing and qualification.",
        ),
        (
            "What information is needed before quotation?",
            "Southern Machinery should review PCB size, BOM, component photos, packaging format, production volume, current process, and automation goal before confirming machine configuration or price.",
        ),
        (
            "Can this page be used for SEO and AI search?",
            "Yes. The page includes a clear product answer block, buyer-intent copy, FAQ content, Product schema, FAQ schema, and searchable Southern Machinery contact information.",
        ),
        (
            "Are speed, price, delivery time, and ROI guaranteed on this page?",
            "No. Unless a verified catalog or quotation source is provided, commercial and technical details remain to be confirmed by Southern Machinery engineers and sales staff.",
        ),
        (
            "What is the next step for buyers?",
            "Send PCB drawings, component information, photos, and monthly production volume to jasonwu@smthelp.com for an automation feasibility review.",
        ),
    ]


def json_script(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def html_attr(value: str) -> str:
    return html.escape(value, quote=True)


def render_html(asset: PdfAsset, geo_seo: bool = False) -> str:
    model = product_model(asset.title)
    features = page_features(asset)
    steps = process_steps(asset)
    faqs = faq_items(asset)
    questions = qualification_questions(asset)
    answer = geo_answer(asset)
    description = f"{asset.summary} Single-file HTML landing page for Southern Machinery PCB assembly automation marketing."
    data = {
        "title": asset.title,
        "category": asset.category,
        "profile": asset.model_profile,
        "modelHint": asset.model_hint,
    }
    product_ld = {
        "@type": "Product",
        "name": asset.title,
        "description": description,
        "brand": {"@type": "Brand", "name": "Southern Machinery"},
        "manufacturer": {
            "@type": "Organization",
            "name": "Southern Machinery Co., Ltd.",
            "url": "https://www.smthelp.com",
            "logo": LOGO_URL,
            "sameAs": [url for _, url in SOCIAL_LINKS],
        },
        "category": asset.category_label,
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Source 3D PDF", "value": asset.rel_path},
            {"@type": "PropertyValue", "name": "Detected 3D markers", "value": ", ".join(asset.markers) if asset.markers else "Not detected"},
            {"@type": "PropertyValue", "name": "Specification status", "value": "Final commercial and technical specifications to be confirmed."},
        ],
    }
    faq_ld = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer_text},
            }
            for question, answer_text in faqs
        ],
    }
    ld = {"@context": "https://schema.org", "@graph": [product_ld, faq_ld] if geo_seo else [product_ld]}
    feature_html = "\n".join(
        f"<li><strong>{html.escape(title)}</strong>{html.escape(body)}</li>" for title, body in features
    )
    step_html = "\n".join(
        f"<div class=\"process-step\"><b>{html.escape(kicker)}</b><h3>{html.escape(title)}</h3><p>{html.escape(body)}</p></div>"
        for kicker, title, body in steps
    )
    social_html = "\n".join(
        f"<a href=\"{html_attr(url)}\">{html.escape(label)}</a>" for label, url in SOCIAL_LINKS
    )
    geo_html = ""
    if geo_seo:
        question_html = "\n".join(f"<li>{html.escape(question)}</li>" for question in questions)
        faq_html = "\n".join(
            f"<details><summary>{html.escape(question)}</summary><p>{html.escape(answer_text)}</p></details>"
            for question, answer_text in faqs
        )
        geo_html = f"""
    <section class="geo alt" id="geo-answer"><div class="inner two"><div><span class="kicker">GEO answer</span><h2>Fast answer for AI search and buyer research.</h2><p class="lede">{html.escape(answer)}</p></div><div class="answer-box"><strong>Best next step</strong><p>Send PCB drawings, BOM, component photos, package format, monthly volume, and current process notes to Southern Machinery for a feasibility review.</p></div></div></section>
    <section class="qualify"><div class="inner two"><div><span class="kicker">Buyer qualification</span><h2>Questions this page should answer before quotation.</h2><p class="lede">Use these prompts in email, LinkedIn, WhatsApp, and sales follow-up so the page becomes a technical lead-capture asset rather than only a viewer.</p></div><ol class="questions">{question_html}</ol></div></section>
    <section class="faq alt" id="faq"><div class="inner"><span class="kicker">FAQ for search engines and AI assistants</span><h2>Common questions buyers ask before sending samples.</h2><div class="faq-list">{faq_html}</div></div></section>"""
    markers = ", ".join(asset.markers) if asset.markers else "No explicit 3D marker detected"
    return HTML_TEMPLATE.replace("__PAGE_TITLE__", html.escape(f"{asset.title} | Interactive 3D SEO Landing Page | Southern Machinery")) \
        .replace("__META_DESCRIPTION__", html_attr(description[:300])) \
        .replace("__KEYWORDS__", html_attr(f"{asset.title}, {asset.category_label}, 3D PDF, WebGL product viewer, PCB assembly automation, Southern Machinery")) \
        .replace("__JSON_LD__", json.dumps(ld, ensure_ascii=False, indent=2).replace("</", "<\\/")) \
        .replace("__LOGO_URL__", LOGO_URL) \
        .replace("__H1__", html.escape(asset.title)) \
        .replace("__EYEBROW__", html.escape(asset.category_label)) \
        .replace("__SUMMARY__", html.escape(asset.summary)) \
        .replace("__MODEL__", html.escape(model)) \
        .replace("__SOURCE__", html.escape(asset.rel_path)) \
        .replace("__MARKERS__", html.escape(markers)) \
        .replace("__FEATURES__", feature_html) \
        .replace("__STEPS__", step_html) \
        .replace("__GEO_SEO_SECTIONS__", geo_html) \
        .replace("__SOCIAL_LINKS__", social_html) \
        .replace("__PAGE_DATA__", json_script(data))


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__PAGE_TITLE__</title>
  <meta name="description" content="__META_DESCRIPTION__">
  <meta name="keywords" content="__KEYWORDS__">
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="__PAGE_TITLE__">
  <meta property="og:description" content="__META_DESCRIPTION__">
  <meta property="og:type" content="website">
  <meta property="og:image" content="__LOGO_URL__">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">__JSON_LD__</script>
  <style>
    :root{--ink:#12201d;--soft:#40524c;--surface:#f6f8f9;--white:#fff;--line:#d7e0df;--green:#059669;--green2:#047857;--blue:#0e8fbd;--amber:#f59e0b;--graphite:#26343a;--shadow:0 22px 70px rgba(25,37,40,.16);font-family:Rubik,"Segoe UI",system-ui,sans-serif;color-scheme:light}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;min-width:320px;background:linear-gradient(90deg,rgba(18,32,29,.045) 1px,transparent 1px),linear-gradient(0deg,rgba(18,32,29,.035) 1px,transparent 1px),var(--surface);background-size:40px 40px;color:var(--ink);line-height:1.55}
    a{color:inherit}button{font:inherit}.skip{position:fixed;left:16px;top:12px;z-index:99;transform:translateY(-140%);background:var(--ink);color:white;padding:10px 14px;border-radius:6px;text-decoration:none}.skip:focus{transform:none;outline:3px solid var(--amber)}
    header{position:fixed;inset:0 0 auto;z-index:50;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px clamp(18px,4vw,56px);background:rgba(246,248,249,.86);border-bottom:1px solid rgba(18,32,29,.08);backdrop-filter:blur(16px)}
    .brand{min-height:44px;display:flex;align-items:center}.brand img{width:min(210px,48vw);height:auto}.nav{display:flex;gap:8px;font-size:13px;font-weight:800;text-transform:uppercase;color:var(--soft)}.nav a{min-height:44px;display:flex;align-items:center;padding:0 12px;border-radius:6px;text-decoration:none}.nav a:hover,.nav a:focus-visible{background:rgba(5,150,105,.1);color:var(--green2);outline:none}
    .hero{position:relative;min-height:92dvh;overflow:hidden;isolation:isolate;padding-top:92px;background:linear-gradient(135deg,#eef4f5,#f8fbfb 48%,#eef6f3)}.stage{position:absolute;inset:0;z-index:0}canvas{display:block;width:100%;height:100%;touch-action:none;cursor:grab}canvas:active{cursor:grabbing}canvas:focus-visible{outline:3px solid var(--amber);outline-offset:-8px}.hero:after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(90deg,rgba(246,248,249,.94),rgba(246,248,249,.62) 28%,rgba(246,248,249,.08) 62%,rgba(246,248,249,.72)),linear-gradient(0deg,rgba(246,248,249,.86),transparent 32%,transparent 72%,rgba(246,248,249,.38))}
    .copy{position:relative;z-index:3;width:min(660px,calc(100% - 36px));margin-left:clamp(18px,5vw,72px);padding-top:clamp(36px,7vh,92px)}.eyebrow{display:inline-flex;align-items:center;gap:10px;color:var(--green2);font-size:12px;font-weight:900;text-transform:uppercase}.eyebrow:before{content:"";width:34px;height:2px;background:var(--green)}
    h1{max-width:14ch;margin:18px 0 12px;font-size:clamp(42px,6.2vw,82px);line-height:.95;font-weight:900;letter-spacing:0}.copy p{max-width:620px;margin:0;color:var(--soft);font-size:clamp(17px,1.4vw,22px)}.actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}.btn{min-height:46px;display:inline-flex;align-items:center;justify-content:center;padding:0 18px;border:1px solid transparent;border-radius:6px;background:var(--green);color:white;font-weight:900;text-decoration:none;box-shadow:0 12px 24px rgba(5,150,105,.2)}.btn:hover,.btn:focus-visible{background:var(--green2);outline:none}.btn.secondary{background:rgba(255,255,255,.76);border-color:rgba(18,32,29,.14);box-shadow:none;color:var(--ink)}
    .toolbar{position:absolute;right:clamp(16px,4vw,48px);top:118px;z-index:4;display:grid;gap:8px;width:min(190px,calc(100vw - 32px))}.views{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.toolbar button{min-height:44px;border:1px solid rgba(18,32,29,.14);border-radius:6px;background:rgba(255,255,255,.78);font-size:12px;font-weight:900;cursor:pointer;box-shadow:0 8px 22px rgba(18,32,29,.08)}.toolbar button:hover,.toolbar button:focus-visible{background:white;border-color:rgba(5,150,105,.42);outline:none}.spin{grid-column:1/-1}
    .readout{position:absolute;right:clamp(16px,4vw,48px);bottom:clamp(28px,8vh,74px);z-index:4;width:min(340px,calc(100vw - 32px));padding:18px;border-left:4px solid var(--green);background:rgba(255,255,255,.84);box-shadow:var(--shadow);backdrop-filter:blur(14px)}.readout strong{display:block;margin-bottom:5px}.readout span{display:block;color:var(--soft);font-size:14px}.meta{position:absolute;left:clamp(18px,5vw,72px);bottom:18px;z-index:4;display:flex;flex-wrap:wrap;gap:8px;width:min(840px,calc(100% - 36px));font-size:12px;font-weight:800;color:var(--soft)}.meta span{min-height:30px;display:flex;align-items:center;padding:0 10px;border:1px solid rgba(18,32,29,.11);border-radius:999px;background:rgba(255,255,255,.74)}
    .hotspots{position:absolute;inset:0;z-index:5;pointer-events:none}.hotspot{position:absolute;width:34px;height:34px;border:0;border-radius:50%;background:var(--green);color:white;font-weight:900;pointer-events:auto;box-shadow:0 0 0 8px rgba(5,150,105,.14),0 14px 32px rgba(5,150,105,.26)}
    section{padding:clamp(64px,9vw,118px) clamp(18px,5vw,72px);background:var(--surface)}section.alt{background:white}.inner{width:min(1180px,100%);margin:auto}.kicker{color:var(--green2);font-size:12px;font-weight:900;text-transform:uppercase}h2{max-width:920px;margin:12px 0 20px;font-size:clamp(30px,4.8vw,62px);line-height:1.02}.lede{max-width:760px;color:var(--soft);font-size:clamp(17px,1.5vw,21px)}.two{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.05fr);gap:clamp(28px,5vw,72px);align-items:start}.features{display:grid;gap:14px;margin:0;padding:0;list-style:none}.features li{position:relative;padding:18px 18px 18px 48px;border:1px solid var(--line);border-radius:8px;background:white;box-shadow:0 10px 28px rgba(18,32,29,.06);color:var(--soft)}.features li:before{content:"";position:absolute;left:18px;top:23px;width:14px;height:14px;border-radius:50%;background:var(--green);box-shadow:inset 0 0 0 4px #dff4ec}.features strong{display:block;margin-bottom:4px;color:var(--ink)}.answer-box{padding:24px;border:1px solid rgba(5,150,105,.24);border-left:4px solid var(--green);border-radius:8px;background:#fff;box-shadow:0 16px 40px rgba(18,32,29,.08)}.answer-box strong{display:block;margin-bottom:8px;font-size:18px}.answer-box p{margin:0;color:var(--soft)}.questions{display:grid;gap:10px;margin:0;padding-left:22px;color:var(--soft)}.questions li{padding:14px 16px;border:1px solid var(--line);border-radius:8px;background:white}.faq-list{display:grid;gap:10px;margin-top:30px}.faq-list details{border:1px solid var(--line);border-radius:8px;background:white;box-shadow:0 10px 28px rgba(18,32,29,.05)}.faq-list summary{cursor:pointer;padding:18px;font-weight:900}.faq-list p{margin:0;padding:0 18px 18px;color:var(--soft)}
    table{width:100%;border-collapse:collapse;border:1px solid var(--line);border-radius:8px;background:white;overflow:hidden;box-shadow:0 16px 40px rgba(18,32,29,.08)}th,td{padding:16px 18px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{width:38%;background:#f2f6f5;font-size:13px;text-transform:uppercase}td{color:var(--soft)}tr:last-child th,tr:last-child td{border-bottom:0}.note{margin-top:16px;color:var(--soft);font-size:13px}
    .process{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:32px}.process-step{min-height:190px;padding:20px;border:1px solid var(--line);border-radius:8px;background:white;position:relative;overflow:hidden}.process-step:after{content:"";position:absolute;left:20px;right:20px;bottom:20px;height:4px;background:linear-gradient(90deg,var(--green),var(--blue),var(--amber))}.process-step b{font-size:12px;text-transform:uppercase}.process-step h3{margin:18px 0 10px;font-size:20px;line-height:1.15}.process-step p{margin:0;color:var(--soft);font-size:14px}
    .cta{color:white;background:linear-gradient(120deg,rgba(5,150,105,.96),rgba(14,143,189,.92))}.cta h2{color:white}.cta p{max-width:720px;margin:0;color:rgba(255,255,255,.88);font-size:18px}.cta .inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:32px;align-items:center}.cta .btn{background:white;color:var(--green2);box-shadow:0 20px 44px rgba(0,0,0,.16)}
    footer{padding:48px clamp(18px,5vw,72px);background:#15231f;color:rgba(255,255,255,.78)}.foot{width:min(1180px,100%);margin:auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.9fr);gap:36px}.foot h2{margin:0 0 14px;color:white;font-size:28px}.social{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.social a{min-height:44px;display:flex;align-items:center;padding:0 12px;border:1px solid rgba(255,255,255,.14);border-radius:6px;color:white;text-decoration:none}.catalog{grid-column:1/-1;padding-top:20px;border-top:1px solid rgba(255,255,255,.14);font-size:14px}.catalog a{color:white;font-weight:900}
    @media(max-width:980px){.nav{display:none}.hero{min-height:900px}.toolbar,.readout{right:18px}.readout{bottom:86px}.two,.process,.cta .inner,.foot{grid-template-columns:1fr}}
    @media(max-width:620px){header{padding:12px 16px}.brand img{width:min(180px,62vw)}.hero{min-height:960px;padding-top:72px;padding-bottom:24px}.copy{width:calc(100% - 32px);margin-left:16px}h1{font-size:clamp(42px,16vw,64px)}.toolbar,.readout,.meta{position:relative;left:auto;right:auto;top:auto;bottom:auto;width:calc(100% - 32px);margin-left:16px;margin-right:16px}.toolbar{margin-top:30px}.readout,.meta{margin-top:16px}.hotspots{display:none}.social{grid-template-columns:1fr}table,tbody,tr,th,td{display:block;width:100%}th{border-bottom:0;padding-bottom:6px}td{padding-top:6px}}
    @media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;transition-duration:.001ms!important;animation-duration:.001ms!important}}
  </style>
</head>
<body>
  <a class="skip" href="#main">Skip to product content</a>
  <header><a class="brand" href="https://www.smthelp.com" aria-label="Southern Machinery website"><img src="__LOGO_URL__" width="300" height="83" alt="Southern Machinery logo"></a><nav class="nav" aria-label="Page navigation"><a href="#viewer">3D viewer</a><a href="#fit">Automation fit</a><a href="#specs">Specs</a><a href="#contact">Contact</a></nav></header>
  <main id="main">
    <section class="hero" id="viewer" aria-labelledby="title"><div class="stage"><canvas id="modelCanvas" tabindex="0" role="img" aria-label="Interactive WebGL product viewer. Drag to rotate, scroll to zoom, or use view buttons."></canvas></div><div class="copy"><span class="eyebrow">__EYEBROW__</span><h1 id="title">__H1__</h1><p>__SUMMARY__</p><div class="actions"><a class="btn" href="mailto:jasonwu@smthelp.com?subject=Automation%20feasibility%20review">Send PCB sample</a><a class="btn secondary" href="#specs">Review line fit</a></div></div><div class="toolbar" aria-label="3D viewer controls"><div class="views"><button type="button" data-view="iso">Iso</button><button type="button" data-view="front">Front</button><button type="button" data-view="top">Top</button><button type="button" data-view="detail">Detail</button></div><button type="button" class="spin" id="spinToggle" aria-pressed="true">Pause rotation</button></div><div class="hotspots" id="hotspots"></div><aside class="readout" aria-live="polite"><strong id="readoutTitle">Drag the product to inspect it</strong><span id="readoutBody">This is a browser-native WebGL reconstruction for marketing. The original PDF remains the source visual asset.</span></aside><div class="meta"><span>Source: __SOURCE__</span><span>Detected: __MARKERS__</span><span>Single-file HTML with inline WebGL</span></div></section>
    <section class="alt" id="fit"><div class="inner"><span class="kicker">Marketing-ready 3D PDF conversion</span><h2>Turn a sealed 3D PDF into a product page buyers can inspect in the browser.</h2><p class="lede">This page converts a product presentation asset into a lightweight landing page for EMS buyers, production managers, and PCB assembly engineers. Use it to qualify the application before quotation.</p></div></section>
    <section><div class="inner two"><div><span class="kicker">Why this page helps sales</span><h2>Use visual inspection to start the technical conversation earlier.</h2><p class="lede">The interactive scene helps buyers understand the equipment type, line position, and review inputs without installing a 3D PDF viewer.</p></div><ul class="features">__FEATURES__</ul></div></section>
__GEO_SEO_SECTIONS__
    <section class="alt" id="specs"><div class="inner two"><div><span class="kicker">Specification status</span><h2>Confirm all technical and commercial data before quotation.</h2><p class="lede">The 3D PDF is a visual source. Final speed, dimensions, feeder compatibility, delivery time, price, and warranty must be checked against the latest catalog and engineering review.</p></div><div><table aria-label="Product review summary"><tbody><tr><th scope="row">Product model</th><td>__MODEL__</td></tr><tr><th scope="row">Category</th><td>__EYEBROW__</td></tr><tr><th scope="row">Source file</th><td>__SOURCE__</td></tr><tr><th scope="row">3D stream</th><td>__MARKERS__</td></tr><tr><th scope="row">Next data needed</th><td>PCB size, component list, production volume, current process, target output, and automation goal.</td></tr></tbody></table><p class="note">Browser engines do not natively render PRC/U3D streams from 3D PDF. This page uses a fast WebGL reconstruction for marketing interaction.</p></div></div></section>
    <section><div class="inner"><span class="kicker">Recommended qualification flow</span><h2>Move from product interest to a technical review.</h2><div class="process">__STEPS__</div></div></section>
    <section class="cta" id="contact"><div class="inner"><div><span class="kicker" style="color:rgba(255,255,255,.82)">Technical review</span><h2>Ready to check this equipment against your PCB assembly process?</h2><p>Send PCB drawings, component photos, packaging details, and monthly volume. Southern Machinery will help review automation feasibility before quotation.</p></div><a class="btn" href="mailto:jasonwu@smthelp.com?subject=Southern%20Machinery%20automation%20review">Email Southern Machinery</a></div></section>
  </main>
  <footer><div class="foot"><div><h2>Southern Machinery Co., Ltd.</h2><p>Smart PCB assembly automation from Shenzhen since 2011. SMT, THT, wave soldering, board handling, feeders, and customized automation support for global EMS factories.</p></div><nav class="social" aria-label="Company social media links">__SOCIAL_LINKS__</nav><p class="catalog">Browse our machine catalog at <a href="https://file.autoinsertion.com">file.autoinsertion.com</a> and find machine photos at <a href="https://ph.smthelp.com">ph.smthelp.com</a>.</p></div></footer>
  <script>
  (()=>{"use strict";const DATA=__PAGE_DATA__;const c=document.getElementById("modelCanvas"),gl=c.getContext("webgl",{antialias:true,alpha:true});const title=document.getElementById("readoutTitle"),body=document.getElementById("readoutBody"),hot=document.getElementById("hotspots"),reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;if(!gl){title.textContent="WebGL is unavailable";body.textContent="Product details remain available below.";return}const vs=`attribute vec3 p;attribute vec3 n;attribute vec4 co;uniform mat4 m;uniform vec3 l;varying vec4 vc;varying float li;void main(){vec3 nn=normalize(n);li=.32+max(dot(nn,normalize(l)),0.)*.74;vc=co;gl_Position=m*vec4(p,1.);}`;const fs=`precision mediump float;varying vec4 vc;varying float li;void main(){gl_FragColor=vec4(vc.rgb*li,vc.a);}`;function sh(t,s){let x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(x));return x}const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);const loc={p:gl.getAttribLocation(pr,"p"),n:gl.getAttribLocation(pr,"n"),co:gl.getAttribLocation(pr,"co"),m:gl.getUniformLocation(pr,"m"),l:gl.getUniformLocation(pr,"l")};const F=[];function rgb(h,a=1){let v=parseInt(h.slice(1),16);return[(v>>16&255)/255,(v>>8&255)/255,(v&255)/255,a]}function V(p,n,co){F.push(p[0],p[1],p[2],n[0],n[1],n[2],co[0],co[1],co[2],co[3])}function box(C,S,H){const co=rgb(H),x=S[0]/2,y=S[1]/2,z=S[2]/2,faces=[[[1,0,0],[[x,-y,-z],[x,y,-z],[x,y,z],[x,-y,z]]],[[-1,0,0],[[-x,-y,z],[-x,y,z],[-x,y,-z],[-x,-y,-z]]],[[0,1,0],[[-x,y,-z],[-x,y,z],[x,y,z],[x,y,-z]]],[[0,-1,0],[[-x,-y,z],[-x,-y,-z],[x,-y,-z],[x,-y,z]]],[[0,0,1],[[-x,-y,z],[x,-y,z],[x,y,z],[-x,y,z]]],[[0,0,-1],[[x,-y,-z],[-x,-y,-z],[-x,y,-z],[x,y,-z]]]];for(const f of faces){let p=f[1].map(q=>[q[0]+C[0],q[1]+C[1],q[2]+C[2]]);V(p[0],f[0],co);V(p[1],f[0],co);V(p[2],f[0],co);V(p[0],f[0],co);V(p[2],f[0],co);V(p[3],f[0],co)}}function cyl(C,r,len,axis,H,seg=24){const co=rgb(H),hh=len/2;function or(p){return axis==="x"?[p[1],p[0],p[2]]:axis==="z"?[p[0],p[2],p[1]]:p}function add(a,b){return[a[0]+b[0],a[1]+b[1],a[2]+b[2]]}for(let i=0;i<seg;i++){let a=i/seg*Math.PI*2,b=(i+1)/seg*Math.PI*2,p0=[Math.cos(a)*r,-hh,Math.sin(a)*r],p1=[Math.cos(b)*r,-hh,Math.sin(b)*r],p2=[Math.cos(b)*r,hh,Math.sin(b)*r],p3=[Math.cos(a)*r,hh,Math.sin(a)*r],n0=[Math.cos(a),0,Math.sin(a)],n1=[Math.cos(b),0,Math.sin(b)];let w=[p0,p1,p2,p3].map(q=>add(or(q),C)),nn=[or(n0),or(n1)];V(w[0],nn[0],co);V(w[1],nn[1],co);V(w[2],nn[1],co);V(w[0],nn[0],co);V(w[2],nn[1],co);V(w[3],nn[0],co)}}function base(){box([0,.35,0],[5.8,.7,1.2],"#dfe7ea");box([0,.8,0],[5.4,.08,1.0],"#f7fbfb");box([0,1.05,0],[4.2,.05,.5],"#059669");box([-2.25,1.55,-.35],[.22,1.3,.2],"#cdd8dc");box([2.25,1.55,-.35],[.22,1.3,.2],"#cdd8dc");box([0,2.25,-.35],[4.8,.22,.22],"#e8eef1")}function build(){const p=DATA.profile;base();if(p==="feeder"){for(let i=0;i<8;i++){let x=-2.1+i*.6;box([x,1.15,.55],[.32,.22,.9],"#dfe7ea");cyl([x,1.42,1.05],.18,.1,"x",i%2?"#0e8fbd":"#f59e0b")}box([0,1.75,.85],[5,.1,.08],"#26343a")}else if(p==="nozzle"){box([0,1.45,0],[.8,.5,.8],"#26343a");cyl([0,1.9,0],.22,.65,"y","#0e8fbd");cyl([0,1.1,0],.13,.85,"y","#f59e0b");for(let i=0;i<6;i++)cyl([Math.cos(i)*.75,1.05,Math.sin(i)*.75],.05,.4,"y","#059669")}else if(p==="handling"){box([0,1.05,0],[5.6,.12,.72],"#26343a");for(let i=0;i<12;i++)cyl([-2.5+i*.45,1.16,0],.07,.78,"z","#dfe7ea");box([-2.7,1.55,0],[.5,1,.8],"#e8eef1");box([2.7,1.55,0],[.5,1,.8],"#e8eef1")}else if(p==="pcba"){box([0,1.18,0],[4,.05,1.65],"#059669");for(let i=0;i<18;i++)box([-1.8+(i%6)*.72,1.28,-.55+Math.floor(i/6)*.55],[.28,.15,.22],i%3?"#26343a":"#f59e0b")}else{for(let i=0;i<10;i++){let x=-2.2+i*.5;box([x,1.15,.72],[.24,.18,.85],"#e8eef1");cyl([x,1.45,1.15],.15,.08,"x",i%2?"#0e8fbd":"#f59e0b")}box([0,1.95,-.05],[.8,.45,.5],"#0e8fbd");cyl([0,1.45,0],.08,.55,"y","#26343a")}}build();const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(F),gl.STATIC_DRAW);const count=F.length/10,state={yaw:-.78,pitch:.33,d:6.7,spin:!reduced,drag:false,lx:0,ly:0,m:new Float32Array(16)};function persp(o,f,a,n,fa){let q=1/Math.tan(f/2);o[0]=q/a;o[1]=0;o[2]=0;o[3]=0;o[4]=0;o[5]=q;o[6]=0;o[7]=0;o[8]=0;o[9]=0;o[10]=(fa+n)/(n-fa);o[11]=-1;o[12]=0;o[13]=0;o[14]=2*fa*n/(n-fa);o[15]=0}function look(o,e,t,u){let zx=e[0]-t[0],zy=e[1]-t[1],zz=e[2]-t[2],l=Math.hypot(zx,zy,zz);zx/=l;zy/=l;zz/=l;let xx=u[1]*zz-u[2]*zy,xy=u[2]*zx-u[0]*zz,xz=u[0]*zy-u[1]*zx;l=Math.hypot(xx,xy,xz);xx/=l;xy/=l;xz/=l;let yx=zy*xz-zz*xy,yy=zz*xx-zx*xz,yz=zx*xy-zy*xx;o[0]=xx;o[1]=yx;o[2]=zx;o[3]=0;o[4]=xy;o[5]=yy;o[6]=zy;o[7]=0;o[8]=xz;o[9]=yz;o[10]=zz;o[11]=0;o[12]=-(xx*e[0]+xy*e[1]+xz*e[2]);o[13]=-(yx*e[0]+yy*e[1]+yz*e[2]);o[14]=-(zx*e[0]+zy*e[1]+zz*e[2]);o[15]=1}function mul(o,a,b){for(let i=0;i<4;i++)for(let j=0;j<4;j++)o[i*4+j]=b[i*4]*a[j]+b[i*4+1]*a[j+4]+b[i*4+2]*a[j+8]+b[i*4+3]*a[j+12]}function resize(){let r=c.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2),w=Math.max(1,Math.round(r.width*d)),h=Math.max(1,Math.round(r.height*d));if(c.width!==w||c.height!==h){c.width=w;c.height=h}gl.viewport(0,0,w,h)}function frame(){resize();if(state.spin&&!state.drag)state.yaw+=.0026;let proj=new Float32Array(16),view=new Float32Array(16),eye=[state.d*Math.cos(state.pitch)*Math.sin(state.yaw),1.25+state.d*Math.sin(state.pitch),state.d*Math.cos(state.pitch)*Math.cos(state.yaw)];persp(proj,50*Math.PI/180,c.width/c.height,.1,80);look(view,eye,[0,1.25,0],[0,1,0]);mul(state.m,proj,view);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.useProgram(pr);gl.enable(gl.DEPTH_TEST);gl.enable(gl.CULL_FACE);gl.uniformMatrix4fv(loc.m,false,state.m);gl.uniform3f(loc.l,-.42,.82,.36);gl.bindBuffer(gl.ARRAY_BUFFER,buf);let s=40;gl.enableVertexAttribArray(loc.p);gl.vertexAttribPointer(loc.p,3,gl.FLOAT,false,s,0);gl.enableVertexAttribArray(loc.n);gl.vertexAttribPointer(loc.n,3,gl.FLOAT,false,s,12);gl.enableVertexAttribArray(loc.co);gl.vertexAttribPointer(loc.co,4,gl.FLOAT,false,s,24);gl.drawArrays(gl.TRIANGLES,0,count);requestAnimationFrame(frame)}function clamp(v,a,b){return Math.max(a,Math.min(b,v))}c.addEventListener("pointerdown",e=>{state.drag=true;state.lx=e.clientX;state.ly=e.clientY;c.setPointerCapture(e.pointerId)});c.addEventListener("pointermove",e=>{if(!state.drag)return;state.yaw+=(e.clientX-state.lx)*.008;state.pitch=clamp(state.pitch+(e.clientY-state.ly)*.006,-.32,1.05);state.lx=e.clientX;state.ly=e.clientY});c.addEventListener("pointerup",e=>{state.drag=false;c.releasePointerCapture(e.pointerId)});c.addEventListener("wheel",e=>{e.preventDefault();state.d=clamp(state.d+e.deltaY*.006,4.2,9.5)},{passive:false});document.querySelectorAll("[data-view]").forEach(b=>b.addEventListener("click",()=>{let v=b.dataset.view;if(v==="front"){state.yaw=0;state.pitch=.1}else if(v==="top"){state.yaw=-.4;state.pitch=1.02}else if(v==="detail"){state.yaw=-.08;state.pitch=.24;state.d=5.2}else{state.yaw=-.78;state.pitch=.33;state.d=6.7}}));document.getElementById("spinToggle").addEventListener("click",e=>{state.spin=!state.spin;e.currentTarget.textContent=state.spin?"Pause rotation":"Resume rotation";e.currentTarget.setAttribute("aria-pressed",String(state.spin))});frame()})();
  </script>
</body>
</html>
"""


def render_index(assets: list[PdfAsset], output: Path) -> str:
    cards = []
    for asset in assets:
        page = f"{asset.slug}.html"
        size_label = f"{asset.size_bytes / 1024:.1f} KB"
        cards.append(
            f"<a class=\"card\" href=\"{html_attr(page)}\"><span>{html.escape(asset.category_label)} - {html.escape(size_label)}</span><strong>{html.escape(asset.title)}</strong><small>{html.escape(asset.rel_path)}</small></a>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Southern Machinery 3D PDF HTML Landing Pages</title>
  <meta name="description" content="Generated single-file HTML SEO landing pages from Southern Machinery 3D PDF product assets.">
  <style>
    body{{margin:0;background:#f6f8f9;color:#12201d;font-family:Rubik,"Segoe UI",system-ui,sans-serif;line-height:1.5}}
    header{{padding:34px clamp(18px,5vw,72px);background:white;border-bottom:1px solid #d7e0df}}
    img{{width:min(220px,60vw);height:auto}}h1{{max-width:900px;font-size:clamp(34px,6vw,72px);line-height:.98;margin:28px 0 10px}}p{{color:#40524c;max-width:820px}}main{{padding:32px clamp(18px,5vw,72px) 72px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}.card{{display:block;min-height:160px;padding:18px;border:1px solid #d7e0df;border-radius:8px;background:white;text-decoration:none;color:inherit;box-shadow:0 12px 30px rgba(18,32,29,.06)}}.card:hover{{border-color:#059669}}.card span{{display:block;color:#047857;font-size:12px;font-weight:900;text-transform:uppercase}}.card strong{{display:block;margin:14px 0 10px;font-size:20px;line-height:1.1}}.card small{{color:#40524c;overflow-wrap:anywhere}}
  </style>
</head>
<body>
  <header><img src="{LOGO_URL}" alt="Southern Machinery logo"><h1>3D PDF HTML Landing Pages</h1><p>{len(assets)} generated single-file WebGL SEO pages. Review technical claims before publishing externally.</p></header>
  <main><div class="grid">{''.join(cards)}</div></main>
</body>
</html>
"""


def write_outputs(assets: list[PdfAsset], output: Path, force: bool, manifest_name: str, geo_seo: bool) -> None:
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    for asset in assets:
        out_file = output / f"{asset.slug}.html"
        if out_file.exists() and not force:
            status = "exists"
        else:
            out_file.write_text(render_html(asset, geo_seo=geo_seo), encoding="utf-8")
            status = "written"
        manifest.append(
            {
                "title": asset.title,
                "source": asset.rel_path,
                "html": out_file.name,
                "category": asset.category,
                "category_label": asset.category_label,
                "markers": asset.markers,
                "size_bytes": asset.size_bytes,
                "geo_seo": geo_seo,
                "status": status,
            }
        )
    (output / "index.html").write_text(render_index(assets, output), encoding="utf-8")
    (output / manifest_name).write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    with (output / "manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["title", "source", "html", "category", "category_label", "markers", "size_bytes", "geo_seo", "status"])
        writer.writeheader()
        for row in manifest:
            writer.writerow({**row, "markers": "; ".join(row["markers"])})


def main() -> int:
    args = parse_args()
    root = Path(args.input).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Input folder not found: {root}", file=sys.stderr)
        return 2
    assets = collect_assets(root, output, args.include_all_pdfs, args.limit, args.sort)
    if not assets:
        print("No 3D PDFs detected. Use --include-all-pdfs to generate pages for every PDF.", file=sys.stderr)
        return 1
    write_outputs(assets, output, args.force, args.manifest_name, args.geo_seo)
    print(f"Generated/reviewed {len(assets)} landing pages")
    print(f"Output: {output}")
    print(f"Index: {output / 'index.html'}")
    print(f"Manifest: {output / args.manifest_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
