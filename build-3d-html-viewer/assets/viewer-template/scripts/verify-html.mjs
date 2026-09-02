import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const root = path.resolve(import.meta.dirname, "..");
const config = JSON.parse(fs.readFileSync(path.join(root, "viewer-config.json"), "utf8").replace(/^\uFEFF/, ""));
const outputSlug = (config.outputSlug || "product-interactive-3d-viewer")
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, "-")
  .replace(/^-+|-+$/g, "");
const htmlPath = path.join(root, "dist", `${outputSlug}.html`);
const artifactsDir = path.resolve(root, "..", "playwright", outputSlug);

fs.mkdirSync(artifactsDir, { recursive: true });

const browser = await chromium.launch({ headless: true });

async function inspectViewport(name, width, height) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "domcontentloaded" });
  await page.waitForSelector("canvas", { state: "attached", timeout: 15000 });
  await page.waitForTimeout(1600);

  const inspection = await page.evaluate(() => {
    const canvas = document.querySelector("canvas");
    if (!canvas) return { hasCanvas: false };
    const gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
    const rect = canvas.getBoundingClientRect();
    const result = {
      hasCanvas: true,
      canvasCssWidth: Math.round(rect.width),
      canvasCssHeight: Math.round(rect.height),
      drawingWidth: canvas.width,
      drawingHeight: canvas.height,
      nonBackgroundPixels: 0,
      distinctBuckets: 0,
      logoPresent: Boolean(document.querySelector(".brand img")),
      footerLinks: Array.from(document.querySelectorAll(".footer-links a")).length,
      title: document.querySelector("h1")?.textContent || "",
      toolButtons: Array.from(document.querySelectorAll(".tool-button")).map((button) => button.textContent?.trim())
    };
    if (!gl) return { ...result, hasWebgl: false };
    const sampleW = Math.min(180, canvas.width);
    const sampleH = Math.min(140, canvas.height);
    const startX = Math.max(0, Math.floor((canvas.width - sampleW) / 2));
    const startY = Math.max(0, Math.floor((canvas.height - sampleH) / 2));
    const pixels = new Uint8Array(sampleW * sampleH * 4);
    gl.readPixels(startX, startY, sampleW, sampleH, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
    const buckets = new Set();
    for (let i = 0; i < pixels.length; i += 4) {
      const r = pixels[i];
      const g = pixels[i + 1];
      const b = pixels[i + 2];
      const a = pixels[i + 3];
      const looksLikeBackground = Math.abs(r - 245) < 12 && Math.abs(g - 243) < 12 && Math.abs(b - 239) < 12;
      if (a > 0 && !looksLikeBackground) result.nonBackgroundPixels += 1;
      buckets.add(`${r >> 4}-${g >> 4}-${b >> 4}`);
    }
    result.distinctBuckets = buckets.size;
    return { ...result, hasWebgl: true };
  });

  await page.screenshot({
    path: path.join(artifactsDir, `${name}.png`),
    fullPage: true
  });

  await page.getByRole("button", { name: /Wire/i }).click();
  await page.waitForTimeout(600);
  const afterWire = await page.evaluate(() => {
    const canvas = document.querySelector("canvas");
    const gl = canvas?.getContext("webgl2") || canvas?.getContext("webgl");
    if (!canvas || !gl) return { ok: false };
    const pixels = new Uint8Array(80 * 80 * 4);
    gl.readPixels(Math.max(0, Math.floor(canvas.width / 2 - 40)), Math.max(0, Math.floor(canvas.height / 2 - 40)), 80, 80, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
    let marked = 0;
    for (let i = 0; i < pixels.length; i += 4) {
      if (pixels[i + 3] > 0 && (pixels[i] < 230 || pixels[i + 1] < 230 || pixels[i + 2] < 230)) marked += 1;
    }
    return { ok: marked > 100, marked };
  });

  await page.close();
  return { viewport: { name, width, height }, inspection, afterWire };
}

const desktop = await inspectViewport("desktop-1440x900", 1440, 900);
const mobile = await inspectViewport("mobile-390x844", 390, 844);
await browser.close();

const report = {
  htmlPath,
  artifactsDir,
  desktop,
  mobile
};

fs.writeFileSync(path.join(artifactsDir, "verification-report.json"), JSON.stringify(report, null, 2), "utf8");
console.log(JSON.stringify(report, null, 2));
