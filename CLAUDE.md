# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

mindful-gate is a **hackathon project**: a Digital Wellbeing–style mock app that interrupts mindless social media use with intentions + gentle interruptions ("You opened Instagram. Still on purpose?"). The final deliverable is a **SwiftUI** app (iPhone/iPad/Mac, offline, hardcoded mock data, under 25 MB) — scaffolding for that phase has started (`swift/`), but no screens are ported yet.

This repo contains `prototype/` (Python + PySide6 clickable prototype, the UX source of truth) and `swift/` (the SwiftUI port destination — Swift Playgrounds `.swiftpm` App Playground, scaffolding only so far, see `swift/README.md`). See `development-goal.md` for current phase/scope and `README.md` for the full concept.

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

## Swift scaffolding (swift/) — started 2026-08-08

`swift/MindfulGate.swiftpm` is a Swift Playgrounds App Playground shell: Package.swift
(iOSApplication product, iOS 17+, no external dependencies) plus an empty
Sources/AppModule/{Core,Views,Views/Widgets} structure mirroring prototype/'s
core/ui/ui-widgets split. No screens ported yet — this is scaffolding only, per
development-goal.md Phase 2. Can only be built/run via Swift Playgrounds on iPad
(dev machine is Linux); see swift/README.md for the workflow.

**2026-08-11 update:** a future Mac/Xcode session has been asked to discard this
Playgrounds scaffold entirely and rebuild the port from scratch in Xcode, porting
directly from `prototype/` (not from this scaffold). Full instructions for that session
are in `swift/HANDOFF.md` — read that file first if you're starting Swift work with
Xcode available. Until then, per that handoff doc, this scaffold is left as-is and
untouched.

## Swift port — handoff to Mac session (Thursday)

IMPORTANT — FUTURE MAC SESSION HANDOFF

STOP: This document is a handoff plan for a future Mac session. DO NOT execute the Swift
porting work now.

You are currently running on Linux, without Xcode or a Swift/iOS development environment.

Your job right now is NOT to modify, delete, rebuild, or repair anything inside `swift/`.

Do not:
- Delete `swift/`
- Modify the existing Swift scaffold
- Attempt to compile or run the Swift project
- Try to recreate the Swift project using Linux tools
- Convert any Python code to Swift yet

Leave the repository exactly as it is.

This document describes what should happen later, when I have access to a MacBook with
full Xcode and the iOS Simulator. When that future Mac session begins, the Claude Code
instance running there should follow the instructions below and take ownership of the
Swift port.

# Swift port — handoff to Mac session (Thursday)

## Purpose

Port the fully working `prototype/` (Python + PySide6) of **Mindful-gate** into a real
SwiftUI app for the hackathon.

The goal is **not** to mechanically translate Python code into Swift. The goal is to
reproduce the prototype's **UI, behavior, wording, interactions, and overall user
experience** as faithfully as practical in SwiftUI, while keeping the implementation
simple and reliable enough to build and demonstrate in Xcode.

The `prototype/` directory is the **single source of truth** for the app's intended
behavior and appearance.

## Starting point

The `swift/` scaffold currently in this repo was built blind on a Linux machine with no
Swift compiler available — it was never opened, built, or verified in any way, and it's
reported broken/unusable.

On this Mac session:
- **DELETE the existing `swift/` directory entirely.**
- Rebuild the Swift app from scratch using **Xcode**.
- Do **not** use Swift Playgrounds this time — full Xcode is available now.
- Use Xcode's real compiler, previews, and iOS Simulator feedback throughout development.
- **Do not use the old `swift/` implementation as a reference.**
- Port **FROM `prototype/` only.**

## Recommended porting order

Each stage depends on the previous one.

1. **Core**
   - `Core/MockData.swift`
   - `Core/Strings.swift`
   - Source: `prototype/core/mock_data.py` and `prototype/core/strings.py`

2. **Reusable widgets**
   - Port the reusable components from `prototype/ui/widgets/*.py`
   - `ToggleSwitch` → use native SwiftUI `Toggle`
   - `LevelSlider` → use native SwiftUI `Slider`
   - Do **not** recreate these two as custom SwiftUI controls unless there is a concrete
     visual/behavioral reason.

3. **Views, screen by screen**
   - `PhoneHome`
   - `Interruption`
   - `FakeApp`
   - `Dashboard`
   - `ProtectionCustomization` / `Set Your Intention`

4. **Navigation**
   - Wire the complete navigation only after individual screens render correctly in
     isolation.
   - Use Xcode `#Preview` to verify each screen independently before connecting the full
     flow.

## Verification rule

After **EVERY meaningful implementation step**, actually build the project in Xcode and
run the relevant screen in the iOS Simulator.

Do not just write code and assume it compiles.

This Mac has a real Swift compiler — use it constantly. This is the entire reason we
waited for Mac access instead of continuing blind development on Linux.

For each screen, verify at minimum:
- It compiles successfully.
- It renders correctly in `#Preview`.
- It launches correctly in the iOS Simulator.
- Layout is reasonably faithful to the Python prototype.
- Interactions behave like the prototype.
- No unnecessary warnings/errors are being introduced.

If something fails to compile, **fix it before moving on** rather than accumulating
unverified code.

## Hackathon constraints

These constraints are unchanged from the rest of the project:
- Offline only.
- Apple platforms: iPhone / iPad / Mac.
- `<25 MB` project size requirement.
- Mock data only.
- Calm, non-judgmental design.
- No red.
- No scores or grades.
- Teal accent / `#93cfc4`-family palette matching the prototype.

Do not introduce unnecessary dependencies, networking, analytics, backend services, or
external assets.

## Time constraint / priority

This is a borrowed MacBook and the available time is limited to **Thursday only**, with
unknown exact hours.

Therefore, prioritize **working software over breadth**.

The priority is:
1. Get a real Xcode project building.
2. Get `PhoneHome` visually correct and working.
3. Get `Interruption` visually correct and working.
4. Connect those screens into a working flow.
5. Then continue with `FakeApp`, `Dashboard`, and `ProtectionCustomization` if time
   allows.

A working `PhoneHome + Interruption` flow is **much more valuable than six partially
implemented screens that do not compile or cannot be demonstrated**.

If time becomes tight, stop expanding scope and polish/verify the already-working flow
instead.

## Apple ID / signing constraint

There is **no Apple ID available** — no Apple device is owned.

Build and verify everything using **Xcode + iOS Simulator only**. This does not require
Apple ID sign-in.
- Do **not** attempt to run on a physical device.
- Do **not** ask for Apple ID sign-in.
- If physical-device code signing becomes necessary for any reason, **stop and flag the
  issue** rather than assuming account access (e.g. do not assume use of the MacBook
  owner's personal Apple ID without explicit confirmation first).

## Final definition of done

At minimum, by the end of the session there should be:
- A clean SwiftUI Xcode project rebuilt from scratch.
- The project builds successfully.
- `PhoneHome` works in the iOS Simulator.
- `Interruption` works in the iOS Simulator.
- The two screens can be demonstrated as a coherent flow.
- The implementation is based on `prototype/`, not the old broken `swift/` scaffold.
- No physical device or Apple ID is required.

If additional screens are completed, verify each one in the Simulator before considering
it done.

## Architecture notes

- prototype/core/ = business/mock data logic (mirrors ClipPortal's core/)
- prototype/ui/ = screens; prototype/ui/widgets/ = reusable components (mirrors ClipPortal's ui/ + ui/widgets/)
- swift/MindfulGate.swiftpm/Sources/AppModule/{Core,Views,Views/Widgets}/ mirrors this same split, one-way port target
- Stylesheet lives in prototype/ui/styles.qss, loaded via BASE_DIR-relative path in main.py — never inline it back into main.py
- Debug mode: python main.py --screen <name> --app <name> jumps directly to any single screen for visual QA
