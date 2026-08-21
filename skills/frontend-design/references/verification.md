# Visual QA Checklist

Use this after implementing a frontend design to verify the result before declaring done.

## Responsive Breakpoints

Test at these widths:
- **Mobile**: 375px (iPhone SE), 390px (iPhone 14)
- **Tablet**: 768px (iPad portrait)
- **Desktop**: 1280px, 1440px, 1920px

## Existing Design Contract Compliance

If the project already has a design contract in its root (`DESIGN.md`, `FRONTEND.md`, a brand guide, or an established component library), verify the output matches it:

- [ ] Colors match the contract's palette and roles
- [ ] Typography matches the contract's font families, sizes, and weights
- [ ] Spacing follows the contract's scale
- [ ] Border-radius matches the contract's radius personality
- [ ] Component styling matches the contract's component tokens
- [ ] No anti-patterns from the contract's Do's and Don'ts
- [ ] Selected framework, rendering model, and component source match the contract

If no such contract exists, skip this section. This kit does not create design contracts.

## What to Check

### Layout
- [ ] No horizontal overflow at any breakpoint
- [ ] Content hierarchy reads correctly on mobile (stacking order)
- [ ] Grid/flex gaps scale appropriately
- [ ] Touch targets >= 44×44px on mobile

### Typography
- [ ] Font loads correctly (check network tab for 404s)
- [ ] Line length readable (45–75 characters for body text)
- [ ] Heading hierarchy visually clear
- [ ] No text truncation that hides meaning

### Color and Contrast
- [ ] Text meets WCAG AA (4.5:1 body, 3:1 large text)
- [ ] Interactive elements distinguishable from static content
- [ ] Focus states visible against background
- [ ] Dark/light mode consistent if applicable

### Motion
- [ ] Animations don't cause layout shifts
- [ ] `prefers-reduced-motion` respected
- [ ] Staggered animations have reasonable total duration (<1s)
- [ ] Hover states don't obscure content

### Interaction
- [ ] All interactive elements keyboard-accessible
- [ ] Tab order logical
- [ ] No focus traps (except modals)
- [ ] Form inputs have visible labels

### Build
- [ ] Project build/check command passes (`pnpm run build`, `uv run streamlit run app.py`, etc.)
- [ ] No new lint or type errors introduced

## Screenshot Methods

### Method A: Self-service via Playwright (preferred)

When a dev server is running, take screenshots directly rather than asking the user.

```bash
# Single viewport
npx playwright screenshot http://localhost:3000 /tmp/ui-check.png

# Specific viewport
npx playwright screenshot --viewport-size="375,812" http://localhost:3000 /tmp/ui-mobile.png
npx playwright screenshot --viewport-size="1440,900" http://localhost:3000 /tmp/ui-desktop.png

# Full page scroll capture
npx playwright screenshot --full-page http://localhost:3000 /tmp/ui-full.png
```

Read the image with the image tool to analyze it. Check Playwright is installed first: `npx playwright install chromium`.

### Method B: User screenshots

Ask the user to provide screenshots when Playwright is not available or when their subjective assessment matters.

When reviewing a user screenshot:
1. Compare spatial relationships: spacing, alignment, proportions
2. Check color accuracy: are CSS values rendering as intended?
3. Look for overflow, clipping, or unexpected wrapping
4. Verify animation states if visible
5. Suggest specific fixes with CSS property and value

### When to use which
- **Method A**: Iterative refinement, autonomous QA passes, responsive breakpoint checks
- **Method B**: Quick one-off feedback, no Playwright in project, user is actively looking at the page
