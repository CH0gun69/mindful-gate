import SwiftUI

/// Which screen is currently shown -- a minimal SwiftUI equivalent of
/// prototype/main.py's MainWindow owning a QStackedWidget + wiring
/// navigation as signal/slot connections between screens.
enum AppScreen: Equatable {
    case phoneHome
    case interruption(app: String)
    case fakeApp(app: String)
    case dashboard
    case protectionCustomization
}

/// Central navigation router. Mirrors MainWindow's _wire_navigation:
///   Phone Home --(tap protected app, protection on)--> Interruption
///   Phone Home --(tap non-protected app, or protection off)--> Fake App
///   Phone Home --(tap screen-time widget)--> Dashboard
///   Interruption --(Continue Anyway)--> Fake App
///   Interruption --(Go Back)--> Phone Home
///   Fake App --(back arrow)--> Phone Home, always
///   Dashboard --(Set your intention)--> Set Your Intention
///   Dashboard --(Home)--> Phone Home
///   Set Your Intention --(Back)--> Dashboard
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
                onOpenDashboard: { screen = .dashboard }
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

        case .dashboard:
            DashboardView(
                onGoToProtection: { screen = .protectionCustomization },
                onGoHome: { screen = .phoneHome }
            )

        case .protectionCustomization:
            ProtectionCustomizationView(onGoBack: { screen = .dashboard })
        }
    }
}
