import SwiftUI

/// A circle that smoothly grows then shrinks on a repeating loop -- a
/// wordless breathing pulse shown during Interruption levels 2/3. Ported
/// from prototype/ui/widgets/breathing_circle.py. Fixed bounding box (the
/// frame never reflows the layout; only the drawn circle inside grows).
struct BreathingCircleView: View {
    var minDiameter: CGFloat = 36
    var maxDiameter: CGFloat = 64
    var cycleMs: Int = MockData.breathingCycleMs
    var isAnimating: Bool

    @State private var grown = false

    var body: some View {
        Circle()
            // #93cfc4 at ~40% opacity -- calm fill, no new colors introduced.
            .fill(Theme.teal.opacity(0.39))
            .frame(
                width: grown ? maxDiameter : minDiameter,
                height: grown ? maxDiameter : minDiameter
            )
            .frame(width: maxDiameter, height: maxDiameter)
            .animation(breathingAnimation, value: grown)
            .onAppear { grown = isAnimating }
            .onChange(of: isAnimating) { _, newValue in
                grown = newValue
            }
    }

    /// A single looping animation would sawtooth-reset (start -> end, snap
    /// back, repeat) rather than breathe -- repeatForever(autoreverses:
    /// true) on a half-cycle duration grows then shrinks, matching the
    /// prototype's QSequentialAnimationGroup of two chained InOutSine
    /// animations.
    private var breathingAnimation: Animation {
        isAnimating
            ? .easeInOut(duration: Double(cycleMs) / 1000 / 2).repeatForever(autoreverses: true)
            : .easeInOut(duration: 0.01)
    }
}
