# swift/ — SwiftUI port (Phase 2)

This is the SwiftUI port destination for mindful-gate's final deliverable (see root
[`development-goal.md`](../development-goal.md), Phase 2). It is a Swift Playgrounds
**App Playground** project (`.swiftpm` package format), not an Xcode project.

## Source of truth

[`../prototype/`](../prototype/) (the Python/PySide6 clickable prototype) is the UX and
behavior source of truth. Nothing here should invent new flow or copy — it's a straight
port. When picking up porting work, diff against the current state of
`prototype/core/` and `prototype/ui/` first.

## Folder mirror

| prototype/                              | swift/MindfulGate.swiftpm/Sources/AppModule/ |
| ---------------------------------------- | --------------------------------------------- |
| `core/mock_data.py`, `core/strings.py`   | `Core/` — will hold `MockData.swift`, `Strings.swift` |
| `ui/*.py` (5 screens)                    | `Views/` — will hold one file per screen (`PhoneHomeView.swift`, `DashboardView.swift`, `InterruptionView.swift`, `SetYourIntentionView.swift`, `FakeAppView.swift`) |
| `ui/widgets/*.py`                        | `Views/Widgets/` — one reusable component per file |

Nothing has been ported yet — this commit is scaffolding only.

## Build/test workflow

This dev machine is Linux and cannot compile or run SwiftUI. All building and testing
happens **on iPad, in Swift Playgrounds**:

1. Pull the latest commit on iPad via **Working Copy**.
2. Open `swift/MindfulGate.swiftpm` from Working Copy's Files integration in
   **Swift Playgrounds**.
3. Edit/build/run there. Commit and push back through Working Copy.

The very first thing to do after picking this up on iPad is confirm the project opens
and runs as-is — that hasn't been verified yet (this scaffold was built and only
sanity-checked on a Linux machine, never compiled).

## Known deferred items

- `Package.swift` currently targets `.pad` and `.phone` device families only, not
  `.mac` — CLAUDE.md/README.md's iPhone/iPad/Mac goal is deferred until there's an
  actual Mac available to verify Mac Catalyst support on.
- App icon/accent color use Swift Playgrounds' built-in placeholder system
  (`.placeholder(icon: .leaf)`, `.presetColor(.teal)` — teal matches the prototype's
  real brand accent, `#93cfc4` in `prototype/core/mock_data.py`) rather than a custom
  asset catalog. Swap for a real icon later using Swift Playgrounds' own on-device icon
  editor.
