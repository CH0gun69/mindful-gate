import SwiftUI

/// Placeholder root view. Will be replaced by real navigation between the ported
/// screens (see swift/README.md's folder-mirror table):
///   PhoneHomeView, DashboardView, InterruptionView, SetYourIntentionView, FakeAppView
/// — one file each in this folder, mirroring prototype/ui/*.py. Nothing is ported yet;
/// this scaffold only confirms the package builds and opens in Swift Playgrounds.
struct ContentView: View {
    var body: some View {
        VStack(spacing: 12) {
            Text("MindfulGate")
                .font(.largeTitle.bold())
            Text("SwiftUI port scaffold — no screens ported yet.\nSource of truth: prototype/ (Python).")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
