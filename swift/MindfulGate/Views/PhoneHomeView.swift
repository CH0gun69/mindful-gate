import SwiftUI

/// Mock phone lock/home screen -- the entry point of the app. Ported from
/// prototype/ui/phone_home.py. Tapping any app icon fires onAppTapped(name)
/// -- the caller (navigation, wired in a later step) decides whether that
/// means showing the Interruption screen or opening the Fake App directly.
/// Dock icons stay inert, matching the prototype.
struct PhoneHomeView: View {
    @EnvironmentObject var appState: AppState

    var onAppTapped: (String) -> Void = { _ in }
    var onOpenDashboard: () -> Void = {}

    private static let gridColumns = 4

    /// Merge topApps + protectableApps into one ordered name list, same as
    /// prototype's _build_app_roster() -- Instagram, YouTube, TikTok,
    /// Messages, X (Twitter), Facebook, Reddit.
    private var appRoster: [String] {
        var names = MockData.topApps.map(\.name)
        for name in MockData.protectableApps where !names.contains(name) {
            names.append(name)
        }
        return names
    }

    private let dockApps: [(glyph: String, name: String)] = [
        ("📞", "Phone"), ("📷", "Camera"), ("⚙", "Settings"), ("💬", "Messages"),
    ]

    private let gridItems = Array(
        repeating: GridItem(.flexible(), spacing: 12),
        count: 4
    )

    var body: some View {
        VStack(spacing: 0) {
            statusBar
            appGrid
            screenTimeSection
            controlsRow
            Spacer(minLength: 0)
            dock
        }
        .padding(.bottom, 20)
        .background(Theme.background)
        // This screen draws its own fake status bar (matching the Python
        // prototype's fixed 390x780 "phone" window, no real OS chrome around
        // it) -- ignore the real device safe area and hide the real iOS
        // status bar so we don't stack real system chrome on top of our
        // simulated one.
        .ignoresSafeArea()
        .statusBarHidden()
    }

    private var statusBar: some View {
        HStack {
            Text("9:41")
                .font(.system(size: 15, weight: .semibold))
                .foregroundStyle(Theme.textPrimary)
            Spacer()
            Text("•••  5G  🔋")
                .font(.system(size: 12))
                .foregroundStyle(Theme.textMuted)
        }
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
        .background(Theme.background)
        .overlay(alignment: .bottom) {
            Rectangle().fill(Theme.borderSubtle).frame(height: 1)
        }
    }

    private var appGrid: some View {
        LazyVGrid(columns: gridItems, spacing: 24) {
            ForEach(appRoster, id: \.self) { name in
                AppIconView(name: name) {
                    onAppTapped(name)
                }
            }
        }
        .padding(.horizontal, 20)
        .padding(.top, 32)
        .padding(.bottom, 16)
    }

    private var screenTimeSection: some View {
        ScreenTimeWidgetView(onTap: onOpenDashboard)
            .padding(.horizontal, 20)
            .padding(.vertical, 8)
    }

    /// Three compact referee/demo utility controls: Shuffle (randomize mock
    /// usage data live), Light/Dark, TH/EN. Always English-only labels, same
    /// as the prototype -- these are meta/demo controls, not simulated phone
    /// UI. Light/Dark and TH/EN currently just flip AppState + their own
    /// label; the full palette/translation swap is a later-stage item.
    private var controlsRow: some View {
        HStack(spacing: 8) {
            miniControlButton("🔀 \(Strings.t("shuffle"))") { appState.shuffle() }
            miniControlButton(appState.darkMode ? "☀️ Light" : "🌙 Dark") { appState.toggleTheme() }
            miniControlButton(appState.language == "en" ? "TH" : "EN") { appState.toggleLanguage() }
        }
        .padding(.horizontal, 20)
    }

    private func miniControlButton(_ title: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Text(title)
                .font(.system(size: 12))
                .frame(maxWidth: .infinity)
                .padding(.vertical, 2)
        }
        .buttonStyle(.bordered)
        .buttonBorderShape(.capsule)
        .tint(Theme.textSecondary)
    }

    private var dock: some View {
        HStack(spacing: 8) {
            ForEach(dockApps, id: \.name) { app in
                AppIconView(name: app.name, avatarSize: 44, isDecorative: true, glyphOverride: app.glyph)
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 10)
        .background(RoundedRectangle(cornerRadius: 20).fill(Theme.surface))
        .padding(.horizontal, 20)
    }
}

#Preview {
    PhoneHomeView()
        .environmentObject(AppState())
        .preferredColorScheme(.dark)
}
