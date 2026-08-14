import SwiftUI

enum AppScreen: Equatable {
    case phoneHome
    case interruption(app: String)
    case fakeApp(app: String)
    case dashboard
    case protectionCustomization
}

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
