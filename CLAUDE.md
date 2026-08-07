# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

mindful-gate is a **hackathon project**: a Digital Wellbeing–style mock app that interrupts mindless social media use with intentions + gentle interruptions ("You opened Instagram. Still on purpose?"). The final deliverable is a **SwiftUI** app (iPhone/iPad/Mac, offline, hardcoded mock data, under 25 MB) — that phase hasn't started yet.

This repo currently only contains `prototype/`: a Python + PySide6 clickable prototype used to validate the UX flow before anything is built in Swift. See `development-goal.md` for current phase/scope and `README.md` for the full concept.

## Commands

All commands run from `prototype/`, with the venv activated.

```bash
# one-time setup
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt    # only dependency: PySide6>=6.5

# run the app normally (opens on the Phone Home screen)
python main.py

# debug mode: jump directly to any single screen for visual QA
python main.py --screen <name>
# valid names: phone_home, dashboard, interruption, protection_customization, fake_app
python main.py --screen interruption --app TikTok   # --app populates interruption/fake_app
```

There is no test suite, linter, or build step in this repo — it's a single-window PySide6 script.

## How the app is wired

- `prototype/main.py` holds `MainWindow` (the real app: builds every screen once, adds them to a `QStackedWidget`, and wires navigation as Qt signal/slot connections between screens) and `DebugWindow` (`--screen`/`--app` mode: instantiates just one screen in isolation, pre-populated with mock context, no navigation wiring).
- Navigation flow: **Phone Home** (entry point) → tapping a protected app (Instagram/TikTok/X (Twitter)/Facebook/Reddit) goes through the **Interruption** screen first, then **Fake App**; tapping a non-protected app (YouTube/Messages) skips straight to **Fake App**. Separately, **Dashboard → Set Your Intention** (protected-app selection + per-app protection level + intention + on/off toggle, all merged into one screen — replaces the old separate Setup and Insights/Protection Customization screens) is the original wellbeing-stats flow; as of Phone Home becoming the entry point, there is currently no link from Phone Home into that group — it's only reachable from itself (e.g. via `--screen dashboard`) or the legacy "▶ Simulate opening Instagram" button on the Dashboard. See `usage-manual.md` for the full click-by-click flow.
- All demo data (screen time, app list, protected/non-protected status, insights numbers, default intention, per-app icon/color) is centralized in `core/mock_data.py` — screens import from there rather than hardcoding their own copies.

## Non-negotiable habits

- Always commit and push after completing a task — never leave finished work sitting uncommitted between sessions. Confirm the push succeeded and report the commit hash.
- Before editing a file, check whether requested fixes are already present — some fixes have been re-requested multiple times after being lost to uncommitted work.

## Recent session checkpoint (animated switch/slider + breathing circle)

As of commit `6d2669c` (pushed to `main`), the protection-levels UI was redesigned:
`ui/widgets/toggle_switch.py` (`ToggleSwitch`, animated on/off), `ui/widgets/level_slider.py`
(`LevelSlider`, click-anywhere-jumps-to-nearest-of-3), and `ui/widgets/breathing_circle.py`
(`BreathingCircle`, replaces the old cycling breathe-in/out text on the Interruption
screen). `ui/protection_customization.py` and `ui/interruption.py` were updated to use
these. **This was fully built AND verified** (not just built) on a real X display before
this commit — the 4-point plan checklist below all passed:
1. Switch slides, not snaps — confirmed numerically (`thumbX` interpolated 22.0 → 13.6 →
   2.0 across the animation, not an instant jump).
2. OFF app hides its level control entirely, ON app shows a clearly-labeled level —
   confirmed via screenshots + `maximumHeight` reads on the collapsible container.
3. Breathing circle genuinely oscillates (not a one-shot grow or sawtooth) — confirmed
   numerically (diameter: 36 → ~64 at half-cycle → ~36 at full cycle, symmetric ~50 at
   both the 1/4 and 3/4 marks).
4. Full `MainWindow` click-through re-confirmed: switch-driven app selection and
   slider-driven levels still commit through `protection_toggled`/`level_changed`
   correctly, with the same persistence-across-toggle and level-gating behavior as before.

No further verification needed on this specific feature — if picking this up again, this
note is just provenance, not a to-do.

## TODO: web demo (docs/index.html) is stale — needs a parity pass

`docs/index.html` is a self-contained HTML/JS/CSS mirror of `prototype/`, deployed via
GitHub Pages at `https://ch0gun69.github.io/mindful-gate/` (source: `main` branch, `/docs`
path — confirmed via `gh api repos/CH0gun69/mindful-gate/pages`). Comments in that file
say it deliberately mirrors the Python app's logic 1:1 (`APP_GLYPHS`, `usageColor()`,
`describeRingSegment()`, etc. are direct JS ports of `core/mock_data.py` /
`ui/widgets/usage_ring_chart.py`). It has **not** been updated to match anything from this
entire session — confirmed stale as of the checkpoint at commit `6284901`. Known gaps, in
the order they were built on the Python side:

1. **Interruption screen's app icon**: still a single static emoji per app
   (`interruptGlyph.textContent = glyph`) — predates even this session's first fix (real
   brand-logo SVG via `icon_path_for()`/`white_svg_pixmap()` on the Python side, now
   `avatarInnerHTML()`'s masked-SVG approach already used elsewhere in this same HTML file
   for Phone Home/Fake App, just never applied to the Interruption screen's icon).
2. **No protection levels at all**: no per-app level (1/2/3), no countdown text on
   Continue, no breathing circle, no reaffirm-tap step. `startInterruption()` just shows a
   plain "Continue" button, always immediately clickable.
3. **No "time spent today" nudge** on either the Interruption screen or the Fake App
   header (mirrors `core.mock_data.time_spent_today_for()` on the Python side — data
   already available here via the existing `TOP_APPS` JS array, just not wired up).
4. **No merged "Set Your Intention" screen**: still two separate screens
   (`#screen-setup`, `#screen-insights`), `Setup` still one-way (`activateProtection()`
   commits but nothing ever turns protection off), no per-app protection levels, no
   animated switch/slider (the whole `ToggleSwitch`/`LevelSlider` redesign from this
   session's last commit has no JS equivalent). `Insights` screen still exists as-is
   (Python side deleted it entirely).
5. **Ring chart stroke still ambient-tinted**: `buildRingChart()`'s
   `strokeColor = usageColor(isHighUsage())` is exactly the pattern removed on the Python
   side this session (`ui/dashboard.py`) — the ambient signal should live only on the big
   screen-time text, not the ring's per-segment stroke.
6. **Palette not desaturated**: `AMBIENT_COLOR_NORMAL`/`AMBIENT_COLOR_HIGH`/`APP_GLYPHS`
   here are still the original, more-saturated hex values — Python side's
   `core/mock_data.py` has the ~13%-desaturated versions (e.g. teal `#8fd3c7` → `#93cfc4`,
   amber `#e0a96d` → `#d9a974`, each app's own accent similarly softened). This file's CSS
   custom properties (`--accent`, `--accent-hover`) need the same update.

Recommended approach when picking this up: work top-to-bottom through the list above,
porting each Python-side change into the matching JS/CSS in `docs/index.html`, verifying
in a real browser (not just "no console error") after each item, then commit once all six
are done rather than piecemeal (this file has no build step / no diffing tool to catch a
partial port going stale again).

## Architecture notes

- prototype/core/ = business/mock data logic (mirrors ClipPortal's core/)
- prototype/ui/ = screens; prototype/ui/widgets/ = reusable components (mirrors ClipPortal's ui/ + ui/widgets/)
- Stylesheet lives in prototype/ui/styles.qss, loaded via BASE_DIR-relative path in main.py — never inline it back into main.py
- Debug mode: python main.py --screen <name> --app <name> jumps directly to any single screen for visual QA
