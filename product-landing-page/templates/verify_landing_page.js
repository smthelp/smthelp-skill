#!/usr/bin/env node
/* Headless verification harness for a Southern Machinery product landing page.
 *
 * Usage:
 *   NODE_PATH=/Users/jasonwu/.workbuddy-ai/binaries/node/workspace/node_modules \
 *   /Users/jasonwu/.workbuddy-ai/binaries/node/versions/22.22.2-2/bin/node \
 *     verify_landing_page.js "/abs/path/to/<MODEL>-...-Landing.html"
 *
 * Requires jsdom:  cd /Users/jasonwu/.workbuddy-ai/binaries/node/workspace && npm install jsdom
 *
 * Every check that depends on a feature the page does not have is reported as
 * SKIP rather than FAIL, so the same harness works on a plain English page and
 * on a full 7-language build. Read the SKIP list before signing off — a page
 * that was supposed to have the language layer but shows 20 SKIPs is a defect.
 */
const fs = require("fs");
const { JSDOM } = require("jsdom");

const FILE = process.argv[2];
const CFG_FILE = process.argv[3];   // optional per-page JSON override
if (!FILE) {
  console.error("usage: node verify_landing_page.js <landing-page.html> [config.json]");
  process.exit(2);
}
const html = fs.readFileSync(FILE, "utf8");

/* ------------------------------------------------------------------ config */
const CFG = {
  // Slug used as the jsdom base URL (only affects relative-link resolution).
  baseUrl: "https://smthelp.com/" + FILE.split("/").pop(),

  // Languages the page claims to support. Order matters — it is asserted.
  langs: ["en", "es", "pt", "fr", "ar", "ru", "zh"],
  rtlLangs: ["ar"],

  // localStorage keys. Set to null to skip persistence checks.
  langKey: "s380a_lang",
  themeKey: "s380a_theme",

  // Brand assets that must always be present.
  logo: "https://ph.smthelp.com/images/2024/06/26/Southern-Machinery-logo-300x83.png",

  // Every one of these must appear in a footer href.
  requiredLinks: [
    "https://www.linkedin.com/company/smtmachine",
    "https://cn.linkedin.com/in/smtsupplier",
    "https://twitter.com/smtspecialist",
    "https://www.facebook.com/autoinsertion",
    "https://www.youtube.com/c/Smthelping",
    "https://file.autoinsertion.com",
    "https://ph.smthelp.com"
  ],
  requiredMailto: "mailto:info@smthelp.com",
  whatsapp: /wa\.me\/\d+/,

  // Chatwoot widget.
  chatwoot: { token: null, launcherTitle: null },

  // Long-form article structure. Set postSelector to null to skip.
  // minStepsPerPost is a FLOOR, not an exact count. Articles legitimately vary
  // in length -- an exact-equality check fails on editorial variance and trains
  // you to ignore it. A floor still catches the failure that matters: an article
  // that lost its body (truncated markup, a half-written post).
  postSelector: "details.post",
  minStepsPerPost: 4,
  // Words that must not appear in any heading / summary.
  bannedWords: /\b(hook|diagnosis|framework|vehicle|loop|cta)\b/i,

  // FAQ + structured data.
  faqSelector: ".fqs details",
  faqMin: 6,
  jsonLdTypes: ["Organization", "Product", "FAQPage", "BreadcrumbList"],

  // Images.
  imageHost: "https://ph.smthelp.com/images/",
  minHostImages: 6,

  // i18n DOM hooks. Defaults match the contract in SKILL.md.
  langBtnId: "langBtn",
  langMenuId: "langMenu",
  themeBtnId: "themeBtn",
  themeIconId: "themeIcon",

  // Payback calculator. `inputs` are the field ids to drive, `outputs` maps a
  // short name to the output element id, and `steps` are the arithmetic
  // assertions. Nothing about a specific page's formula is hardcoded here --
  // the previous version baked the S380A conveyor maths (length/feed) into the
  // check text, which made the harness unusable on any other calculator.
  //
  // Work the expected values out by hand from the page's own formula and write
  // them into `re` as a regex, so thousands separators and locale digits do not
  // produce false failures.
  calc: {
    inputs: { cOp: "2", cSal: "9000", cPanel: "6000", cLen: "1200", cFeed: "30", cHrs: "8", cDays: "25", cPrice: "45000" },
    outputs: { perPanel: "rPerPanel", labour: "rLabour", machHrs: "rMachHrs", payback: "rPayback", paybackUnit: "rPaybackU", slack: "rSlack" },
    // secPerPanel = 1200/30 = 40.0 s
    // machine hours/month = 6000 * 40 / 3600 = 66.7 h
    // labour replaced/year = 2 * 9000 = 18,000
    // payback = 45000 / (18000/12) = 30 months = 2.5 years
    steps: [
      { out: "perPanel", re: /40\.0/, label: "cut time per panel = length / feed (40.0 s)" },
      { out: "labour",   re: /18[.,]?\s?000/, label: "labour replaced per year = operators x salary (18,000)" },
      { out: "machHrs",  re: /66\.7/, label: "machine hours per month (66.7 h)" },
      { out: "payback",  re: /2\.5/, label: "payback = price / (labourYear/12) (2.5 years)" }
    ],
    // Degenerate inputs must not print Infinity / NaN.
    degenerate: [
      { label: "zero investment shows a prompt, not Infinity/NaN", set: { cPrice: "0" }, watch: "payback" },
      { label: "zero labour shows a prompt, not Infinity/NaN", set: { cOp: "0", cSal: "0" }, watch: "payback" },
      { label: "absurd feed does not crash the per-unit figure", set: { cFeed: "99999" }, watch: "perPanel" }
    ],
    // A key the renderer writes but which never appears in the markup.
    keyLeakPattern: /^(unit_|calc_)[a-z0-9_]+$/
  },

  // Non-hero images should be lazy-loaded. Images exempt from this rule:
  //   - the brand logo (header AND footer, matched by exact src)
  //   - anything with fetchpriority="high" (a deliberate above-the-fold hero)
  //   - anything inside <header>
  // A naive "every img except the hero is lazy" check false-positives on all
  // three, which is how a harness loses its credibility.
  expectLazyImages: true
};

/* ------------------------------------------------- per-page JSON override */
// A second CLI argument points at a JSON file whose keys deep-merge into CFG.
// This is what makes the harness reusable: the page-specific ids, storage keys,
// Chatwoot token and calculator arithmetic live in a config file next to the
// page, not in this script. JSON has no regex literal, so any string that looks
// like /.../flags is revived into a RegExp.
const REGEXISH = /^\/(.+)\/([gimsuy]*)$/;
function revive(v) {
  if (typeof v === "string") {
    const m = v.match(REGEXISH);
    if (m) { try { return new RegExp(m[1], m[2]); } catch (e) { return v; } }
    return v;
  }
  if (Array.isArray(v)) return v.map(revive);
  if (v && typeof v === "object") {
    const out = {};
    for (const k of Object.keys(v)) out[k] = revive(v[k]);
    return out;
  }
  return v;
}
function deepMerge(base, over) {
  for (const k of Object.keys(over)) {
    const b = base[k], o = over[k];
    if (b && o && typeof b === "object" && typeof o === "object" &&
        !Array.isArray(b) && !Array.isArray(o) && !(b instanceof RegExp)) {
      deepMerge(b, o);
    } else {
      base[k] = o;
    }
  }
  return base;
}
if (CFG_FILE) {
  if (!fs.existsSync(CFG_FILE)) {
    console.error("config file not found: " + CFG_FILE);
    process.exit(2);
  }
  let over;
  try { over = JSON.parse(fs.readFileSync(CFG_FILE, "utf8")); }
  catch (e) { console.error("config file is not valid JSON: " + e.message); process.exit(2); }
  deepMerge(CFG, revive(over));
  console.log("config: " + CFG_FILE);
}

/* ---------------------------------------------------------------- helpers */
// Rough display-width estimator for SERP truncation. Google truncates on pixel
// width (~600px for titles), not character count, so a plain .length check is
// wrong in both directions: it flags keyword-dense Latin titles that fit, and
// it passes CJK titles that are actually twice as wide. Calibrated 2026-09-18
// against real SERP behaviour: latin title <= 60 units, CJK title <= 60 units.
function displayWidth(s) {
  const NARROW = "iljtfrI.,'!|:;()[]-/ ";
  let w = 0;
  for (const ch of s) {
    const cp = ch.codePointAt(0);
    const wide = (cp >= 0x1100 && cp <= 0x115f) || (cp >= 0x2e80 && cp <= 0xa4cf) ||
                 (cp >= 0xac00 && cp <= 0xd7a3) || (cp >= 0xf900 && cp <= 0xfaff) ||
                 (cp >= 0xfe30 && cp <= 0xfe6f) || (cp >= 0xff00 && cp <= 0xff60) ||
                 (cp >= 0xffe0 && cp <= 0xffe6);
    if (wide) w += 2;
    else if (NARROW.includes(ch)) w += 0.5;
    else if (ch !== ch.toLowerCase()) w += 1.15;
    else w += 1;
  }
  return w;
}
const TITLE_LIMIT = 60, DESC_LIMIT = 160;

/* ----------------------------------------------------------------- harness */
function boot(url, storage) {
  return new JSDOM(html, {
    url: url || CFG.baseUrl,
    runScripts: "dangerously",
    pretendToBeVisual: true,
    beforeParse(win) {
      // Keep the test offline: no Chatwoot SDK, no YouTube, no analytics.
      win.fetch = () => Promise.reject(new Error("offline"));
      if (storage) Object.keys(storage).forEach(k => win.localStorage.setItem(k, storage[k]));
    }
  });
}

let failures = 0, skips = 0;
function check(name, ok, detail) {
  console.log((ok ? "  PASS  " : "  FAIL  ") + name + (detail ? "  -> " + detail : ""));
  if (!ok) failures++;
}
function skip(name, why) {
  console.log("  SKIP  " + name + (why ? "  -> " + why : ""));
  skips++;
}
function group(n, title) { console.log("\n=== " + n + ". " + title + " ==="); }
const txt = el => ((el && el.textContent) || "").trim();
const attr = (el, a) => (el ? el.getAttribute(a) : null);
const byId = (d, id) => d.getElementById(id);

/* -------------------------------------------------------------- 1. boot */
group(1, "boot");
const dom = boot();
const win = dom.window, doc = win.document;

check("page parses and has a title", !!doc.title, doc.title.slice(0, 70));
const logoImg = doc.querySelector("header img, .brand img, header .logo img");
check("header logo present", !!logoImg);
check("logo src is the required brand asset", logoImg && logoImg.getAttribute("src") === CFG.logo, logoImg ? logoImg.getAttribute("src") : "");
check(`title fits the SERP width budget (<= ${TITLE_LIMIT} units)`, displayWidth(doc.title) <= TITLE_LIMIT,
  displayWidth(doc.title).toFixed(1) + " units / " + doc.title.length + " chars");
const desc = doc.querySelector('meta[name="description"]');
check(`meta description present and within ${DESC_LIMIT} units`, !!desc && displayWidth(desc.getAttribute("content")) <= DESC_LIMIT,
  desc ? displayWidth(desc.getAttribute("content")).toFixed(1) + " units / " + desc.getAttribute("content").length + " chars" : "missing");
const canonical = doc.querySelector('link[rel="canonical"]');
check("canonical link present", !!canonical, attr(canonical, "href") || "missing");

/* ------------------------------------------------------ 2. i18n coverage */
const hasI18n = typeof win.applyLang === "function" && doc.querySelectorAll("[data-i18n]").length > 0;
const LANG_CODES = doc.querySelectorAll("#" + CFG.langMenuId + " button").length
  ? Array.from(doc.querySelectorAll("#" + CFG.langMenuId + " button")).map(b => b.getAttribute("data-lang"))
  : CFG.langs;

group(2, "i18n: every language renders real text, never a raw key");
if (!hasI18n) {
  skip("all i18n checks", "page has no applyLang() / data-i18n layer");
} else {
  const titles = {};
  // Always evaluate English first — later languages are compared against it.
  const ORDER = ["en", ...LANG_CODES.filter(c => c !== "en")];
  for (const L of ORDER) {
    win.applyLang(L, false);
    const badText = [], badPh = [], badTitle = [];
    doc.querySelectorAll("[data-i18n]").forEach(el => {
      const k = el.getAttribute("data-i18n");
      const t = txt(el);
      if (!t || t === k) badText.push(k);
    });
    doc.querySelectorAll("[data-i18n-ph]").forEach(el => {
      const k = el.getAttribute("data-i18n-ph");
      const t = (el.getAttribute("placeholder") || "").trim();
      if (!t || t === k) badPh.push(k);
    });
    doc.querySelectorAll("[data-i18n-title]").forEach(el => {
      const k = el.getAttribute("data-i18n-title");
      const t = (el.getAttribute("title") || "").trim();
      if (!t || t === k) badTitle.push(k);
    });
    const dir = doc.documentElement.getAttribute("dir");
    check(`${L}: all data-i18n elements resolved`, badText.length === 0, badText.length ? badText.slice(0, 8).join(", ") + ` (+${Math.max(0, badText.length - 8)} more)` : `${doc.querySelectorAll("[data-i18n]").length} keys`);
    if (doc.querySelectorAll("[data-i18n-ph]").length) check(`${L}: placeholders resolved`, badPh.length === 0, badPh.slice(0, 5).join(", "));
    if (doc.querySelectorAll("[data-i18n-title]").length) check(`${L}: title attributes resolved`, badTitle.length === 0, badTitle.slice(0, 5).join(", "));
    check(`${L}: <html lang> is set`, doc.documentElement.getAttribute("lang") === L, doc.documentElement.getAttribute("lang"));
    const wantDir = CFG.rtlLangs.includes(L) ? "rtl" : "ltr";
    check(`${L}: dir is ${wantDir}`, dir === wantDir, dir);
    check(`${L}: SEO title localised`, !!doc.title && doc.title.length > 20, doc.title.slice(0, 60));
    check(`${L}: SEO title fits the width budget`, displayWidth(doc.title) <= TITLE_LIMIT, displayWidth(doc.title).toFixed(1) + " units");
    const mdEl = doc.querySelector('meta[name="description"]');
    check(`${L}: meta description fits the width budget`, !!mdEl && displayWidth(mdEl.getAttribute("content")) <= DESC_LIMIT,
      mdEl ? displayWidth(mdEl.getAttribute("content")).toFixed(1) + " units" : "missing");
    if (L !== "en") check(`${L}: SEO title actually differs from English`, doc.title !== titles.en, doc.title.slice(0, 45));
    titles[L] = doc.title;
  }
}

/* ------------------------------------- 3. translated copy is not English */
group(3, "spot-check that translated copy is actually translated");
if (!hasI18n) {
  skip("translation spot-checks", "no i18n layer");
} else {
  const SCRIPT = {
    zh: /[\u4e00-\u9fff]/, ru: /[\u0400-\u04FF]/, ar: /[\u0600-\u06FF]/,
    es: /[áéíóúñ¿¡]|ción|para|más/i, pt: /[ãõçáéíóú]|ção|para|mais/i, fr: /[àâçéèêëîïôùû]|pour|avec/i
  };
  for (const L of ["zh", "ru", "ar", "es", "pt", "fr"]) {
    if (!LANG_CODES.includes(L)) { skip(`${L}: translation spot-check`, "language not enabled"); continue; }
    win.applyLang(L, false);
    const els = Array.from(doc.querySelectorAll("[data-i18n]"))
      .map(txt).filter(t => t && t.length > 12);
    const sample = els.slice(0, 40).join(" ");
    const re = SCRIPT[L];
    check(`${L}: sample copy shows ${L} orthography`, re.test(sample), els.slice(0, 1).join("").slice(0, 55) || "no long strings found");
  }
  win.applyLang("en", false);
}

/* ------------------------------------------------------------ 4. videos */
group(4, "video grid");
const vids = doc.querySelectorAll("[data-vid]");
if (!vids.length) {
  skip("video checks", "no [data-vid] cards found");
} else {
  check(`${vids.length} video card(s) rendered`, vids.length >= 2, String(vids.length));
  let thumbOk = true, thumbBad = null, titleOk = true, lazyOk = true, frameOk = true;
  vids.forEach(c => {
    const img = c.querySelector("img");
    const src = img ? img.getAttribute("src") : "";
    if (!/^https:\/\/i\.ytimg\.com\/vi\/[\w-]+\/hqdefault\.jpg$/.test(src)) { thumbOk = false; thumbBad = src; }
    if (img && img.getAttribute("loading") !== "lazy") lazyOk = false;
    const h = c.querySelector("h3, h4, .t");
    const t = txt(h);
    if (!t || /^[a-z0-9_]+$/.test(t)) titleOk = false;
    if (c.querySelector("iframe")) frameOk = false; // iframes must be injected on click, not eagerly
  });
  check("all thumbnails use i.ytimg.com/vi/<id>/hqdefault.jpg", thumbOk, thumbBad || "");
  check("video titles are real text, not keys", titleOk);
  check("video thumbnails are lazy-loaded", lazyOk);
  check("no eager <iframe> in the grid (privacy + weight)", frameOk);
}

/* ------------------------------------------------------ 5. theme toggle */
group(5, "theme toggle");
const themeBtn = byId(doc, CFG.themeBtnId);
if (!themeBtn || !CFG.themeKey) {
  skip("theme checks", "no theme toggle on the page");
} else {
  const icon = byId(doc, CFG.themeIconId);
  if (icon) check("theme icon shows a sun or moon", ["☀", "☾", "🌙", "☀️"].includes(txt(icon)), txt(icon));
  const before = doc.documentElement.getAttribute("data-theme");
  themeBtn.dispatchEvent(new win.MouseEvent("click", { bubbles: true }));
  const after = doc.documentElement.getAttribute("data-theme");
  check("clicking the toggle flips data-theme", before !== after, before + " -> " + after);
  check("theme stored in localStorage", win.localStorage.getItem(CFG.themeKey) === after, String(win.localStorage.getItem(CFG.themeKey)));
  const tc = doc.querySelector('meta[name="theme-color"]');
  check("theme-color meta is updated", !!tc && tc.getAttribute("content") !== "", tc ? tc.getAttribute("content") : "missing");
  themeBtn.dispatchEvent(new win.MouseEvent("click", { bubbles: true }));
  check("toggling back restores the original value", doc.documentElement.getAttribute("data-theme") === before);
}

/* ------------------------------------------------- 6. persistence/reload */
group(6, "persistence across a reload and ?lang= override");
if (!hasI18n || !CFG.langKey) {
  skip("persistence checks", "no i18n / storage keys configured");
} else {
  const dom2 = boot(undefined, { [CFG.langKey]: "fr", [CFG.themeKey]: "dark" });
  check("stored language applied on load", dom2.window.document.documentElement.getAttribute("lang") === "fr", dom2.window.document.documentElement.getAttribute("lang"));
  if (CFG.themeKey) check("stored theme applied on load", dom2.window.document.documentElement.getAttribute("data-theme") === "dark", dom2.window.document.documentElement.getAttribute("data-theme"));
  const dom3 = boot(CFG.baseUrl + "?lang=zh", { [CFG.langKey]: "fr" });
  check("?lang= overrides the stored preference", dom3.window.document.documentElement.getAttribute("lang") === "zh", dom3.window.document.documentElement.getAttribute("lang"));
  const dom4 = boot(CFG.baseUrl + "?lang=xx", { [CFG.langKey]: "fr" });
  check("unknown ?lang= falls back instead of breaking", dom4.window.document.documentElement.getAttribute("lang") !== "xx", dom4.window.document.documentElement.getAttribute("lang"));
}

/* --------------------------------------------------------- 7. calculator */
group(7, "payback calculator arithmetic");
const calcFn = win.calc;
if (!calcFn || !CFG.calc) {
  skip("calculator checks", "no window.calc() on the page");
} else {
  Object.keys(CFG.calc.inputs).forEach(id => { const el = byId(doc, id); if (el) el.value = CFG.calc.inputs[id]; });
  calcFn();
  const got = {};
  Object.keys(CFG.calc.outputs).forEach(k => { got[k] = txt(byId(doc, CFG.calc.outputs[k])); });
  (CFG.calc.steps || []).forEach(s => {
    check(s.label, s.re.test(got[s.out] || ""), (got[s.out] || "(empty)"));
  });
  (CFG.calc.degenerate || []).forEach(c => {
    Object.keys(c.set).forEach(id => { const el = byId(doc, id); if (el) el.value = c.set[id]; });
    calcFn();
    const v = txt(byId(doc, CFG.calc.outputs[c.watch]));
    check(c.label, !/Infinity|NaN/.test(v), v || "(empty)");
    Object.keys(c.set).forEach(id => {
      const el = byId(doc, id);
      if (el && CFG.calc.inputs[id] !== undefined) el.value = CFG.calc.inputs[id];
    });
    calcFn();
  });
}

/* --------------------------- 7b. calculator localisation (the key-leak bug) */
group("7b", "calculator units and prompts are localised, never raw keys");
if (!hasI18n || !calcFn || !CFG.calc) {
  skip("calculator localisation", "no i18n layer or calculator");
} else {
  const KEYLIKE = CFG.calc.keyLeakPattern;
  for (const L of LANG_CODES) {
    win.applyLang(L, false);
    Object.keys(CFG.calc.inputs).forEach(id => { const el = byId(doc, id); if (el) el.value = CFG.calc.inputs[id]; });
    calcFn();
    const cells = Object.keys(CFG.calc.outputs).map(k => txt(byId(doc, CFG.calc.outputs[k]))).filter(Boolean);
    const leaked = cells.filter(t => KEYLIKE.test(t));
    check(`${L}: no raw key in calculator output`, leaked.length === 0, leaked.join(" | ") || cells.join(" | "));
  }
  win.applyLang("en", false);
}

/* ----------------------------------------------------- 8. language menu */
group(8, "language menu and persistence");
if (!hasI18n) {
  skip("language menu checks", "no i18n layer");
} else {
  const menu = doc.querySelectorAll("#" + CFG.langMenuId + " button");
  if (menu.length) {
    check(`language menu has ${CFG.langs.length} entries`, menu.length === CFG.langs.length, String(menu.length));
    const codes = Array.from(menu).map(b => b.getAttribute("data-lang")).join(",");
    check(`menu order is ${CFG.langs.join(",")}`, codes === CFG.langs.join(","), codes);
    check("the active language is marked aria-current", !!doc.querySelector('#' + CFG.langMenuId + ' button[aria-current="true"]'));
  } else skip("language menu checks", "no #" + CFG.langMenuId);
  if (CFG.langKey) {
    win.applyLang("pt", true);
    check("applyLang persists the choice", win.localStorage.getItem(CFG.langKey) === "pt", String(win.localStorage.getItem(CFG.langKey)));
  }
}

/* -------------------------------------------------------- 9. required links */
group(9, "required links, contact block and support widget");
const footerLinks = Array.from(doc.querySelectorAll("footer a, .fg a, .soc a")).map(a => a.getAttribute("href"));
CFG.requiredLinks.forEach(u => check("links " + u, footerLinks.includes(u)));
check("mailto " + CFG.requiredMailto, footerLinks.includes(CFG.requiredMailto), CFG.requiredMailto);
check("WhatsApp deep link present", footerLinks.some(h => h && CFG.whatsapp.test(h)));
const allHtml = doc.documentElement.outerHTML;
if (CFG.chatwoot.token) {
  check("Chatwoot snippet present with the configured token", allHtml.includes("chatwootSDK.run") && allHtml.includes(CFG.chatwoot.token));
  check("Chatwoot launcher title preserved", !CFG.chatwoot.launcherTitle || allHtml.includes(CFG.chatwoot.launcherTitle));
  check("Chatwoot CSS pins the launcher bottom-right", allHtml.includes(".woot-widget-holder"));
  check("Chatwoot base URL follows the page protocol (no mixed content)",
    !/BASE_URL\s*=\s*["']http:\/\/chat\./.test(allHtml) || /location\.protocol/.test(allHtml));
} else {
  skip("Chatwoot checks", "CFG.chatwoot.token not set for this page");
}

/* --------------------------------------------------- 10. content integrity */
group(10, "content integrity");
// Reset to English so the banned-word and structure scans are deterministic.
if (typeof win.applyLang === "function") win.applyLang("en", false);
if (CFG.postSelector) {
  const posts = doc.querySelectorAll(CFG.postSelector);
  if (!posts.length) skip("long-form article checks", "no " + CFG.postSelector);
  else {
    check(`${posts.length} long-form article(s) present`, posts.length >= 1, String(posts.length));
    let thin = null, total = 0;
    const counts = [];
    posts.forEach((p, i) => {
      const n = p.querySelectorAll(".step").length;
      total += n; counts.push(n);
      if (n < CFG.minStepsPerPost) thin = `article ${i + 1} has only ${n}`;
    });
    check(`every article has at least ${CFG.minStepsPerPost} body sections`, thin === null,
      thin || `per article: ${counts.join(", ")} (total ${total})`);
    // Articles must be in the DOM, not fetched, so the file works offline.
    check("article bodies are inline, not fetched", !/fetch\(|XMLHttpRequest/.test(allHtml.replace(/chatwoot[\s\S]{0,400}/g, "")));
  }
}
let bannedHit = null;
doc.querySelectorAll("h1,h2,h3,h4,h5,summary,title").forEach(el => {
  const t = txt(el);
  if (t && CFG.bannedWords.test(t)) bannedHit = t.slice(0, 70);
});
check("no banned word in any heading / summary / title", bannedHit === null, bannedHit || "");
if (CFG.faqSelector) {
  const faq = doc.querySelectorAll(CFG.faqSelector);
  check(`at least ${CFG.faqMin} FAQ entries`, faq.length >= CFG.faqMin, String(faq.length));
}
const ldEl = doc.querySelector('script[type="application/ld+json"]');
if (!ldEl) {
  skip("structured data checks", "no JSON-LD block");
} else {
  let ld = null;
  try { ld = JSON.parse(ldEl.textContent); } catch (e) { check("JSON-LD parses", false, e.message); }
  if (ld) {
    const nodes = ld["@graph"] || [ld];
    const types = nodes.map(n => n["@type"]);
    check("JSON-LD has " + CFG.jsonLdTypes.join(", "), CFG.jsonLdTypes.every(t => types.includes(t)), types.join(","));
    const faqLd = nodes.find(n => n["@type"] === "FAQPage");
    const visibleFaq = CFG.faqSelector ? doc.querySelectorAll(CFG.faqSelector).length : 0;
    if (faqLd) check("FAQPage question count matches the visible FAQ", faqLd.mainEntity.length === visibleFaq, `${faqLd.mainEntity.length} vs ${visibleFaq} visible`);
    const prod = nodes.find(n => n["@type"] === "Product");
    if (prod) check("Product carries specs as additionalProperty", Array.isArray(prod.additionalProperty) && prod.additionalProperty.length > 0, String((prod.additionalProperty || []).length));
  }
}
check("hreflang alternates present (x-default included)", !!doc.querySelector('link[rel="alternate"][hreflang="x-default"]'),
  String(doc.querySelectorAll('link[rel="alternate"][hreflang]').length) + " alternates");

/* ------------------------------------------------------------- 11. images */
group(11, "images");
const imgs = Array.from(doc.querySelectorAll("img")).map(i => i.getAttribute("src")).filter(Boolean);
const hostImgs = imgs.filter(s => s.startsWith(CFG.imageHost));
check(`at least ${CFG.minHostImages} images served from ${CFG.imageHost}`, hostImgs.length >= CFG.minHostImages, String(hostImgs.length));
check("no base64 placeholder images", imgs.filter(s => s.startsWith("data:")).length === 0);
check("every <img> has alt text", Array.from(doc.querySelectorAll("img")).every(i => i.hasAttribute("alt")));
if (CFG.expectLazyImages) {
  const exempt = i => {
    const src = i.getAttribute("src") || "";
    if (src === CFG.logo) return true;                          // brand logo, header or footer
    if (i.getAttribute("fetchpriority") === "high") return true; // deliberate above-the-fold hero
    if (i.closest("header")) return true;                        // nothing above the fold
    return false;
  };
  const all = Array.from(doc.querySelectorAll("img"));
  const culprits = all.filter(i => !exempt(i) && i.getAttribute("loading") !== "lazy");
  check("below-the-fold images are lazy-loaded", culprits.length === 0,
    culprits.slice(0, 4).map(i => (i.getAttribute("src") || "").split("/").pop()).join(", ") ||
    `${all.length - culprits.length}/${all.length} lazy or exempt`);
}

/* ---------------------------------------------------------------- result */
console.log("\n=== RESULT ===");
console.log(failures === 0 ? "ALL CHECKS PASSED" : failures + " CHECK(S) FAILED");
if (skips) console.log(skips + " check(s) skipped — confirm each skip is expected for this page");
process.exit(failures === 0 ? 0 : 1);
