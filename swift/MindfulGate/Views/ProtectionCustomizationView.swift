import SwiftUI

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
