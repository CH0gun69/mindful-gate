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
* **`development-goal.md`** — Development roadmap and project planning.
* **`README.md`** — Project overview.

## Screens

1. **Dashboard** — Screen time, quick statistics, top apps, Focus/Intention Mode toggle.
2. **Focus / Intention Setup** — Select protected apps, create an intention, and activate the experience.
3. **Interruption Screen** *(main demo)* — Simulates opening Instagram and asks whether the user is still following their intention.
4. **Insights** *(optional)* — Displays sample statistics such as intentions kept and estimated reduction in social media usage.

## Development Workflow

1. Build and iterate the UX using **Python + PySide6**.
2. Recreate the validated design in **SwiftUI**.
3. Present a polished interactive mock during the hackathon.

## Status

See **`development-goal.md`** for the current development phase, roadmap, and upcoming milestones.
