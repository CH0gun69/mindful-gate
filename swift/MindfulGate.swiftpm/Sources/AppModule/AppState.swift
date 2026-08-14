import SwiftUI

final class AppState: ObservableObject {
    @Published var currentIntention: String = MockData.defaultIntention
    @Published var currentApp: String = "Instagram"
    @Published var protectedApps: Set<String> = MockData.defaultProtectedApps
    @Published var protectionEnabled: Bool = true
    @Published var appProtectionLevels: [String: Int] = MockData.defaultAppProtectionLevels
    @Published var darkMode: Bool = true {
        didSet { Theme.isDark = darkMode }
    }
    @Published var language: String = "en"

    @Published private(set) var shuffleTick: Int = 0

    @Published private(set) var unlocksToday: Int = MockData.unlocksToday
    @Published private(set) var notificationsToday: Int = MockData.notificationsToday

    func isProtected(_ appName: String) -> Bool {
        protectedApps.contains(appName)
    }

    func level(for appName: String) -> Int {
        appProtectionLevels[appName] ?? 1
    }

    func t(_ key: String) -> String {
        Strings.t(key, lang: language)
    }

    func shuffle() {
        MockData.shuffleTopApps()
        unlocksToday = Int.random(in: 40...150)
        notificationsToday = Int.random(in: 50...260)
        shuffleTick += 1
    }

    func toggleTheme() {
        darkMode.toggle()
    }

    func toggleLanguage() {
        language = (language == "en") ? "th" : "en"
    }
}
