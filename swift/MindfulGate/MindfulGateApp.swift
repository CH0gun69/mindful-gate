import SwiftUI

@main
struct MindfulGateApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environmentObject(appState)
                .preferredColorScheme(appState.darkMode ? .dark : .light)
        }
    }
}
