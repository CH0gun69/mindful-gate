import SwiftUI

/// App entry point. Mirrors prototype/main.py's MainWindow at the top level — real
/// screen navigation gets wired up here once views are ported (see swift/README.md).
@main
struct MindfulGateApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
