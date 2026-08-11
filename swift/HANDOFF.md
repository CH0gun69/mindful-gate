# Swift port handoff — received 2026-08-11, for a future Mac session

The content below was provided verbatim by the project owner in a Linux Claude Code
session on 2026-08-11, specifically to be picked up by a **future Claude Code session
running on a MacBook with Xcode**, planned for Thursday. The Linux session that received
it took no action on `swift/` or the porting work itself — this file is purely additive
documentation, added at the owner's request so the plan below doesn't only exist in a
chat transcript.

If you are the Claude Code instance in that future Mac session: the "STOP" section
below was addressed to the Linux session that received this doc, not to you. Skip past
it to "Swift port — handoff to Mac session (Thursday)" and follow those instructions.

---

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
