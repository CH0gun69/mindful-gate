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

A generic mock "app opened" view — header with the app's name/icon, a few placeholder content cards, clearly labeled as fake. Every app (protected or not) uses this same screen, just re-skinned with that app's name/color.

- **← (back arrow, top-left)** → returns to the Phone Home screen

### Dashboard, Setup, and Insights

These three screens are the original wellbeing-stats flow (screen time, focus mode setup, weekly insights) and still fully work, but as of the Phone Home screen becoming the entry point, **there's currently no button that links from Phone Home into this group** — they're only reachable from each other once you're already on one of them. If you need to view/QA them, use [debug mode](#4-debug-mode) (`--screen dashboard`) or reach them via the legacy path described below.

Once you're on the **Dashboard** (e.g. via debug mode):

- **Activate Focus Mode** → **Setup** screen (choose protected apps + write an intention) → **Activate Protection** returns you to the Dashboard with focus mode marked on, or **Back** returns without saving
- **View Insights** → **Insights** screen (intentions kept, time saved, most-interrupted app); **Back to Dashboard** returns
- **⌂ Home** → returns to the Phone Home screen (one-way — there's no button back into Dashboard from Phone Home yet)

---

## 4. Debug mode

For visual QA, you don't have to click through the whole flow every time — launch any single screen directly.

```bash
python main.py --screen <name>
```

Valid names: `phone_home`, `dashboard`, `setup`, `interruption`, `insights`, `fake_app`.

The screen opens in the same 390×780 window with the same styling as the real app — just without the rest of the navigation wired up.

### Example commands for all 6 screens

```bash
python main.py --screen phone_home
python main.py --screen dashboard
python main.py --screen setup
python main.py --screen interruption
python main.py --screen insights
python main.py --screen fake_app
```

### Picking which app populates a screen

`interruption` and `fake_app` need to know which app they're pretending to represent. Use `--app` alongside `--screen` to pick one — it defaults to `"Instagram"` if you leave it out.

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
    │   └── mock_data.py       ← all hardcoded demo data: screen time, app list, insights,
    │                             default intention, and each app's icon/color
    ├── ui/
    │   ├── phone_home.py      ← Phone Home screen (the entry point)
    │   ├── dashboard.py       ← Dashboard screen
    │   ├── intention_setup.py ← Setup screen
    │   ├── interruption.py    ← Interruption ("still on purpose?") screen
    │   ├── insights.py        ← Insights screen
    │   ├── fake_app_screen.py ← generic "you opened the app" mock screen
    │   ├── styles.qss         ← one stylesheet for the whole app (dark theme, teal accent)
    │   └── widgets/
    │       ├── app_icon.py    ← tappable app icon (avatar + label) — used by phone_home
    │       ├── stat_card.py   ← one stat box in Dashboard (e.g. "87 Unlocks")
    │       └── usage_ring_chart.py ← Dashboard's screen-time donut chart
    └── assets/                ← icons/images (currently empty placeholders)
```

**Rule of thumb:** `core/` holds data with no UI code in it; `ui/` holds one file per full screen; `ui/widgets/` holds small reusable pieces used *inside* those screens. If you're adding a new full screen, it goes in `ui/`; if you're adding a small reusable component, it goes in `ui/widgets/`.
