import SwiftUI

/// Filled teal button (QPushButton#primaryBtn) -- Interruption's "Go Back",
/// always enabled, always the escape hatch.
struct PrimaryButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 14, weight: .semibold))
            .foregroundStyle(Theme.tealOnColorText)
            .frame(maxWidth: .infinity)
            .padding(12)
            .background(
                RoundedRectangle(cornerRadius: 10)
                    .fill(configuration.isPressed ? Theme.tealHover : Theme.teal)
            )
    }
}

/// Outlined button (QPushButton#secondaryBtn) with an explicit disabled
/// look (color #6b7076, border #2a2e34) -- Interruption's "Continue Anyway",
/// gated by protection level.
struct SecondaryButtonStyle: ButtonStyle {
    var isEnabled: Bool

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 14))
            .foregroundStyle(isEnabled ? Theme.textPrimary : Theme.disabledText)
            .frame(maxWidth: .infinity)
            .padding(12)
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(isEnabled ? Theme.borderDefault : Theme.disabledBorder, lineWidth: 1)
            )
    }
}
