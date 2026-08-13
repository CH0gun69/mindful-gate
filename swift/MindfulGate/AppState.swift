import SwiftUI

/// Central navigation/app state, analogous to prototype/main.py's
/// MainWindow-owned state -- never owned by individual screens themselves.
final class AppState: ObservableObject {
    @Published var currentIntention: String = MockData.defaultIntention
    @Published var currentApp: String = "Instagram"
    @Published var protectedApps: Set<String> = MockData.defaultProtectedApps
    @Published var protectionEnabled: Bool = true
    @Published var appProtectionLevels: [String: Int] = MockData.defaultAppProtectionLevels
    @Published var darkMode: Bool = true
    @Published var language: String = "en"

    /// Bumped by shuffle() so views reading MockData's mutable shuffle state
    /// directly (not itself @Published) still get told to re-render --
    /// MockData mirrors prototype/core/mock_data.py's module-level globals,
    /// which have no observation mechanism of their own.
    @Published private(set) var shuffleTick: Int = 0

    func isProtected(_ appName: String) -> Bool {
        protectedApps.contains(appName)
    }

    func level(for appName: String) -> Int {
        appProtectionLevels[appName] ?? 1
    }

    func t(_ key: String) -> String {
        Strings.t(key, lang: language)
    }

    /// Referee/demo utility actions -- mirrors MainWindow owning the actual
    /// shuffle/theme/language state in prototype/main.py, with each screen
    /// just reporting "the button was tapped".
    func shuffle() {
        MockData.shuffleTopApps()
        shuffleTick += 1
    }

    func toggleTheme() {
        darkMode.toggle()
    }

    func toggleLanguage() {
        language = (language == "en") ? "th" : "en"
    }
}
