import SwiftUI

/// App entry point. Mirrors prototype/main.py's MainWindow at the top level.
@main
struct MindfulGateApp: App {
    var body: some Scene {
        WindowGroup {
            Text("MindfulGate")
                .font(.largeTitle)
        }
    }
}
