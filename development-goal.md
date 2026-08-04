# Development Goal

Keeping the team aligned on scope, phases, and what "done" looks like for the hackathon demo.

## North star

A judge should be able to watch a 60–90 second demo and immediately get: *"this app interrupts you kindly when you're doomscrolling, based on an intention you set."*

## Phase 1 — PySide6 clickable prototype (alignment tool, PC only)

Goal: get the whole team seeing and agreeing on the flow before touching Swift.

- [ ] Dashboard screen (static mock data)
- [ ] Focus/Intention Setup screen
- [ ] Interruption screen w/ "Simulate opening Instagram" button
- [ ] Basic navigation between all screens
- [ ] Team sign-off on flow and copy
- [x] Phone home screen (mock lock screen entry point) — *scope addition, not in original plan*
- [x] Screen time widget on phone home screen (tap to open Dashboard) — *scope addition, not in original plan*

**Not in scope for Phase 1:** real usage tracking, persistence, animations/polish.

## Phase 2 — SwiftUI mock (final deliverable)

Goal: port the agreed flow into a lightweight SwiftUI app under 25 MB, offline, mock data only.

- [ ] Dashboard (hardcoded screen time + stats)
- [ ] Focus/Intention Setup (local @State, no persistence needed unless trivial)
- [ ] Interruption screen (core demo moment — polish this the most)
- [ ] Insights screen (optional, only if time allows)
- [ ] Runs on iPhone/iPad/Mac via SwiftUI multiplatform
- [ ] Confirm build size < 25 MB

## Out of scope (don't get distracted)

- Real social media integration/detection (impossible offline anyway)
- Accounts, login, backend, sync
- Real analytics or notification permissions
- Full design system — just clean and consistent enough to demo

## Definition of done

Interruption screen flow can be demoed live, end-to-end, in under 2 minutes, without crashing.
