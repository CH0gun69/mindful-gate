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

    func isProtected(_ appName: String) -> Bool {
        protectedApps.contains(appName)
    }

    func level(for appName: String) -> Int {
        appProtectionLevels[appName] ?? 1
    }

    func t(_ key: String) -> String {
        Strings.t(key, lang: language)
    }
}
