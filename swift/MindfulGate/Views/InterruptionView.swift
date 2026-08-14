import SwiftUI

/// "You opened {app}. Still on purpose?" gate screen. Ported from
/// prototype/ui/interruption.py. Per-level gating (delay/breathing/reaffirm)
/// lives in InterruptionTimerModel; this view is purely presentational.
struct InterruptionView: View {
    let appName: String
    let intention: String
    let level: Int
    var onContinue: () -> Void = {}
    var onGoBack: () -> Void = {}

    @EnvironmentObject var appState: AppState
    @StateObject private var timer = InterruptionTimerModel()

    private static let avatarSize: CGFloat = 72

    private var glyph: (glyph: String, color: String) { MockData.glyph(for: appName) }
    private var iconAsset: String? { MockData.iconAssetName(for: appName) }
    private var timeSpent: String? { MockData.timeSpentTodayFor(appName) }

    private var continueText: String {
        // Once the delay elapses -- whether Continue auto-enabled or is
        // waiting on a reaffirm tap -- drop the countdown suffix rather than
        // show a stale "(0s)" next to a button that isn't about to unlock
        // on its own (reaffirm case) or is already unlocked (auto case).
        if timer.isContinueEnabled || timer.showReaffirm {
            return appState.t("continue_anyway")
        }
        return appState.t("continue_anyway_countdown").filling(["seconds": "\(timer.secondsLeft)"])
    }

    var body: some View {
        VStack(spacing: 24) {
            Text(appState.t("you_opened").filling(["app": appName]))
                .font(.system(size: 18))
                .foregroundStyle(Theme.textMuted)
                .multilineTextAlignment(.center)

            Text(appState.t("still_on_purpose"))
                .font(.system(size: 30, weight: .bold))
                .foregroundStyle(Theme.textPrimary)
                .multilineTextAlignment(.center)

            Text("“\(intention)”")
                .font(.system(size: 16))
                .italic()
                .foregroundStyle(Theme.teal)
                .multilineTextAlignment(.center)
                .padding(16)
                .background(RoundedRectangle(cornerRadius: 10).fill(Theme.surface))

            if let timeSpent {
                Text(appState.t("time_spent_nudge").filling(["time": timeSpent, "app": appName]))
                    .font(.system(size: 12))
                    .foregroundStyle(Theme.textDim)
                    .multilineTextAlignment(.center)
            }

            if timer.showReaffirm {
                Button(action: { timer.reaffirmTapped() }) {
                    Text(appState.t("still_on_purpose"))
                        .font(.system(size: 13))
                }
                .buttonStyle(.bordered)
                .buttonBorderShape(.capsule)
                .tint(Theme.teal)
            }

            Spacer()

            ZStack {
                RoundedRectangle(cornerRadius: Self.avatarSize / 4)
                    .fill(Color(hex: glyph.color))
                    .frame(width: Self.avatarSize, height: Self.avatarSize)
                if let iconAsset {
                    Image(iconAsset)
                        .renderingMode(.template)
                        .resizable()
                        .scaledToFit()
                        .frame(width: Self.avatarSize * 0.6, height: Self.avatarSize * 0.6)
                        .foregroundStyle(.white)
                } else {
                    Text(glyph.glyph)
                        .font(.system(size: Self.avatarSize / 2, weight: .semibold))
                        .foregroundStyle(.white)
                }
            }

            if timer.isBreathing {
                BreathingCircleView(isAnimating: true)
            }

            Spacer()
            Spacer()

            Button(action: onGoBack) {
                Text(appState.t("go_back"))
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Theme.tealOnColorText)
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            .tint(Theme.teal)

            Button(action: onContinue) {
                Text(continueText)
                    .font(.system(size: 14))
                    .foregroundStyle(timer.isContinueEnabled ? Theme.textPrimary : Theme.disabledText)
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.bordered)
            .tint(timer.isContinueEnabled ? Theme.borderDefault : Theme.disabledBorder)
            .disabled(!timer.isContinueEnabled)
        }
        .padding(.horizontal, 48)
        .padding(.top, 64)
        .padding(.bottom, 48)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Theme.background)
        .ignoresSafeArea()
        .statusBarHidden()
        .onAppear { timer.setContext(level: level) }
        .onDisappear { timer.stopTimers() }
    }
}

#Preview {
    InterruptionView(appName: "TikTok", intention: MockData.defaultIntention, level: 3)
        .environmentObject(AppState())
        .preferredColorScheme(.dark)
}
