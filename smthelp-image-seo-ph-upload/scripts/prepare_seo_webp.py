from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image


ROOT = Path(os.environ.get("SMTHELP_IMAGE_WORKSPACE", os.getcwd())).resolve()
PACKAGE_NAME = os.environ.get("SMTHELP_IMAGE_PACKAGE_DIR", f"seo-webp-upload-{datetime.now():%Y-%m-%d}")
OUTPUT_DIR = Path(PACKAGE_NAME)
if not OUTPUT_DIR.is_absolute():
    OUTPUT_DIR = ROOT / OUTPUT_DIR
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
BRAND = "Southern Machinery"
SITE_TAGS = ["Southern Machinery", "SMThelp", "PCB assembly equipment", "SMT equipment", "THT equipment"]
ALBUM_NAME = os.environ.get("SMTHELP_PH_ALBUM_NAME", f"southern-machinery-image-seo-webp-{datetime.now():%Y-%m-%d}")


@dataclass(frozen=True)
class ImageMeta:
    product: str
    certification: str
    model: str | None = None
    descriptor: str | None = None
    source_note: str | None = None


EXACT_META: dict[str, ImageMeta] = {
    "-s7000.jpg": ImageMeta("S7000 odd form insertion machine", "RoHS certification", "S7000", "duplicate source image"),
    "AGV robot CE.jpg": ImageMeta("AGV robot", "CE certification"),
    "CE -Curing Oven.jpg": ImageMeta("curing oven", "CE certification"),
    "CE certificate AGV robot.png": ImageMeta("AGV robot", "CE certification", descriptor="certificate scan"),
    "CE Certification -Dispensing machine.jpg": ImageMeta("dispensing machine", "CE certification"),
    "CE MD -Laser marker.jpg": ImageMeta("laser marking machine", "CE MD certification"),
    "CE MD Feeder.jpg": ImageMeta("feeder", "CE MD certification"),
    "CE MD- Axial Insertion.jpg": ImageMeta("axial insertion machine", "CE MD certification"),
    "CE MD- Oddform Insertion machine.jpg": ImageMeta("odd form insertion machine", "CE MD certification"),
    "CE(MD+ISO) Reflow Oven.jpg": ImageMeta("reflow oven", "CE MD and ISO certification"),
    "CE-MD+ISO V-cut Machine.jpg": ImageMeta("V-cut PCB separator machine", "CE MD and ISO certification"),
    "CE-ROHS Magazine Rack.jpg": ImageMeta("SMT magazine rack", "CE and RoHS certification"),
    "MD.jpg": ImageMeta("odd form insertion machine", "CE MD certification", descriptor="duplicate source image"),
    "PCB Board Handling Machine PCB conveyor Loader _3.jpg": ImageMeta("PCB board handling conveyor loader", "equipment certification image", descriptor="detail image 3"),
    "PCB Board Handling Machine PCB conveyor Loader _4.jpg": ImageMeta("PCB board handling conveyor loader", "equipment certification image", descriptor="detail image 4"),
    "PCB Board Handling Machine-CE Certification-逐页转图片.jpg": ImageMeta("PCB board handling machine", "CE certification", descriptor="converted certificate page"),
    "PCB Board Handling Machine-CE Certification-逐页转图片-1b87db8df078.jpg": ImageMeta("PCB board handling machine", "CE certification", descriptor="converted certificate page duplicate"),
    "PCB Board Handling Machine-ROHS Certification.jpg": ImageMeta("PCB board handling machine", "RoHS certification"),
    "PCB Board Handling Machine_3.jpg": ImageMeta("PCB board handling machine", "equipment certification image", descriptor="detail image 3"),
    "PCB Board Handling Machine_4.jpg": ImageMeta("PCB board handling machine", "equipment certification image", descriptor="detail image 4"),
    "PCB Board Handling Machine_5.jpg": ImageMeta("PCB board handling machine", "equipment certification image", descriptor="detail image 5"),
    "PCB Conveyor & Buffer_5.jpg": ImageMeta("PCB conveyor and buffer", "equipment certification image", descriptor="detail image 5"),
    "PCB Conveyor&Buffer-CE Certification-逐页转图片.jpg": ImageMeta("PCB conveyor and buffer", "CE certification", descriptor="converted certificate page"),
    "PCB Conveyor&Buffer-CE Certification-逐页转图片-4bdd19d72c81.jpg": ImageMeta("PCB conveyor and buffer", "CE certification", descriptor="converted certificate page duplicate"),
    "PCB Conveyor&Buffer-ROHS Certification.jpg": ImageMeta("PCB conveyor and buffer", "RoHS certification"),
    "PCB LD-Unloader-ROHS Certification_6.jpg": ImageMeta("PCB loader and unloader", "RoHS certification", descriptor="detail image 6"),
    "PCB LD-Unloader-ROHS Certification_7.jpg": ImageMeta("PCB loader and unloader", "RoHS certification", descriptor="detail image 7"),
    "PCB Loader CE.jpg": ImageMeta("PCB loader", "CE certification"),
    "PCB Loader Conveyor-ROHS Certification .jpg": ImageMeta("PCB loader conveyor", "RoHS certification"),
    "PCB Loader-CE Certification-逐页转图片.jpg": ImageMeta("PCB loader", "CE certification", descriptor="converted certificate page"),
    "PCB Loader-CE Certification-逐页转图片-e4539c1bda64.jpg": ImageMeta("PCB loader", "CE certification", descriptor="converted certificate page duplicate"),
    "PCB Unloader-CE Certification(1)-转长图.jpg": ImageMeta("PCB unloader", "CE certification", descriptor="long certificate image"),
    "PCB Unloader-CE Certification(1)-转长图-0bca44a63e74.jpg": ImageMeta("PCB unloader", "CE certification", descriptor="long certificate image duplicate"),
    "PCB Unloader-CE Certification-逐页转图片.jpg": ImageMeta("PCB unloader", "CE certification", descriptor="converted certificate page"),
    "PCB Unloader-CE Certification-逐页转图片-4345c4ea5a13.jpg": ImageMeta("PCB unloader", "CE certification", descriptor="converted certificate page duplicate"),
    "PCB Unloader-ROHS Certification.jpg": ImageMeta("PCB unloader", "RoHS certification"),
    "ROHS --Laser marker.jpg": ImageMeta("laser marking machine", "RoHS certification"),
    "ROHS -Oddform Insertion machine.jpg": ImageMeta("odd form insertion machine", "RoHS certification"),
    "ROHS _axial insertion.jpg": ImageMeta("axial insertion machine", "RoHS certification"),
    "ROHS.jpg": ImageMeta("laser marking machine", "RoHS certification", descriptor="duplicate source image"),
    "S3000 Radial Insertion Machine  ROHS.jpg": ImageMeta("S3000 radial insertion machine", "RoHS certification", "S3000"),
    "S3000 Radial Insertion Machine MD.jpg": ImageMeta("S3000 radial insertion machine", "CE MD certification", "S3000"),
    "S400 Laser Marking Machine MD.jpg": ImageMeta("S400 laser marking machine", "CE MD certification", "S400"),
    "S400 Laser Marking Machine ROHS.jpg": ImageMeta("S400 laser marking machine", "RoHS certification", "S400"),
    "S4000 Axial Insertion Machine MD.jpg": ImageMeta("S4000 axial insertion machine", "CE MD certification", "S4000"),
    "S4000 Axial Insertion Machine ROHS.jpg": ImageMeta("S4000 axial insertion machine", "RoHS certification", "S4000"),
    "S7000 Odd form Insertion Machine  ROHS.jpg": ImageMeta("S7000 odd form insertion machine", "RoHS certification", "S7000"),
    "S7000 Odd form Insertion Machine MD.jpg": ImageMeta("S7000 odd form insertion machine", "CE MD certification", "S7000"),
}


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def source_images() -> list[Path]:
    images: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if "chrome_profile_notebooklm" in path.parts:
            continue
        if OUTPUT_DIR.name in path.parts:
            continue
        if path.name.startswith("~$"):
            continue
        images.append(path)
    return sorted(images, key=lambda item: item.name.lower())


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def convert_to_webp(source: Path, target: Path) -> tuple[int, int]:
    with Image.open(source) as image:
        image.load()
        width, height = image.size
        if image.mode in ("RGBA", "LA") or ("transparency" in image.info):
            background = Image.new("RGBA", image.size, (255, 255, 255, 255))
            background.alpha_composite(image.convert("RGBA"))
            image = background.convert("RGB")
        elif image.mode != "RGB":
            image = image.convert("RGB")
        image.save(target, "WEBP", quality=86, method=6, optimize=True)
    return width, height


def tags_for(meta: ImageMeta) -> list[str]:
    tags = list(SITE_TAGS)
    tags.extend(
        part
        for part in [
            meta.model,
            meta.product,
            meta.certification,
            "CE certificate" if "CE" in meta.certification else None,
            "RoHS certificate" if "RoHS" in meta.certification else None,
            "machine compliance certificate",
        ]
        if part
    )
    seen: set[str] = set()
    result: list[str] = []
    for tag in tags:
        normalized = tag.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(tag)
    return result


def seo_phrase(meta: ImageMeta) -> str:
    product = meta.product
    if meta.model and product.lower().startswith(meta.model.lower()):
        return f"{product} {meta.certification} {BRAND}"
    return f"{meta.model or ''} {product} {meta.certification} {BRAND}"


def smart_title(value: str) -> str:
    replacements = {
        "agv": "AGV",
        "ce": "CE",
        "md": "MD",
        "iso": "ISO",
        "rohs": "RoHS",
        "pcb": "PCB",
        "smt": "SMT",
        "tht": "THT",
        "v-cut": "V-cut",
    }
    titled = value.title()
    for lower, proper in replacements.items():
        titled = re.sub(rf"\b{re.escape(lower)}\b", proper, titled, flags=re.IGNORECASE)
    titled = re.sub(r"\bS(\d{3,5})\b", r"S\1", titled)
    return titled


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    rows: list[dict[str, object]] = []
    slug_counts: dict[str, int] = {}
    missing_meta: list[str] = []

    for source in source_images():
        meta = EXACT_META.get(source.name)
        if meta is None:
            missing_meta.append(source.name)
            stem = re.sub(r"[-_]+", " ", source.stem)
            meta = ImageMeta(stem.strip(), "certification image")

        base_slug = slugify(seo_phrase(meta))
        count = slug_counts.get(base_slug, 0) + 1
        slug_counts[base_slug] = count
        slug = base_slug if count == 1 else f"{base_slug}-{count}"
        target = OUTPUT_DIR / f"{slug}.webp"

        width, height = convert_to_webp(source, target)
        digest = file_sha256(source)
        title = f"{smart_title(meta.product)} {smart_title(meta.certification)} | {BRAND}"
        alt_text = f"{BRAND} {meta.product} {meta.certification} image"
        description_bits = [
            f"{BRAND} {meta.product} {meta.certification} image for PCB assembly equipment reference.",
            "Use this image as certification/compliance material only after confirming the exact model and latest certificate status.",
        ]
        if meta.descriptor:
            description_bits.insert(1, f"Source note: {meta.descriptor}.")
        description = " ".join(description_bits)
        row = {
            "original_name": source.name,
            "original_relative_path": str(source.relative_to(ROOT)).replace("\\", "/"),
            "seo_filename": target.name,
            "webp_relative_path": str(target.relative_to(ROOT)).replace("\\", "/"),
            "title": title,
            "alt_text": alt_text,
            "description": description,
            "tags": ", ".join(tags_for(meta)),
            "model": meta.model or "",
            "product": meta.product,
            "certification": meta.certification,
            "width": width,
            "height": height,
            "original_bytes": source.stat().st_size,
            "webp_bytes": target.stat().st_size,
            "sha256": digest,
            "upload_status": "pending",
            "uploaded_url": "",
            "album": ALBUM_NAME,
        }
        rows.append(row)

    csv_path = OUTPUT_DIR / "seo-webp-manifest.csv"
    json_path = OUTPUT_DIR / "seo-webp-manifest.json"
    summary_path = OUTPUT_DIR / "seo-webp-summary.md"
    fields = list(rows[0].keys()) if rows else []
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=2)

    original_total = sum(int(row["original_bytes"]) for row in rows)
    webp_total = sum(int(row["webp_bytes"]) for row in rows)
    reduction = 0 if original_total == 0 else (1 - webp_total / original_total) * 100
    lines = [
        "# SEO WebP Upload Package",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Source folder: `{ROOT}`",
        f"- Output folder: `{OUTPUT_DIR}`",
        f"- Source images processed: {len(rows)}",
        f"- Original total size: {original_total:,} bytes",
        f"- WebP total size: {webp_total:,} bytes",
        f"- Size reduction: {reduction:.1f}%",
        f"- Album name: `{ALBUM_NAME}`",
        "",
        "## Notes",
        "",
        "- Original images were kept unchanged.",
        "- The `chrome_profile_notebooklm` cache folder was excluded.",
        "- Descriptions and tags are stored in the CSV/JSON manifest and are ready for upload API fields when supported.",
    ]
    if missing_meta:
        lines.extend(["", "## Missing Explicit Metadata", ""])
        lines.extend(f"- {name}" for name in missing_meta)
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "processed": len(rows),
        "output_dir": str(OUTPUT_DIR),
        "manifest_csv": str(csv_path),
        "manifest_json": str(json_path),
        "summary": str(summary_path),
        "original_total": original_total,
        "webp_total": webp_total,
        "reduction_percent": round(reduction, 1),
        "missing_meta": missing_meta,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
