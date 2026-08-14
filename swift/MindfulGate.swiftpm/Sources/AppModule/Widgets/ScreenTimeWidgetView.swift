import SwiftUI

struct ScreenTimeWidgetView: View {
    @EnvironmentObject var appState: AppState
    var onTap: (() -> Void)? = nil

    var body: some View {
        Button(action: { onTap?() }) {
            HStack(spacing: 14) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(MockData.currentScreenTimeToday())
                        .font(.system(size: 22, weight: .bold))
                        .foregroundStyle(Theme.teal)
                    Text(appState.t("screen_time_today"))
                        .font(.system(size: 12))
                        .foregroundStyle(Theme.textMuted)
                }
                Spacer()
                Rectangle()
                    .fill(Theme.borderDefault)
                    .frame(width: 1, height: 36)
                VStack(alignment: .trailing, spacing: 2) {
                    Text("\(MockData.unlocksToday)")
                        .font(.system(size: 18, weight: .bold))
                        .foregroundStyle(Theme.textPrimary)
                    Text(appState.t("unlocks"))
                        .font(.system(size: 11))
                        .foregroundStyle(Theme.textMuted)
                }
            }
            .padding(.horizontal, 18)
            .padding(.vertical, 14)
            .frame(minHeight: 72)
        }
        .buttonStyle(CardButtonStyle(cornerRadius: 14))
    }
}

struct CardButtonStyle: ButtonStyle {
    var cornerRadius: CGFloat
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .background(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .fill(configuration.isPressed ? Theme.surfacePressed : Theme.surface)
            )
    }
}
