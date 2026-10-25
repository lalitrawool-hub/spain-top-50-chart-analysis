---
name: Iberian Sonic Intelligence
colors:
  surface: '#0f131c'
  surface-dim: '#0f131c'
  surface-bright: '#353942'
  surface-container-lowest: '#0a0e16'
  surface-container-low: '#181c24'
  surface-container: '#1c2028'
  surface-container-high: '#262a33'
  surface-container-highest: '#31353e'
  on-surface: '#dfe2ee'
  on-surface-variant: '#e5bdbe'
  inverse-surface: '#dfe2ee'
  inverse-on-surface: '#2c3039'
  outline: '#ac8889'
  outline-variant: '#5c3f40'
  surface-tint: '#ffb3b6'
  primary: '#ffb3b6'
  on-primary: '#68001a'
  primary-container: '#e11d48'
  on-primary-container: '#fffaf9'
  inverse-primary: '#be0037'
  secondary: '#ffb95f'
  on-secondary: '#472a00'
  secondary-container: '#ee9800'
  on-secondary-container: '#5b3800'
  tertiary: '#4cd7f6'
  on-tertiary: '#003640'
  tertiary-container: '#007f95'
  on-tertiary-container: '#f5fcff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdada'
  primary-fixed-dim: '#ffb3b6'
  on-primary-fixed: '#40000c'
  on-primary-fixed-variant: '#920028'
  secondary-fixed: '#ffddb8'
  secondary-fixed-dim: '#ffb95f'
  on-secondary-fixed: '#2a1700'
  on-secondary-fixed-variant: '#653e00'
  tertiary-fixed: '#acedff'
  tertiary-fixed-dim: '#4cd7f6'
  on-tertiary-fixed: '#001f26'
  on-tertiary-fixed-variant: '#004e5c'
  background: '#0f131c'
  on-background: '#dfe2ee'
  surface-variant: '#31353e'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
  metric-display:
    fontFamily: JetBrains Mono
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 32px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

The design system projects an authoritative, high-velocity analytics environment tailored for A&R executives, playlist curators, and streaming strategists managing the Spanish music market. The visual atmosphere fuses the precision of an enterprise terminal with the rhythmic, kinetic energy of Madrid and Barcelona’s contemporary urban and pop music landscape. 

The aesthetic is dark-mode native, utilizing deep obsidian layers, precision borders, and radiant sonic accents. Glassmorphism is deployed surgically—not as decorative wash, but to construct depth over dense telemetry, data grids, and trajectory curves. The UI conveys instant legibility under high-cognitive load, blending high-contrast status feedback with atmospheric, night-session recording console elegance.

## Colors

The palette is engineered for prolonged operational focus in low-light environments, using deep obsidian foundations balanced against vivid, high-saturation indicators.

### Surface Architecture
- **Base Canvas (`#0B0F17`):** The primary ground, establishing total visual silence.
- **Surface Elevation 1 (`#131B2E`):** Secondary paneling, structural sidebars, and sub-headers.
- **Surface Elevation 2 (`#1E293B`):** Interactive card backgrounds, active table rows, and popovers.
- **Border Stroke (`rgba(148, 163, 184, 0.12)`): Ultra-crisp dividers maintaining component definition without visual noise.

### Accent & Sonic Energy
- **Primary Rose-Crimson (`#E11D48` / `#F43F5E`):** Represents high velocity, market leadership, and Atlantic brand vitality. Reserved for peak lifecycle states, primary CTAs, and top-tier metrics.
- **Secondary Solar Goldenrod (`#F59E0B`):** Represents breakout momentum, playlist growth phases, and critical watch alerts.
- **Tertiary Cyan (`#06B6D4`):** Indicates stable rotation, recurrent catalog performance, and spatial audio telemetry.
- **Success Mint (`#10B981`):** Quantifies upward rank delta, positive streaming velocity, and algorithmic adoption.

### Lifecycle Status Semantic Rules
- **New Entry:** Electric Violet (`#8B5CF6`) with a 15% alpha background tint.
- **Growth:** Emerald Mint (`#10B981`) with upward momentum vectors.
- **Peak:** Crimson Pulse (`#E11D48`) backed by an inner ambient glow.
- **Mature:** Amber Balance (`#F59E0B`) highlighting sustained daily streams.
- **Decline:** Slate Gray (`#64748B`) signifying playlist pruning and churn risk.

## Typography

The typographic hierarchy combines contemporary structural geometric forms with rigid, monospaced tabular data.

### Structural Type (Plus Jakarta Sans)
Utilized for brand headings, track metadata, and editorial labeling. It balances geometric modernism with human touchpoints, retaining readability even at reduced weight configurations.

### Telemetry & Technical Type (JetBrains Mono)
Applied to all rankings, stream counts, duration stamps, ISWC/ISRC identifiers, and delta metrics. Tabular figures prevent layout shifting in real-time streaming displays and allow rapid vertical scanning across chart tables.

## Layout & Spacing

The architecture operates on a high-density 12-column fluid grid, optimized for data-dense dashboards across ultrawide monitors and laptop displays.

### Layout Rules
- **Desktop (1440px+):** 12-column layout with 16px (`1rem`) gutters and 32px (`2rem`) global margins. Information-heavy charts and comparative matrices occupy up to 8 columns; analytical summaries and lifecycle telemetry panels occupy the remaining 4.
- **Tablet (768px - 1439px):** 8-column layout. Multi-column metric groups collapse into 2-by-2 clusters; secondary track metadata drops down into expandable drawer views.
- **Mobile (< 768px):** 4-column layout with 12px (`0.75rem`) gutters and 16px (`1rem`) edge padding. Dense tables transform into horizontally scrollable metric cards with sticky ranking columns.

## Elevation & Depth

Visual hierarchy uses subtle frosted layers and translucent obsidian surfaces rather than drop shadows, preventing muddy dark-mode UI.

- **Level 0 (Base Canvas):** Solid `#0B0F17`.
- **Level 1 (Sub-Panels & Sidebar):** Solid `#131B2E` with a 1px border of `rgba(148, 163, 184, 0.08)`.
- **Level 2 (Analytical Cards):** Translucent `#1E293B` at 75% opacity with an 8px backdrop blur (`backdrop-filter: blur(8px)`) and a subtle top-edge highlight (`border-top: 1px solid rgba(255, 255, 255, 0.1)`).
- **Level 3 (Modals, Overlays & Floating Tooltips):** Obsidian glass (`#0B0F17` at 90% opacity), 16px backdrop blur, bounded by a 1px contour of `rgba(244, 63, 94, 0.3)` on active selection.
- **Glow Effects:** High-priority items (e.g., #1 Track or Rapid Acceleration status) emit a faint 12px radius ambient glow matching the state's neon token at 15% opacity.

## Shapes

The interface uses a calibrated, soft geometry (`roundedness: 1`). Radii stay small to maximize usable area in dense information tables and sparkline clusters.

- **Buttons, Inputs, Status Pills:** 4px (`0.25rem`) border radius.
- **Cards, Panels, Floating Modules:** 8px (`0.5rem`) border radius.
- **Album Art & Track Thumbnails:** 4px (`0.25rem`) corner radius to preserve cover framing.
- **Data Indicator Badges:** Full pill-capsule rounding (`9999px`) to visually differentiate status tokens from actionable controls.

## Components

### Buttons
- **Primary Action:** Solid crimson (`#E11D48`) fill with high-contrast white text, 4px border radius, uppercase mono tracking on labels, and an interactive state that shifts to `#F43F5E` with a subtle box-shadow bloom.
- **Secondary / Ghost Action:** Transparent background with a 1px stroke of `rgba(148, 163, 184, 0.2)`. On hover, fills to `#1E293B` with full white text.

### Status Pills (Lifecycle Stages)
- Compact, high-visibility badges with an internal 6px pulsating dot.
- Built using monospaced micro typography (`label-sm`), with 8px horizontal padding and 2px vertical padding.
- Employs color tokens mapped strictly to stage rules: New Entry (Violet), Growth (Emerald), Peak (Crimson Glow), Mature (Amber), Decline (Slate).

### Data Tables & Playlist Rows
- Low-profile headers with sticky positioning, styled with muted JetBrains Mono text and uppercase tracking.
- Alternating subtle row fills (`#131B2E` to transparent), framed by `1px` bottom dividers.
- Hover reveals quick-action audio snippets, playlist pitch logs, and DSP destination links without triggering layout shifts.

### Audio Waves & Longevity Sparklines
- Dynamic SVGs embedded directly into table cells and cards.
- Line weights set to a sharp 1.5px with a vertical gradient fill tapering to 0% opacity at the baseline.
- Markers for algorithmic trigger thresholds are indicated via dotted secondary-accent guides.

### Input & Filter Bars
- Monolithic inputs set against `#131B2E` with inset styling, 1px perimeter border, and a vibrant `#06B6D4` ring on focus.
- Filter chips toggle states with instant background shifts from inactive slate-alpha to active primary-crimson.