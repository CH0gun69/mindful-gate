import SwiftUI

struct BreathingCircleView: View {
    var minDiameter: CGFloat = 36
    var maxDiameter: CGFloat = 64
    var cycleMs: Int = MockData.breathingCycleMs
    var isAnimating: Bool

    @State private var grown = false

    var body: some View {
        Circle()
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

    private var breathingAnimation: Animation {
        isAnimating
            ? .easeInOut(duration: Double(cycleMs) / 1000 / 2).repeatForever(autoreverses: true)
            : .easeInOut(duration: 0.01)
    }
}
