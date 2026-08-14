import SwiftUI

struct PhoneHomeView: View {
    @EnvironmentObject var appState: AppState

    var onAppTapped: (String) -> Void = { _ in }
    var onOpenDashboard: () -> Void = {}

    private static let gridColumns = 4

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
