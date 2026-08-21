# Negativregeln — Anti-Patterns for UI Generation

Strict negative rules (MUST NOT). These are hard constraints — violating any of these disqualifies the output as "AI slop."

**Scope:** These rules govern bespoke new brand surfaces. They do not override:

- An approved design contract or brand guide in the project root (e.g. `DESIGN.md`, `FRONTEND.md`)
- An established component library (shadcn/ui, MUI, daisyUI, Streamlit native, etc.)
- A project's existing design system

When a project has any of these, its conventions take precedence. These anti-patterns apply only when no project-specific constraint exists (see `frontend-design/SKILL.md §Surface Type`).

---

## Typography

- **NEVER** use Inter, Roboto, Arial, system-ui as default or fallback fonts
- **NEVER** use Space Grotesk as a starting point — it is overused in AI outputs
- **NEVER** use a single font for all text sizes — distinguish display from body
- **NEVER** leave font-family without explicit fallbacks (serif/sans-serif minimum)
- **NEVER** use font sizes that don't respect the design hierarchy

---

## Color & Theme

- **NEVER** use purple-blue gradient on white hero sections
- **NEVER** use a single "brand color" as a flat wash across the entire design
- **NEVER** use `background: white` / `background: #f8fafc` as the default without purpose
- **NEVER** use color choices that are "safe defaults" — purple, blue, indigo gradients
- **NEVER** use identical button/card colors across unrelated components
- **NEVER** use a timid palette where every color competes equally — commit to dominance

---

## Layout & Composition

- **NEVER** produce a generic card grid with equal spacing, rounded corners, subtle shadow
- **NEVER** use a centered single-column layout with no asymmetry or visual interest
- **NEVER** use a 12-column grid that is perfectly symmetrical with no breaking elements
- **NEVER** place all content in a clean white box — avoid "container-itis"
- **NEVER** use the same spacing rhythm everywhere (16px/24px/32px without variation)
- **NEVER** default to centered alignment — left-aligned content reads faster and looks more intentional
- **NEVER** add a footer that is an afterthought with thin gray text on gray background

---

## Backgrounds & Texture

- **NEVER** use a flat solid color background when the design could use atmosphere
- **NEVER** leave backgrounds empty when gradients, noise, or subtle patterns would add depth
- **NEVER** use generic "hero background image" patterns without purpose
- **NEVER** default to white/off-white for dark-themed designs — deep backgrounds need richness

---

## Motion & Interaction

- **NEVER** add scattered micro-interactions without a coherent animation philosophy
- **NEVER** use `transition: all 0.3s ease` on everything — animate only what matters
- **NEVER** use animation durations longer than 500ms for UI feedback (page transitions can be longer)
- **NEVER** skip `prefers-reduced-motion` support
- **NEVER** use animation as a substitute for good visual hierarchy

---

## Component Patterns

- **NEVER** create a button that is a rounded rectangle with a shadow and a single color
- **NEVER** design cards that all look identical with the same padding, shadow, border-radius
- **NEVER** use the same border-radius value (typically 8px or 12px) on every element
- **NEVER** create a navigation that uses the same style for every item without hierarchy
- **NEVER** use placeholder images that are stock-photo generic (office workers shaking hands)
- **NEVER** produce form inputs with a single-style appearance across all states

---

## Iconography & Graphics

- **NEVER** use the same icon library as every other AI-generated UI (Heroicons, FontAwesome defaults)
- **NEVER** use icons at the same size throughout — icons need hierarchy too
- **NEVER** use emoji in place of proper icons or illustrations

---

## Specific Combinations to Avoid

1. Hero section: centered white background + purple-blue gradient + Space Grotesk + rounded button
2. Feature section: 3-column card grid + identical cards + subtle shadow + 8px border-radius
3. Footer: dark gray background + light gray text + thin divider line + centered links
4. CTA section: purple gradient background + white text + "Get Started" button + centered layout
5. Testimonial section: avatar circle + quote in italics + 5-star rating + card with shadow

---

## How to Use These Rules

Before writing any CSS or HTML, verify your design decisions against this list:

1. Font choice → check typography rules
2. Color palette → check color rules
3. Layout structure → check layout rules
4. Background treatment → check background rules
5. Animation plan → check motion rules
6. Component design → check component rules

If a pattern matches one of the "NEVER" items, stop and choose differently.

---

## Project-Specific Overrides

If the project has an approved design contract (e.g. `DESIGN.md`, `FRONTEND.md`), an established component library, or a brand guide, those take precedence. These Negativregeln apply when no project-specific constraint exists. See `SKILL.md §Surface Type` for the Brand vs Product distinction.