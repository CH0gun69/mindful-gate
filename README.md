# mindful-gate

> **Hackathon Project**
> This repository contains the prototype and development materials for our SwiftUI hackathon project. The goal is to demonstrate a digital wellbeing concept through a polished mock UI and user experience, rather than build a production-ready application.

A Digital Wellbeing–style mock app that reduces mindless social media scrolling through **intentions + gentle interruptions**.

## Concept

Instead of hard blocking, **mindful-gate** asks users to set a short intention before opening a protected social app (e.g. *"Only reply to messages"* or *"Max 10 minutes"*). When the app is "opened" during the demo, a calm full-screen interruption appears and asks:

> **"You opened Instagram. Are you still on purpose?"**

The experience encourages mindful decision-making instead of restricting users with hard limits.

## Hackathon Context

This project is being developed for a **Swift/iOS hackathon**.

To match the competition requirements, the repository focuses on demonstrating the user experience rather than implementing a production-ready digital wellbeing system.

### Competition Constraints

* Final application written in **SwiftUI**
* Offline only (no internet or cloud services)
* Compatible with **iPhone, iPad, and Mac**
* Project size under **25 MB**
* Mock UI and interaction flow only
* Uses hardcoded sample data for demonstration

## Repository Structure

* **`prototype/`** — Python + PySide6 interactive prototype used to validate the UX flow before implementation in SwiftUI.
* **`swift/`** — SwiftUI port destination, Swift Playgrounds App Playground (`.swiftpm`); scaffolding only so far, see `swift/README.md`.
* **`development-goal.md`** — Development roadmap and project planning.
* **`README.md`** — Project overview.

## Screens

1. **Dashboard** — Screen time, quick statistics, top apps, Focus/Intention Mode toggle.
2. **Set Your Intention** — Select protected apps, set each one's 1–3 protection level (how much calm friction — delay, breathing prompt, reaffirm tap — the Interruption screen adds before letting the user continue), write an intention, and toggle protection on/off.
3. **Interruption Screen** *(main demo)* — Simulates opening Instagram and asks whether the user is still following their intention.

## Development Workflow

1. Build and iterate the UX using **Python + PySide6**.
2. Recreate the validated design in **SwiftUI**.
3. Present a polished interactive mock during the hackathon.

## Status

See **`development-goal.md`** for the current development phase, roadmap, and upcoming milestones.
