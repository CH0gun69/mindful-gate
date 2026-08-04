# mindful-gate

A Digital Wellbeing–style mock app that reduces mindless social media scrolling through **intentions + gentle interruptions**.

## Concept

Instead of hard blocking, mindful-gate asks you to set a short intention before using a protected social app (e.g. *"Only reply to messages"* or *"Max 10 minutes"*). When you open that app, a calm full-screen interruption checks in: **are you still on purpose?**

## Constraints (hackathon)

- Written in Swift (final version)
- Offline only — no internet/network calls
- Runs on iPhone, iPad, and Mac
- Project size under 25 MB
- Mock UI / process only — not a fully functional real app

## Screens

1. **Dashboard** — screen time, quick stats, top-apps list, Focus/Intention Mode toggle
2. **Focus / Intention Setup** — pick apps to protect, write an intention, activate
3. **Interruption Screen** *(the demo moment)* — triggered by a "Simulate opening Instagram" button, shows your intention, asks "Still on purpose?" with Continue / Go Back
4. **Insights** *(optional)* — fake stats: intentions kept, social time reduced

## Tech approach

1. **Prototype** — interactive mock built in Python + PySide6 to align the team on flow
2. **Final build** — SwiftUI mock app with hardcoded data / simple local state

## Status

See [development-goal.md](./development-goal.md) for the current phase and roadmap.
