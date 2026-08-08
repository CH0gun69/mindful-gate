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

## Web demo (docs/index.html) — brought to parity 2026-08-08 ✅

`docs/index.html` is a self-contained HTML/JS/CSS mirror of `prototype/`, deployed via
GitHub Pages at `https://ch0gun69.github.io/mindful-gate/` (source: `main` branch, `/docs`
path). Two ports landed this session (2026-08-07's note below is now superseded by this
one — kept only for history):

**First pass (2026-08-07)**: real brand icon on Interruption, full per-app protection
levels (countdown/breathing circle/reaffirm), time-spent nudges, Setup+Insights merged
into "Set Your Intention", ring stroke de-tinted, palette updated.

**Second pass (2026-08-08, this note)**: ported the Shuffle/Light-Dark/TH-EN referee
controls plus the Bug 1/Bug 2 fixes, none of which existed in the first pass:

- **Shuffle**: `shuffleTopApps()`/`SHUFFLED_TIMES` mirror `core.mock_data`'s
  shuffle mechanism exactly (`TOP_APPS` itself never mutated, `timeFor()` overlay,
  `currentScreenTimeToday()` keeps the big total consistent with what's shuffled). Wired
  into `buildRingChart()`/`buildUsageLegend()`/`timeSpentTodayFor()`/`isHighUsage()` so
  the ring, legend, ambient tint, and Interruption/Fake App nudges all update together.
- **Light/Dark**: a `#phone.light` class flips the shared CSS custom properties
  (`--bg`/`--bg2`/`--border`/`--text`/`--muted`/`--dim`/`--thumb`), plus explicit
  overrides for the handful of hardcoded (non-var) colors, mirroring
  `ui/styles_light.qss` selector-for-selector — including the Bug 1 fix: feed/messages
  content gets its own light "generic real app" look (white cards, near-black text),
  never mindful-gate's own teal/amber; only "shorts" stays unchanged regardless of theme
  (translucent dark overlay on a photo, same as real video apps).
- **TH/EN**: a `STRINGS`/`t()`/`fmt()` trio mirrors `core/strings.py` exactly, covering
  the same 4-screen scope as the Bug 2 fix — Phone Home, Dashboard, Interruption
  (including the live countdown text), and Set Your Intention (including per-app
  "Level N:" labels). Fake App and the three referee controls themselves stay
  English-only, same reasoning as the Python side.

Verified via a local preview (`.claude/launch.json`'s `web-demo` config): shuffle
consistency confirmed numerically (shuffled legend times summed to the exact new total),
theme/language toggles confirmed via direct JS state reads (`#phone.light` class,
translated text on all 4 in-scope screens, app brand names/user-typed text correctly
untranslated), level-3 breathing/reaffirm confirmed mid-flow, and a real per-app-switch
interaction (not a raw variable mutation) confirmed the "Level N:" label re-renders
correctly live. Zero console errors throughout.

This remains a manual, one-time port (per the original KISS decision, no sync tooling) --
whoever picks up the next round of Python-side changes will need to repeat this pass by
diffing against this note's "as of" state, same as this pass did against the old note.

## Referee/demo utility controls on Phone Home (Shuffle, Light/Dark, TH/EN)

Three compact widget-style controls sit directly below the screen-time widget on Phone
Home (`PhoneHomeScreen._build_controls_row()`), all session-only (never persisted, all
reset to defaults on restart):

- **Shuffle** (`core.mock_data.shuffle_top_apps()`): randomizes each `TOP_APPS` app's mock
  "time spent today" in memory only — `TOP_APPS` itself is never mutated. Refreshes the
  screen-time widget's total, Dashboard's ring/legend/ambient tint, and (implicitly, since
  they read the data fresh every time they're opened) the Interruption/Fake App
  "time spent" nudges.
- **Light/Dark** (`main.load_stylesheet()` + new `prototype/ui/styles_light.qss`): swaps
  the whole app's stylesheet at runtime via `app.setStyleSheet()`. Brand accent colors
  (teal, the Focus-Mode-active green) are identical in both files on purpose. Fake App's
  feed/messages body content DOES get its own light variant (generic "real app" colors —
  white cards, near-black text — never mindful-gate's own teal/amber, see
  `styles_light.qss`'s top comment); only its "shorts" style (TikTok/YouTube) stays
  unchanged regardless of theme, since that caption bar is a translucent dark overlay on
  top of a photo, same as how real apps/videos keep it dark regardless of OS theme. The
  one thing this swap genuinely can't reach: `ToggleSwitch`/`BreathingCircle`
  (self-painted in Python, never consult the app stylesheet at all — confirmed their
  hardcoded colors still read fine against the light theme regardless).
- **TH/EN** (`core/strings.py`'s `t()`): retranslates Phone Home, Dashboard, Interruption,
  and Set Your Intention — i.e. all of mindful-gate's own UI chrome (captions, labels,
  button text, the level slider's "Level N:" label, etc.). **Fake App remains
  English-only, deliberately** — its feed captions/usernames/chat messages/shorts
  captions are mocked-up real-app content, not mindful-gate's own UI copy, same reasoning
  as its light/dark styling above. Real app brand names (Instagram, TikTok, etc.) and any
  user-typed text (the intention/message field) are never translated anywhere, on any
  screen — proper nouns and user input aren't UI copy.

## Architecture notes

- prototype/core/ = business/mock data logic (mirrors ClipPortal's core/)
- prototype/ui/ = screens; prototype/ui/widgets/ = reusable components (mirrors ClipPortal's ui/ + ui/widgets/)
- Stylesheet lives in prototype/ui/styles.qss, loaded via BASE_DIR-relative path in main.py — never inline it back into main.py
- Debug mode: python main.py --screen <name> --app <name> jumps directly to any single screen for visual QA
