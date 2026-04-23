# DESIGN — AI 時代軟體工程師

改編自 Swiss Pulse（Josef Müller-Brockmann），保留 grid-locked 與數據主導的精神，但加入琥珀暖色讓訊息不會全程冰冷。主題是危機 / 轉機，冷藍代表危機、暖橙代表轉機。

## Style Prompt

Off-black canvas with one cold blue and one warm amber accent. Grid-locked layouts, left-anchored hero text, oversized numerals that dominate the frame at 280–420px. Decoratives are hairline rules, faint dot grids, and ghost characters bleeding off-frame. Motion snaps with `expo.out` / `power4.out` for data reveals; dissolves and pushes for scene transitions. Nothing decorative floats — every element has a grid reason.

## Colors

| Role                  | Hex       | Notes                                                 |
| --------------------- | --------- | ----------------------------------------------------- |
| Background            | `#0a0a0b` | Warm near-black, never `#000`                         |
| Foreground text       | `#f4f4f2` | Warm off-white                                        |
| Muted label           | `#8a8a88` | Captions, source lines, secondary                     |
| Crisis accent (blue)  | `#2f6bff` | Data callouts tied to the declining numbers           |
| Turnpoint accent      | `#f6a93b` | Amber — opportunity, personal results, action items   |
| Warning red           | `#e5484d` | Reserved for the "crisis" moment only, used sparingly |
| Hairline grid         | `#1b1b1d` | Dividers, grid lines, frame panels                    |

## Typography

- **Headlines & Chinese body:** `"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif` — weights 800/900 for hero, 400 for labels. Chinese stays crisp without reaching for overused display fonts.
- **Latin / numbers:** `"Space Grotesk", sans-serif` — 700 for numerals (280–420px) with `font-variant-numeric: tabular-nums` and `letter-spacing: -0.04em`.
- Label/meta: same Space Grotesk, 13–16px, `letter-spacing: 0.22em`, uppercase.

## Motion Rules

- Entrances vary eases: `expo.out`, `power4.out`, `back.out(1.4)`, `sine.inOut` for ambient.
- First animation starts at 0.2–0.4s, never t=0.
- Numbers count up from 0 on reveal (Swiss Pulse signature).
- Transitions: primary = **push slide** (`power3.inOut`, 0.5s) for serial data scenes; accent = **blur crossfade** at the crisis→turnpoint handoff; **color dip to black** for the outro.
- Ambient motion per scene: exactly one — a breathing glow, a hairline pulse, a ghost-text drift. Never two.

## What NOT to Do

- No gradient text, no `background-clip: text`.
- No cyan + purple combos, no generic neon glows.
- No centred single-text-block layouts — always anchor to edges or split the frame.
- No Inter / Roboto / Playfair. No Syne.
- No pie charts, no multi-axis charts, no "web dashboard" grids.
- No decorative motion without purpose — if it doesn't communicate weight, hierarchy, or continuity, delete it.
