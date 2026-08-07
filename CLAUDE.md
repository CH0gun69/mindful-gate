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
# valid names: phone_home, dashboard, setup, interruption, protection_customization, fake_app
python main.py --screen interruption --app TikTok   # --app populates interruption/fake_app
```

There is no test suite, linter, or build step in this repo — it's a single-window PySide6 script.

## How the app is wired

- `prototype/main.py` holds `MainWindow` (the real app: builds every screen once, adds them to a `QStackedWidget`, and wires navigation as Qt signal/slot connections between screens) and `DebugWindow` (`--screen`/`--app` mode: instantiates just one screen in isolation, pre-populated with mock context, no navigation wiring).
- Navigation flow: **Phone Home** (entry point) → tapping a protected app (Instagram/TikTok/X (Twitter)/Facebook/Reddit) goes through the **Interruption** screen first, then **Fake App**; tapping a non-protected app (YouTube/Messages) skips straight to **Fake App**. Separately, **Dashboard → Setup → Insights** is the original wellbeing-stats flow; as of Phone Home becoming the entry point, there is currently no link from Phone Home into that group — it's only reachable from itself (e.g. via `--screen dashboard`) or the legacy "▶ Simulate opening Instagram" button on the Dashboard. See `usage-manual.md` for the full click-by-click flow.
- All demo data (screen time, app list, protected/non-protected status, insights numbers, default intention, per-app icon/color) is centralized in `core/mock_data.py` — screens import from there rather than hardcoding their own copies.

## Non-negotiable habits

- Always commit and push after completing a task — never leave finished work sitting uncommitted between sessions. Confirm the push succeeded and report the commit hash.
- Before editing a file, check whether requested fixes are already present — some fixes have been re-requested multiple times after being lost to uncommitted work.

## Architecture notes

- prototype/core/ = business/mock data logic (mirrors ClipPortal's core/)
- prototype/ui/ = screens; prototype/ui/widgets/ = reusable components (mirrors ClipPortal's ui/ + ui/widgets/)
- Stylesheet lives in prototype/ui/styles.qss, loaded via BASE_DIR-relative path in main.py — never inline it back into main.py
- Debug mode: python main.py --screen <name> --app <name> jumps directly to any single screen for visual QA
