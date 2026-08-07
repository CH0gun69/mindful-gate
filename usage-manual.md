# Usage Manual

How to set up, run, and navigate the mindful-gate Python/PySide6 prototype. This covers the `prototype/` app only — the SwiftUI hackathon deliverable is a separate, later phase (see `development-goal.md`).

No prior PySide6/Qt experience needed — just Python and a terminal.

---

## 1. Setup

### Clone the repo

```bash
git clone https://github.com/CH0gun69/mindful-gate.git
cd mindful-gate/prototype
```

Everything from here on assumes you're inside the `prototype/` folder.

### Create a virtual environment

A venv keeps this project's Python packages separate from anything else on your machine.

```bash
python3 -m venv .venv
```

### Activate it

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

You'll know it worked because your terminal prompt gets a `(.venv)` prefix. You'll need to re-run this activate command every time you open a new terminal to work on the project.

### Install dependencies

```bash
pip install -r requirements.txt
```

This installs PySide6 (the Qt-based UI toolkit the whole app is built on). That's the only dependency — no database, no network access, no accounts.

### First-time checks

Confirm it installed correctly:

```bash
python -c "import PySide6; print('PySide6 OK')"
```

If that prints `PySide6 OK`, you're ready to run the app.

---

## 2. Running the app normally

From inside `prototype/`, with the venv activated:

```bash
python main.py
```

A phone-shaped window (390×780) opens showing the **Phone Home screen** — that's the real entry point of the demo. No flags, no setup required.

---

## 3. The full user flow

### Phone Home screen (start here)

A mock phone lock/home screen: status bar up top, a grid of app icons (Instagram, YouTube, TikTok, Messages, X (Twitter), Facebook, Reddit), and a decorative dock at the bottom (Phone/Camera/Settings/Messages — these do nothing when tapped, they're just for realism).

Tap any app icon and one of two things happens:

**Protected apps (Instagram, TikTok, X (Twitter), Facebook, Reddit)** → the **Interruption screen** appears:

> "You opened \[App]. Still on purpose?"
> *"\[your current intention]"*

- **Continue** → takes you into that app's **Fake App screen** (a mock "you're now inside the app" view)
- **Go Back** → returns you to the Phone Home screen, no fake app shown

**Non-protected apps (YouTube, Messages)** → skip the interruption entirely and go straight to that app's **Fake App screen**.

### Fake App screen

A mock "app opened" view — same header (real brand logo, app name) for every app, then one of 3 body styles depending on which app it is:

- **Feed** (Instagram, Facebook, X (Twitter), Reddit) — a short vertical feed of mock post cards (avatar, username, photo, caption)
- **Shorts** (TikTok, YouTube) — one full-screen vertical photo with a caption overlay and mock engagement icons
- **Messages** (Messages) — a contact sidebar + a mock chat bubble conversation

All content (photos, captions, usernames, contacts) is local hardcoded mock data — no network access, works fully offline.

- **← (back arrow, top-left)** → returns to the Phone Home screen

### Dashboard, Setup, and Protection Customization

These three screens are the original wellbeing-stats flow (screen time, focus mode setup, per-app protection levels) and still fully work, but as of the Phone Home screen becoming the entry point, **there's currently no button that links from Phone Home into this group** — they're only reachable from each other once you're already on one of them. If you need to view/QA them, use [debug mode](#4-debug-mode) (`--screen dashboard`) or reach them via the legacy path described below.

Once you're on the **Dashboard** (e.g. via debug mode):

- **Activate Focus Mode** → **Setup** screen (choose protected apps + write an intention) → **Activate Protection** is now a real ON/OFF toggle: tapping it again shows **Protection ON** and returns you to the Dashboard with focus mode marked on; tapping it while already on turns protection off (without losing your chosen apps/intention), or **Back** returns without saving
- **Customize Protection** → **Protection Customization** screen — pick a 1/2/3 protection level per protected app (how much calm friction the Interruption screen adds before "Continue Anyway" unlocks); **Back to Dashboard** returns
- **⌂ Home** → returns to the Phone Home screen (one-way — there's no button back into Dashboard from Phone Home yet)

---

## 4. Debug mode

For visual QA, you don't have to click through the whole flow every time — launch any single screen directly.

```bash
python main.py --screen <name>
```

Valid names: `phone_home`, `dashboard`, `setup`, `interruption`, `protection_customization`, `fake_app`.

The screen opens in the same 390×780 window with the same styling as the real app — just without the rest of the navigation wired up.

### Example commands for all 6 screens

```bash
python main.py --screen phone_home
python main.py --screen dashboard
python main.py --screen setup
python main.py --screen interruption
python main.py --screen protection_customization
python main.py --screen fake_app
```

### Picking which app populates a screen

`interruption` and `fake_app` need to know which app they're pretending to represent. Use `--app` alongside `--screen` to pick one — it defaults to `"Instagram"` if you leave it out.

`interruption` also takes `--level` (1/2/3) to preview each protection level's escalating behavior — it defaults to `1` if you leave it out, e.g. `python main.py --screen interruption --level 3`.

```bash
python main.py --screen interruption --app TikTok
python main.py --screen fake_app --app Reddit
```

`--app` is ignored for the other four screens (they don't need it).

### Going back to normal

Just leave both flags off:

```bash
python main.py
```

---

## 5. Project structure

```
mindful-gate/
├── README.md
├── usage-manual.md          ← you are here
├── development-goal.md      ← roadmap / current phase
└── prototype/
    ├── main.py               ← entry point: MainWindow (real app) + DebugWindow (--screen mode)
    ├── requirements.txt
    ├── core/
    │   └── mock_data.py       ← all hardcoded demo data: screen time, app list,
    │                             per-app protection levels, default intention,
    │                             and each app's icon/color
    ├── ui/
    │   ├── phone_home.py      ← Phone Home screen (the entry point)
    │   ├── dashboard.py       ← Dashboard screen
    │   ├── intention_setup.py ← Setup screen
    │   ├── interruption.py    ← Interruption ("still on purpose?") screen
    │   ├── protection_customization.py ← Protection Customization screen
    │   ├── fake_app_screen.py ← "you opened the app" mock screen — one configurable
    │   │                         widget with 3 body styles (feed/shorts/messages)
    │   ├── styles.qss         ← one stylesheet for the whole app (dark theme, teal accent)
    │   └── widgets/
    │       ├── app_icon.py     ← tappable app icon (avatar + label) — used by phone_home
    │       ├── stat_card.py    ← one stat box in Dashboard (e.g. "87 Unlocks")
    │       ├── usage_ring_chart.py ← Dashboard's screen-time donut chart
    │       ├── svg_icon.py     ← shared real-brand-logo SVG rendering (AppIcon + FakeAppScreen)
    │       └── image_utils.py  ← shared cover-crop helper for FakeAppScreen's mock photos
    └── assets/
        ├── icons/              ← real brand-logo SVGs (Simple Icons)
        └── images/             ← local CC0 mock feed/shorts photos (Picsum Photos)
```

**Rule of thumb:** `core/` holds data with no UI code in it; `ui/` holds one file per full screen; `ui/widgets/` holds small reusable pieces used *inside* those screens. If you're adding a new full screen, it goes in `ui/`; if you're adding a small reusable component, it goes in `ui/widgets/`.
