# Color Palette

A reference for the visual style used in this dashboard, written for reuse in similar data projects.

## Philosophy

Muted, desaturated tones throughout — nothing neon or overly saturated. Every color reads clearly on a white background without competing with the data. No pure primaries: the red leans orange, the blue leans slate, the green leans teal.

## Anchor Colors

| Role            | Hex       | Use                                   |
| --------------- | --------- | ------------------------------------- |
| Blue (primary)  | `#1a6faf` | Headline/official series              |
| Blue (mid)      | `#457b9d` | Secondary blue series                 |
| Blue (light)    | `#74b3ce` | Core/tertiary variant of blue         |
| Teal (primary)  | `#2a9d8f` | Output, PCE, spending                 |
| Teal (light)    | `#52b788` | Core/secondary teal variant           |
| Amber           | `#f4a261` | Consumer-facing, disposable income    |
| Amber (bright)  | `#ff9f43` | Core CPI, inflation                   |
| Red (primary)   | `#e63946` | Headline CPI, attention series        |
| Red (mid)       | `#d62828` | Unemployment, strong emphasis         |
| Red (muted)     | `#bc4749` | Long-term unemployment, softer red    |
| Coral           | `#e07a5f` | Secondary unemployment                |
| Coral (light)   | `#e76f51` | CPI level, softer emphasis            |
| Purple          | `#6a4c93` | One-off series with no natural family |

## Ordered Ramps

The anchor colors above encode *identity* — series that have no natural order. Where the series are an ordered ladder instead (wealth percentile groups, age bands), a single hue stepped light-to-dark carries the order that separate hues would throw away. Two charts use one.

**Wealth percentile bands** (`--wealth-1` … `--wealth-4`), blue:

| Slot | Light | Dark | Use |
| --- | --- | --- | --- |
| 1 | `#86b6ef` | `#9ec5f4` | Bottom 50% (lowest rung) |
| 2 | `#5598e7` | `#6da7ec` | 50th–90th |
| 3 | `#2a78d6` | `#3987e5` | 90th–99th |
| 4 | `#184f95` | `#1c5cab` | Top 1% (highest rung) |
| — | `#d03b3b` | `#e66767` | National debt, the contrasting overlay line |

**Bankruptcy age bands** (`--age-1` … `--age-6`), violet — a second hue so the two stacked-area charts never read as the same quantity:

| Slot | Light | Dark | Use |
| --- | --- | --- | --- |
| 1 | `#c6b2ed` | `#d8c6fc` | 18–29 (youngest, bottom of stack) |
| 2 | `#b196e1` | `#c4acf2` | 30–39 |
| 3 | `#9c7bd2` | `#b192e7` | 40–49 |
| 4 | `#8760c3` | `#9d78da` | 50–59 |
| 5 | `#724aab` | `#8961c6` | 60–69 |
| 6 | `#5a3a89` | `#744faa` | 70+ (oldest, top of stack) |
| — | `#e3770e` | `#ff9b45` | National total, the contrasting overlay line |

Both columns are stepped for their own background rather than flipped automatically, and each keeps monotone lightness, adjacent gaps of at least 0.06 L, and the surface-facing end clear of the background. The six-step violet ramp holds gaps of 0.069–0.073 L across the same lightness range the four-step blue one spans. Ramp colors live as CSS custom properties so the two themes swap in one place.

A ramp pairs with one contrasting overlay line drawn on top of the stack — warm against the cool ramp — reserved for a total or comparison series rather than another member of the ladder.

## Structural Rules

**Headline vs. secondary:** Solid line for the headline/primary series; dashed line (`strokeDasharray="5,3"`) for core or secondary series. Use a slightly lighter shade of the same hue for the dashed variant (e.g. `#e63946` headline → `#ff9f43` core CPI).

**Recession shading:** `#888` at 8% opacity (`fillOpacity={0.08}`). Enough to notice, not enough to fight the data lines.

**Reference lines:**
- Zero line: default stroke (black), solid
- Policy target (e.g. Fed's 2%): `#bbb`, dashed (`strokeDasharray="4,3"`)

**Line weight:** `strokeWidth={1.5}` for all data lines — thin enough to show detail, heavy enough to read at small sizes.

## Backgrounds & Chrome

| Element             | Value                         |
| ------------------- | ----------------------------- |
| Page background     | `#f8f9fa`                     |
| Card background     | `#fff`                        |
| Card border         | `#e5e7eb`                     |
| Card border radius  | `10px`                        |
| Card box shadow     | `0 1px 3px rgba(0,0,0,0.04)` |
| Section label color | `#999`                        |
| Meta/subtitle text  | `#888`                        |
| Body text           | `#1a1a2e`                     |

## Transfer Recipe

1. Pick 4–5 anchor hues spaced around the color wheel (blue-slate, teal, amber, red-coral, purple).
2. Desaturate each by ~30–40% from a fully saturated starting point.
3. Derive lighter variants by raising lightness ~15% — use these for dashed/secondary lines.
4. Use a warm near-white (`#f8f9fa`) as the page background and `#e5e7eb` for borders.
5. Reserve red tones for series that warrant attention; use blue/teal as the neutral default.
6. Keep purple as a one-off for any series that doesn't fit a natural color family.
