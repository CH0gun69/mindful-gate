import SwiftUI

/// App entry point. Mirrors prototype/main.py's MainWindow at the top level.
@main
struct MindfulGateApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            PhoneHomeView()
                .environmentObject(appState)
                .preferredColorScheme(.dark)
        }
    }
}
