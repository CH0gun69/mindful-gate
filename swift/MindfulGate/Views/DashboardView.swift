import SwiftUI

/// Screen time today (ring + legend) + Focus Mode toggle + link to Set Your
/// Intention. Ported from prototype/ui/dashboard.py.
struct DashboardView: View {
    var onGoToProtection: () -> Void = {}
    var onGoHome: () -> Void = {}

    @EnvironmentObject var appState: AppState

    private var breakdown: [UsageRingChart.Segment] {
        // Reads MockData.usageBreakdown() fresh on every render, gated by
        // appState.shuffleTick so a Shuffle tap (on Phone Home) is reflected
        // here too -- same "re-render, don't own a private copy" idea as
        // the Python DashboardScreen.refresh_usage_data().
        _ = appState.shuffleTick
        return MockData.usageBreakdown().map {
            UsageRingChart.Segment(name: $0.name, minutes: $0.minutes, color: $0.color)
        }
    }

    private var isHigh: Bool {
        _ = appState.shuffleTick
        return MockData.isHighUsage()
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text(appState.t("dashboard_title"))
                    .font(.system(size: 24, weight: .semibold))
                    .foregroundStyle(Theme.textPrimary)

                screenTimeCard

                HStack(spacing: 12) {
                    StatCard(label: appState.t("unlocks"), value: "\(MockData.unlocksToday)")
                    StatCard(label: appState.t("notifications"), value: "\(MockData.notificationsToday)")
                }

                Text(appState.t("focus_mode"))
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundStyle(Theme.textSecondary)
                    .padding(.top, 8)

                Button(action: { appState.protectionEnabled.toggle() }) {
                    Text(appState.t(appState.protectionEnabled ? "deactivate_focus_mode" : "activate_focus_mode"))
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundStyle(Theme.tealOnColorText)
                        .frame(maxWidth: .infinity)
                        .padding(12)
                }
                .background(
                    RoundedRectangle(cornerRadius: 10)
                        .fill(appState.protectionEnabled ? Theme.focusActive : Theme.focusIdle)
                )
                .foregroundStyle(appState.protectionEnabled ? Theme.tealOnColorText : Theme.textPrimary)

                Button(action: onGoToProtection) {
                    Text(appState.t("set_your_intention"))
                }
                .buttonStyle(LinkButtonStyle())

                Button(action: onGoHome) {
                    Text(appState.t("home"))
                }
                .buttonStyle(LinkButtonStyle())
            }
            .padding(32)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Theme.background)
    }

    private var screenTimeCard: some View {
        VStack(spacing: 16) {
            HStack(alignment: .top, spacing: 16) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(MockData.currentScreenTimeToday())
                        .font(.system(size: 44, weight: .bold))
                        .foregroundStyle(Color(hex: MockData.usageColor(isHigh: isHigh)))
                    Text(appState.t("screen_time_today"))
                        .font(.system(size: 13))
                        .foregroundStyle(Theme.textMuted)
                }
                Spacer()
                UsageRingChart(segments: breakdown)
            }

            VStack(spacing: 10) {
                ForEach(breakdown, id: \.name) { segment in
                    legendRow(segment: segment)
                }
            }
        }
        .padding(18)
        .background(RoundedRectangle(cornerRadius: 14).fill(Theme.surface))
    }

    private func legendRow(segment: UsageRingChart.Segment) -> some View {
        let entry = MockData.usageBreakdown().first { $0.name == segment.name }
        return HStack(spacing: 10) {
            Circle()
                .fill(Color(hex: segment.color))
                .overlay(Circle().stroke(Theme.borderDefault, lineWidth: 1))
                .frame(width: 10, height: 10)

            Text(segment.name)
                .font(.system(size: 14, weight: .medium))
                .foregroundStyle(Theme.textPrimary)

            if appState.isProtected(segment.name) {
                Text(appState.t("protected"))
                    .font(.system(size: 11))
                    .foregroundStyle(Theme.teal)
            }

            Spacer()

            Text(entry?.timeString ?? "")
                .font(.system(size: 13))
                .foregroundStyle(Theme.textMuted)
        }
    }
}

/// Underlined, muted text-only button (QPushButton#linkBtn) -- "Set your
/// intention" / "Home" on Dashboard, "Back" on Set Your Intention.
struct LinkButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 13))
            .underline()
            .foregroundStyle(Theme.textMuted)
            .opacity(configuration.isPressed ? 0.7 : 1)
    }
}

#Preview {
    DashboardView()
        .environmentObject(AppState())
        .preferredColorScheme(.dark)
}
