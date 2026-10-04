import fs from "node:fs";
import path from "node:path";
import * as esbuild from "esbuild";

const root = path.resolve(import.meta.dirname, "..");
const srcDir = path.join(root, "src");
const distDir = path.join(root, "dist");
const tempBundle = path.join(distDir, "app.bundle.js");
const config = JSON.parse(fs.readFileSync(path.join(root, "viewer-config.json"), "utf8").replace(/^\uFEFF/, ""));
const outputSlug = (config.outputSlug || "product-interactive-3d-viewer")
  .toLowerCase()
  .replace(/[^a-z0-9]+/g, "-")
  .replace(/^-+|-+$/g, "");
const outHtml = path.join(distDir, `${outputSlug}.html`);

function dataUri(filePath, mime) {
  const bytes = fs.readFileSync(filePath);
  return `data:${mime};base64,${bytes.toString("base64")}`;
}

function base64Asset(filePath, mime) {
  return {
    name: path.basename(filePath),
    mime,
    base64: fs.readFileSync(filePath).toString("base64")
  };
}

function cleanMeta(value) {
  return String(value || "").replace(/[<>&"]/g, "");
}

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderStaticShell() {
  const footerLinks = Array.isArray(config.footerLinks) ? config.footerLinks : [];
  const marketingTiles = Array.isArray(config.marketingTiles) ? config.marketingTiles : [];
  const rfqItems = Array.isArray(config.rfqItems) ? config.rfqItems : [];
  return `<div class="site-shell static-shell" data-priority-text="true">
    <header class="site-header">
      <a class="brand" href="${escapeHtml(config.brand?.url || "https://www.smthelp.com")}" target="_blank" rel="noreferrer">
        <img src="${generatedAssets.logoDataUri}" alt="${escapeHtml(config.brand?.name || "Southern Machinery")} logo">
      </a>
      <nav class="header-actions" aria-label="Primary actions">
        <a href="${escapeHtml(config.catalogUrl || config.brand?.catalogUrl || "https://file.autoinsertion.com")}" target="_blank" rel="noreferrer">Catalog</a>
      </nav>
    </header>
    <main class="viewer-stage">
      <section class="product-panel" aria-label="Product overview">
        <div class="eyebrow"><span>${escapeHtml(config.companySlogan || "Specialized in design and manufacturing SMT THT machine for smart EMS Factory")}</span></div>
        <h1>${escapeHtml(config.productTitle || "Product Interactive 3D Viewer")}</h1>
        <p>${escapeHtml(config.sourceNotice || config.description || "")}</p>
        <div class="stats-strip marketing-tiles">
          ${marketingTiles
            .map((item) => `<article class="marketing-tile"><strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.text)}</span></article>`)
            .join("")}
        </div>
      </section>
      <section class="tool-panel static-loading" aria-label="3D loading status">
        <strong>3D model loading</strong>
        <span>Product text is available first. The optimized model opens in staged sections.</span>
      </section>
      <aside class="source-panel rfq-panel" aria-label="Required RFQ information">
        <div class="rfq-heading">
          <strong>RFQ Required Information</strong>
          <span>${escapeHtml(config.rfqIntro || "For this product quotation, please provide these details first.")}</span>
        </div>
        <div class="rfq-grid">
          ${rfqItems
            .map((item) => `<article class="rfq-item"><div><strong>${escapeHtml(item.label)}</strong></div><p>${escapeHtml(item.text)}</p></article>`)
            .join("")}
        </div>
      </aside>
    </main>
    <footer class="site-footer">
      <div class="footer-inner">
        <strong>Connect with Southern Machinery</strong>
        <div class="footer-links">
          ${footerLinks.map(([label, url]) => `<a href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`).join("")}
        </div>
        <p>Browse our machine catalog at <a href="${escapeHtml(config.brand?.catalogUrl || "https://file.autoinsertion.com")}" target="_blank" rel="noreferrer">file.autoinsertion.com</a> and find machine photos at <a href="${escapeHtml(config.photoUrl || "https://ph.smthelp.com")}" target="_blank" rel="noreferrer">ph.smthelp.com</a>.</p>
      </div>
    </footer>
  </div>`;
}

fs.mkdirSync(distDir, { recursive: true });

const generatedAssets = {
  logoDataUri: dataUri(path.join(root, "assets", config.logoFile || "southern-machinery-logo.png"), "image/png"),
  viewerConfig: config,
  downloads: {},
  groundImages: []
};

if (config.source?.step && config.performance?.embedStepDownload !== false) {
  generatedAssets.downloads.step = base64Asset(path.join(root, "assets", config.source.step), "model/step");
}
if (config.source?.pdf) {
  generatedAssets.downloads.pdf = base64Asset(path.join(root, "assets", config.source.pdf), "application/pdf");
}
if (config.source?.native) {
  generatedAssets.downloads.native = base64Asset(path.join(root, "assets", config.source.native), "application/octet-stream");
}
if (Array.isArray(config.groundImages)) {
  generatedAssets.groundImages = config.groundImages
    .filter((item) => item?.file)
    .map((item) => ({
      label: item.label || path.basename(item.file),
      sourceUrl: item.sourceUrl || "",
      dataUri: dataUri(path.join(root, "assets", item.file), item.mime || "image/png")
    }));
}

fs.writeFileSync(
  path.join(srcDir, "generated-assets.ts"),
  `/* Auto-generated by scripts/build-single-html.mjs. */\nexport const logoDataUri = ${JSON.stringify(generatedAssets.logoDataUri)};\nexport const viewerConfig = ${JSON.stringify(generatedAssets.viewerConfig)};\nexport const downloads = ${JSON.stringify(generatedAssets.downloads)};\nexport const groundImages = ${JSON.stringify(generatedAssets.groundImages)};\n`,
  "utf8"
);

await esbuild.build({
  entryPoints: [path.join(srcDir, "main.tsx")],
  bundle: true,
  minify: true,
  sourcemap: false,
  format: "iife",
  target: ["es2020"],
  outfile: tempBundle,
  legalComments: "none",
  logLevel: "info"
});

const css = fs.readFileSync(path.join(srcDir, "styles.css"), "utf8");
const js = fs.readFileSync(tempBundle, "utf8");
const safeJs = js.replace(/<\/script/gi, "<\\/script");
const safeTitle = cleanMeta(config.productTitle || "Product Interactive 3D Viewer");
const safeDescription = cleanMeta(config.description || "Interactive 3D product viewer.");
const lazy3dBoot = config.performance?.lazy3dBoot !== false;
const scriptMarkup = lazy3dBoot
  ? `<script type="text/plain" id="app-js">${safeJs}</script>
  <script>
    window.setTimeout(function () {
      var payload = document.getElementById("app-js");
      if (!payload) return;
      var script = document.createElement("script");
      script.text = payload.textContent || "";
      document.body.appendChild(script);
    }, 80);
  </script>`
  : `<script>${safeJs}</script>`;

const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <title>${safeTitle} | Southern Machinery</title>
  <meta name="description" content="${safeDescription}">
  <meta name="keywords" content="Southern Machinery, SMThelp, SMT equipment, THT equipment, CAD viewer, interactive 3D, STEP viewer, WordPress single HTML">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${safeTitle}">
  <meta property="og:description" content="${safeDescription}">
  <meta name="theme-color" content="#f5f3ef">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": ${JSON.stringify(safeTitle)},
    "brand": {"@type": "Brand", "name": "Southern Machinery"},
    "category": ${JSON.stringify(config.category || "SMT/THT product visual reference")},
    "description": ${JSON.stringify(safeDescription)},
    "isRelatedTo": {
      "@type": "Organization",
      "name": "Southern Machinery",
      "url": "https://www.smthelp.com"
    }
  }
  </script>
  <style>${css}</style>
</head>
<body>
  <div id="root">${renderStaticShell()}</div>
  <noscript>This interactive 3D viewer needs JavaScript enabled.</noscript>
  ${scriptMarkup}
</body>
</html>
`;

fs.writeFileSync(outHtml, html, "utf8");
fs.copyFileSync(outHtml, path.join(root, `${outputSlug}-wordpress.html`));

const stats = fs.statSync(outHtml);
console.log(JSON.stringify({
  output: outHtml,
  bytes: stats.size,
  copiedTo: path.join(root, `${outputSlug}-wordpress.html`)
}, null, 2));
