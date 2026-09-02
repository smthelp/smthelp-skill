# smtfactory.com Clone — Project Structure Reference

## Verified File Tree

```
~/smthelp-web/                          # Next.js 15.5.20 + React 18
├── SPEC.md                              # Design specification document
├── next.config.ts                       # images.remotePatterns for CDN hostnames
├── package.json
├── tsconfig.json
├── tailwind.config.ts                   # (Tailwind v4: no tailwind.config, uses @theme in globals.css)
└── src/
    ├── app/
    │   ├── layout.tsx                   # Root layout: fonts, Navigation, Footer
    │   ├── globals.css                  # Full design system (vars, keyframes, utilities)
    │   ├── page.tsx                    # Homepage
    │   ├── products/page.tsx            # Product catalog with category filter
    │   ├── company/page.tsx            # About/company page with timeline
    │   └── project/page.tsx            # Global projects grid
    ├── components/
    │   ├── layout/
    │   │   ├── Navigation.tsx           # TopBar + Header + MobileMenu ("use client")
    │   │   └── Footer.tsx              # 4-column footer (static)
    │   ├── sections/
    │   │   ├── HeroCarousel.tsx       # 3-slide auto-play carousel ("use client")
    │   │   ├── GlobalProjectsSection.tsx # Horizontal scroll project cards
    │   │   ├── ThreePillars.tsx        # 3-column value proposition cards
    │   │   ├── ApplicationAreas.tsx     # 12-application icon grid
    │   │   ├── EquipmentCategories.tsx  # 16-category equipment grid
    │   │   ├── FeaturedProducts.tsx     # Product grid with tabs + cart ("use client")
    │   │   ├── SMTLineBanner.tsx       # Full-width banner image
    │   │   └── TrustBadges.tsx         # D-U-N-S + WeChat QR + cert badges
    │   ├── icons/
    │   │   └── SocialIcons.tsx         # YoutubeIcon, LinkedinIcon, TwitterIcon, etc.
    │   └── ui/
    │       └── button.tsx               # shadcn/ui button (installed via shadcn add)
    ├── lib/
    │   ├── data.ts                     # All static content (17KB: products, projects, nav)
    │   └── utils.ts                    # cn() utility for shadcn components
    └── types/
        └── site.ts                      # TypeScript interfaces (Product, Project, NavItem, etc.)
```

## Verified Component Dependencies

```
Root Layout (layout.tsx)
└── Navigation ("use client" — has useState hooks)
└── Footer
└── {page} (page-specific sections)
    ├── HeroCarousel ("use client")
    ├── GlobalProjectsSection
    ├── ThreePillars
    ├── ApplicationAreas
    ├── EquipmentCategories
    ├── FeaturedProducts ("use client")
    ├── SMTLineBanner
    └── TrustBadges
```

## CSS Variables (from smtfactory.com)

```css
:root {
  --color-primary: #007A3D;       /* I.C.T green — main brand color */
  --color-primary-dark: #005C2E;  /* darker green for hover states */
  --color-accent: #D6001C;        /* red — CTA buttons, highlights */
  --color-dark: #1A1A1A;          /* TopBar, footer background */
  --color-text: #333333;           /* primary text */
  --color-text-secondary: #666666; /* secondary/subdued text */
  --color-text-muted: #999999;    /* muted/placeholder text */
  --color-surface: #F5F5F5;       /* light gray background sections */
  --color-border: #E5E5E5;        /* borders and dividers */
  --color-white: #FFFFFF;
  /* Layout */
  --topbar-height: 40px;
  --header-height: 70px;
  --section-padding: 80px;
}
```

## Standard Hero Banner Pattern (all pages)

```tsx
<section
  className="relative flex items-center justify-center text-center text-white"
  style={{
    height: 280,
    background: "linear-gradient(135deg, #007A3D 0%, #005C2E 100%)",
  }}
>
  <div className="container">
    <h1 className="text-3xl font-bold mb-3">{title}</h1>
    <p className="text-white/80 text-lg max-w-2xl mx-auto">{subtitle}</p>
  </div>
</section>
```

## Verified CDN Image Sources

```
Hostname: ikrorwxhnjmplp5m-static.micyjz.com
Used for: Logo SVG, Hero banners (3), Product images, Project images,
          Application icons, Equipment category icons, Trust badge images
```
