---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Load when building web components, pages, layouts, dashboards, landing pages, React components, Astro sites, Streamlit apps, Python dashboards, HTML/CSS artifacts, or any task where visual quality matters — including styling, redesigning, implementing from a mockup, or choosing a component library. Also load it when the user says "make this look good", "style this", or "build a UI for X". Avoids generic AI aesthetics. Do NOT trigger for backend, data pipeline, CLI, or document-only tasks.
---

# Frontend Design

Guide for creating distinctive, polished frontend interfaces that avoid generic "AI slop" aesthetics.

The goal is working code with exceptional aesthetic intentionality — not beautiful in a generic way, but specifically designed for the context.

## Surface Type

Before any aesthetic decision, determine the surface type. This changes which rules apply:

**Brand surface** (marketing, landing page, portfolio, campaign):
- Strong independent typography, bold visual direction, expressive color
- This is where distinctive fonts and dramatic aesthetics matter most
- Generic defaults are weakest here — audiences judge visual quality first

**Product UI** (app, dashboard, tool, admin):
- Established design system tokens take precedence: colors, typography, spacing, components
- System/product fonts (Inter, Roboto, system fonts) are fine when they belong to the existing design system
- Readability, information density, and consistency beat visual distinction
- Avoid generic AI aesthetics, but don't break an established product language for the sake of differentiation

When no project design system exists, default to Brand-surface thinking.

## Design Thinking (Before Code)

Pause and decide before writing any CSS or HTML. Rushing to code before committing to a direction produces mediocre output — the aesthetic decisions are the hard part.

1. **Purpose** — what problem does this interface solve? Who uses it?
2. **Aesthetic direction** — commit to ONE clear tone. Examples:
   - brutally minimal, maximalist, retro-futuristic, organic/natural
   - luxury/refined, playful, editorial/magazine, brutalist/raw
   - art deco/geometric, soft/pastel, industrial/utilitarian
   Pick an extreme and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.
3. **Constraints** — framework, performance budget, accessibility level
4. **Signature element** — what single thing makes this memorable?

## Aesthetic Guidelines

### Typography

Choose distinctive, characterful fonts. Pair a display font with a refined body font. For new surfaces without an existing design system: generic fonts (Inter, Roboto, Arial, system fonts, Space Grotesk) signal low effort — use Google Fonts or self-hosted alternatives. For product UI with an established design system: use the system tokens. Always specify fallbacks.

### Color and Theme

Commit to a cohesive palette via CSS custom properties. Dominant color with sharp accents outperforms timid, evenly-distributed palettes. Purple gradients on white backgrounds are the cliché to avoid. Vary between light and dark themes across designs — no two should converge on the same defaults.

### Motion and Interaction

CSS-only animations for HTML/vanilla projects — they're faster and simpler to maintain. Focus on high-impact moments: a staggered page-load reveal with `animation-delay` creates more delight than scattered micro-interactions. Add scroll-triggered effects and hover states that surprise. For React, use Motion (framer-motion) when available.

### Spatial Composition

Break predictable layouts. Asymmetry, overlap, diagonal flow, and grid-breaking elements create visual interest. Generous negative space OR controlled density both work — avoid the mushy middle where neither reads clearly.

### Backgrounds and Texture

Create atmosphere and depth: gradient meshes, noise/grain overlays, geometric patterns, layered transparencies, dramatic shadows, decorative borders. Flat solid-color backgrounds are only appropriate when that restraint IS the aesthetic direction.

## Accessibility

Accessibility isn't optional — poor accessibility excludes users and is fixable with almost no visual cost.

- Semantic HTML: proper heading hierarchy, landmarks, lists
- Visible focus states on all interactive elements (don't remove outlines without replacing them)
- WCAG AA contrast minimum: 4.5:1 for body text, 3:1 for large text
- Descriptive `aria-label` on buttons and links when text alone is ambiguous
- Screen-reader-friendly: visually hidden headings for navigation where needed
- Touch targets at least 44×44px on mobile
- Respect `prefers-reduced-motion` for animations

## Negativregeln (Anti-Pattern Constraints)

These are hard constraints — any output matching these patterns is disqualified as "AI slop."

**Read before generating any UI**: [references/anti-patterns.md](references/anti-patterns.md)

Quick reference (must never do):
- Inter, Roboto, Arial, system fonts, Space Grotesk as defaults
- Purple-blue gradient on white hero sections
- Generic card grids with identical rounded corners and shadows
- Single centered column layouts with no asymmetry
- `transition: all 0.3s ease` on everything
- Flat solid backgrounds without atmosphere or texture
- Any of the 5 specific combinations listed in the reference file

Every design decision must be verifiable against the full constraint list before writing code.

## Working with Screenshots or Mockups

When given a screenshot or mockup:
1. Analyze the visual language: colors, spacing, typography, hierarchy
2. Identify the design system if present: recurring patterns, component conventions
3. Reproduce with precision — match spacing, proportions, and visual weight
4. Ask if ambiguous: "Should I match this exactly or use it as inspiration?"

## Visual Verification

After implementing, verify visually before declaring done.

**Self-service with Playwright** (preferred when a dev server is running):
```bash
npx playwright screenshot http://localhost:3000 /tmp/ui-check.png
npx playwright screenshot --viewport-size="375,812" http://localhost:3000 /tmp/ui-mobile.png
npx playwright screenshot --viewport-size="1440,900" http://localhost:3000 /tmp/ui-desktop.png
```
Read the screenshots with the image tool to analyze them. Check Playwright is installed first (`npx playwright install chromium`).

**User screenshots** when Playwright is not available or when subjective assessment matters.

Call out which viewports to check: mobile 375px, tablet 768px, desktop 1440px.

See [references/verification.md](references/verification.md) for the full responsive and accessibility QA checklist.

## Reuse-first rule

Before writing any custom control, check in this order:

1. Existing project components
2. Chosen library or framework primitives
3. Accessible primitives (Base UI, Radix, framework-native)
4. Custom implementation — only when no existing source fits

## Design-tool handoff

Figma, v0, or other design output is reference or authorized source material, not automatically production-ready code:

1. Read the design context (tokens, layout, component structure)
2. Map tokens to the project's theme system
3. Rebuild components using the project's selected library and conventions
4. Verify against the original design for fidelity

Do not blindly import generated code — it bypasses the project's component architecture, accessibility patterns, and styling conventions.