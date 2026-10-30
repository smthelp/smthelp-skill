---
name: nextjs-website-clone-workflow
description: Next.js 15 + React 18 website cloning workflow — pixel-perfect clone of B2B marketing sites using Next.js App Router, shadcn/ui, Tailwind CSS v4, and TypeScript. Covers project initialization, design token extraction, component architecture, sub-page building, and common Next.js 15 build errors. Use when asked to clone a website into a Next.js project, scaffold a B2B marketing site with shadcn/ui, or troubleshoot Next.js App Router build failures.
argument-hint: "<target-url> or <project-path>"
user-invocable: true
---

# Next.js Website Clone Workflow

Class-level workflow for cloning/intercepting a B2B marketing website into a Next.js 15 + shadcn/ui project. Captures the full pipeline from zero to live, including design token extraction, component architecture, sub-page routing, and known Next.js 15 pitfalls specific to this environment (macOS ARM64 + Hermes).

## When to Use

- User says: "clone", "rebuild", "reverse-engineer", "make a copy of this site"
- Starting a B2B marketing site from a reference design
- Cloning an SMT/EMS/industrial equipment website

## Prerequisites

**Stack:** Next.js 15 + React 18 + TypeScript + Tailwind CSS v4 + shadcn/ui + next/font/google + Lucide icons

**Why Next.js 15, not 16:** Next.js 16's `@next/swc-darwin-arm64` native binary is unreliable on macOS ARM64 — it corrupts silently causing `dlopen` errors and `invalid type: unit value, expected usize` during build. Next.js 15 + React 18 is fully stable.

## Step 1: Project Initialization

```bash
mkdir -p ~/smthelp-web/
cd ~/smthelp-web/
npx create-next-app@latest . \
  --typescript --tailwind --eslint --app --src-dir \
  --import-alias "@/*" --no-turbopack --yes
cd ~/smthelp-web/
npx shadcn@latest init -d --defaults   # may timeout, retry single component
npx shadcn@latest add button --yes
```

If `npx shadcn@latest init` times out, add components individually:
```bash
npx shadcn@latest add button card --yes
```

## Step 2: Configure Design Tokens

### globals.css
Set up the full design system in `src/app/globals.css`:
- CSS custom properties (design tokens) from the target site
- Keyframe animations (fade-up, slide-in, etc.)
- Tailwind v4 `@theme` block for custom colors/spacing
- Container class for max-width centering

### layout.tsx
Use `next/font/google` for fonts. Always use `variable: "--font-xxx"` on the font import and apply via `className` on `<html>` or `<body>`:
```tsx
import { Inter, JetBrains_Mono } from "next/font/google";
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
// Apply: className={inter.variable}
```

### next.config.ts
Configure `images.remotePatterns` for all external image CDNs the target site uses (required for `next/image` to load remote images):
```ts
const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "ikrorwxhnjmplp5m-static.micyjz.com" },
      // add other CDN hostnames as discovered
    ],
  },
};
```

## Step 3: TypeScript Types

Create `src/types/site.ts` with interfaces matching the data structures. At minimum:
```ts
export interface Product {
  id: string;
  name: string;
  slug: string;
  category: string;
  image: string;
  description: string;
}
export interface Project {
  id: string;
  title: string;
  description: string;
  image: string;
  location: string;
  client?: string;
  products?: string[];
}
export interface NavItem {
  label: string;
  href: string;
  children?: NavItem[];
}
```

Create `src/lib/utils.ts` (required by shadcn components):
```ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Create `src/lib/data.ts` with all static content (products, projects, navigation items, company info). Keep data separate from components.

## Step 4: Global Components First

Build these before any page-specific components:

### Navigation (`src/components/layout/Navigation.tsx`)
- TopBar: social icons + language selector + inquiry link
- Header: sticky, logo + desktop nav links with mega-menu dropdowns + mobile hamburger
- MobileMenu: full-screen overlay with all nav items
- Use `"use client"` for state (mobileOpen, langOpen, openDropdown)

### Footer (`src/components/layout/Footer.tsx`)
- 4-column grid: brand/tagline/socials | Company links | Products links | Contact info
- Dark background, white text
- Static — no "use client" needed unless interactive

### Social Icons (`src/components/icons/SocialIcons.tsx`)
- Inline SVG React components for each social platform
- Export: `YoutubeIcon`, `LinkedinIcon`, `TwitterIcon`, `FacebookIcon`, `InstagramIcon`, `PinterestIcon`, `VkIcon`
- Use `width/height` props inheriting from parent

## Step 5: Page Architecture

Each page lives in `src/app/<route>/page.tsx` (App Router file-system routing).

**Root layout** (`src/app/layout.tsx`): wraps all pages with `<Navigation />` and `<Footer />`.

**Home page** (`src/app/page.tsx`): imports and arranges all section components in topological order.

**Sub-pages**: Products, Company, Project each get:
1. A hero banner section (same green gradient pattern)
2. Breadcrumb trail
3. Content area
4. CTA section at bottom

## Step 6: Component Patterns

### Section components (`src/components/sections/`)
- Named by function: `HeroCarousel.tsx`, `FeaturedProducts.tsx`, `GlobalProjectsSection.tsx`
- Use `next/image` with `fill` for responsive images
- Add `"use client"` only when the component uses hooks (useState, useEffect, etc.)
- HeroCarousel: needs `"use client"` — use `useState` + `useEffect` for auto-play timer

### Product cards
- Grid: `grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4`
- Each card: image (aspect-ratio 1:1) + product name + description + Add to Basket button
- "Add to Basket": use `localStorage` for cart state — no backend needed

### Duplicate text bug
When rendering a list where title already contains the full descriptive name AND location is shown separately, the title will appear duplicated (e.g., "Kazakhstan Kazakhstan"). Fix: make the `title` field contain only the unique part (e.g., "Kazakhstan SMT Line") — the location overlay handles the geographic context.

## Step 7: Build Verification

Always verify with `npm run build` (NOT bare `tsc --noEmit`). Next.js 15's build:
1. Automatically patches `tsconfig.json`
2. Compiles with the correct webpack configuration
3. Runs type-checking with the post-patched tsconfig

Common build errors and fixes:

### `Cannot find module '@/lib/utils'`
Create `src/lib/utils.ts` with the `cn()` function. This is NOT created by `shadcn init` automatically.

### `Event handlers cannot be passed to Client Component props`
Remove `onError`, `onClick`, etc. from Server Components. Either:
- Add `"use client"` to the component
- Or pass event handlers through a client wrapper component

### `NAV_ITEMS' is defined but never used` (ESLint warning → build failure)
The Next.js 15 build treats ESLint errors as build failures. Always fix unused import warnings:
```ts
// Wrong
import { COMPANY_INFO, NAV_ITEMS } from "@/lib/data";

// Right — only import what you use
import { COMPANY_INFO } from "@/lib/data";
```

### `'project.products' is possibly 'undefined'`
Use nullish coalescing: `(project.products ?? []).map(...)`

### Unescaped quotes in JSX
Use `&apos;` or `&quot;` or `China&apos;s` instead of `'s` or `"..."` inside JSX text nodes.

## Step 8: Dev Server

```bash
npm run dev -- -p 3001   # port 3000 often occupied
```

Background process:
```bash
npm run dev -- -p 3001   # use background=true in terminal tool
```

Verify with:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/
# 200 = running, 500 = runtime error, 404 = missing route
```

If `/products` gives 500 after adding a new page: the dev server may have stale cache. Kill and restart:
```bash
# Kill existing dev server process, then:
npm run dev -- -p 3001
```

## Step 9: Visual QA

After all pages build cleanly, take screenshots of each page at:
- Desktop: 1440px
- Mobile: 390px

Compare against the target site section by section. Check:
- [ ] Header/navigation behavior (sticky, scroll effects)
- [ ] Hero carousel (auto-play, dot navigation)
- [ ] All section headings match
- [ ] Product images load
- [ ] Footer columns complete
- [ ] Responsive layout at mobile width
