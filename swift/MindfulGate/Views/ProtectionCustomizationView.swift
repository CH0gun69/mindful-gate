import SwiftUI

/// Single combined destination for setting up protection: pick which apps to
/// protect, write an intention message, and set each app's friction level
/// (1/2/3). Ported from prototype/ui/protection_customization.py.
///
/// The overall on/off switch lives on Dashboard only (Activate/Deactivate
/// Focus Mode) -- this screen has no master toggle of its own; every change
/// here applies live/instantly via `appState`, same as the Python version's
/// per-app switch/level-slider/intention-field signals.
///
/// Per swift/HANDOFF.md: the Python ToggleSwitch/LevelSlider are
/// deliberately NOT recreated as custom controls here -- native SwiftUI
/// `Toggle`/`Slider` are used instead.
struct ProtectionCustomizationView: View {
    var onGoBack: () -> Void = {}

    @EnvironmentObject var appState: AppState
    @State private var intentionText: String = ""

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                VStack(alignment: .leading, spacing: 16) {
                    Text(appState.t("set_your_intention_title"))
                        .font(.system(size: 24, weight: .semibold))
                        .foregroundStyle(Theme.textPrimary)

                    Text(appState.t("protection_subtitle"))
                        .font(.system(size: 13))
                        .foregroundStyle(Theme.textMuted)
                }
                .padding(.bottom, 4)

                VStack(spacing: 10) {
                    ForEach(MockData.protectableApps, id: \.self) { app in
                        appRow(app)
                    }
                }

                Text(appState.t("your_message"))
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Theme.textSecondary)
                    .padding(.top, 8)

                // User input -- never translated, same rule as
                // Interruption's intention quote. Committed on submit
                // (Python's editingFinished == field losing focus), not on
                // every keystroke, so a stray backspace mid-typing can't
                // briefly interrupt with an empty/partial intention.
                TextField(MockData.defaultIntention, text: $intentionText, onCommit: commitIntention)
                    .font(.system(size: 14))
                    .foregroundStyle(Theme.textPrimary)
                    .padding(10)
                    .background(RoundedRectangle(cornerRadius: 8).fill(Theme.surface))
                    .overlay(RoundedRectangle(cornerRadius: 8).stroke(Theme.borderDefault, lineWidth: 1))
                    .onAppear { intentionText = appState.currentIntention }
                    .onSubmit(commitIntention)

                Button(action: onGoBack) {
                    Text(appState.t("back"))
                }
                .buttonStyle(LinkButtonStyle())
            }
            .padding(32)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Theme.background)
    }

    private func commitIntention() {
        let trimmed = intentionText.trimmingCharacters(in: .whitespacesAndNewlines)
        appState.currentIntention = trimmed.isEmpty ? MockData.defaultIntention : trimmed
        intentionText = appState.currentIntention
    }

    @ViewBuilder
    private func appRow(_ app: String) -> some View {
        let isOn = appState.isProtected(app)
        let glyph = MockData.glyph(for: app)
        let iconAsset = MockData.iconAssetName(for: app)

        VStack(spacing: 6) {
            HStack(spacing: 10) {
                ZStack {
                    RoundedRectangle(cornerRadius: 10)
                        .fill(Color(hex: glyph.color))
                        .frame(width: 40, height: 40)
                    if let iconAsset {
                        Image(iconAsset)
                            .renderingMode(.template)
                            .resizable()
                            .scaledToFit()
                            .frame(width: 24, height: 24)
                            .foregroundStyle(.white)
                    } else {
                        Text(glyph.glyph)
                            .font(.system(size: 18, weight: .semibold))
                            .foregroundStyle(.white)
                    }
                }

                Text(app)
                    .font(.system(size: 14, weight: .medium))
                    .foregroundStyle(Theme.textPrimary)

                Spacer()

                Toggle("", isOn: Binding(
                    get: { isOn },
                    set: { newValue in
                        if newValue {
                            appState.protectedApps.insert(app)
                        } else {
                            appState.protectedApps.remove(app)
                        }
                    }
                ))
                .labelsHidden()
                .tint(Theme.teal)
            }

            // Collapsible level control -- only meaningful/visible while
            // Protect is on, revealed with a smooth expand/collapse like the
            // Python version's animated maximumHeight.
            if isOn {
                levelRow(app)
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
        .padding(8)
        .background(RoundedRectangle(cornerRadius: 8).fill(Theme.surface))
        .animation(.easeInOut(duration: 0.18), value: isOn)
    }

    private func levelRow(_ app: String) -> some View {
        let level = appState.level(for: app)
        return HStack(spacing: 8) {
            Text(appState.t("level_label").filling(["level": "\(level)"]))
                .font(.system(size: 13, weight: .semibold))
                .foregroundStyle(Theme.textSecondary)
                .frame(minWidth: 60, alignment: .leading)

            Slider(
                value: Binding(
                    get: { Double(level) },
                    set: { appState.appProtectionLevels[app] = Int($0.rounded()) }
                ),
                in: 1...3,
                step: 1
            )
            .tint(Theme.teal)
            .frame(width: 140)

            Spacer()
        }
        .padding(.leading, 50)
    }
}

#Preview {
    ProtectionCustomizationView()
        .environmentObject(AppState())
        .preferredColorScheme(.dark)
}
