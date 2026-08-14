import SwiftUI

/// Which screen is currently shown -- a minimal SwiftUI equivalent of
/// prototype/main.py's MainWindow owning a QStackedWidget + wiring
/// navigation as signal/slot connections between screens.
enum AppScreen: Equatable {
    case phoneHome
    case interruption(app: String)
    case fakeApp(app: String)
}

/// Central navigation router. Mirrors MainWindow's _wire_navigation exactly
/// for the slice implemented so far:
///   Phone Home --(tap protected app, protection on)--> Interruption
///   Phone Home --(tap non-protected app, or protection off)--> Fake App
///   Interruption --(Continue Anyway)--> Fake App
///   Interruption --(Go Back)--> Phone Home
///   Fake App --(back arrow)--> Phone Home, always
/// Dashboard/Set Your Intention are out of scope this session -- the
/// screen-time widget tap is currently a no-op rather than a dead link.
struct RootView: View {
    @EnvironmentObject var appState: AppState
    @State private var screen: AppScreen = .phoneHome

    var body: some View {
        switch screen {
        case .phoneHome:
            PhoneHomeView(
                onAppTapped: { name in
                    appState.currentApp = name
                    if appState.isProtected(name) && appState.protectionEnabled {
                        screen = .interruption(app: name)
                    } else {
                        screen = .fakeApp(app: name)
                    }
                },
                onOpenDashboard: {
                    // Dashboard isn't built this session -- no-op rather than
                    // a dead/crashing link, per the plan's stop condition.
                }
            )

        case .interruption(let app):
            InterruptionView(
                appName: app,
                intention: appState.currentIntention,
                level: appState.level(for: app),
                onContinue: { screen = .fakeApp(app: app) },
                onGoBack: { screen = .phoneHome }
            )

        case .fakeApp(let app):
            FakeAppView(appName: app, onBack: { screen = .phoneHome })
        }
    }
}
