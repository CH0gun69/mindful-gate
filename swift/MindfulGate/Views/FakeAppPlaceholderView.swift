import SwiftUI

/// TEMPORARY stand-in for the real Fake App screen (prototype/ui/
/// fake_app_screen.py), which is out of scope for this session per the
/// plan's priority order (PhoneHome + Interruption + navigation between
/// them only). A future session should replace this with the real
/// FakeAppView -- swap the two call sites in RootView.swift and delete this
/// file when that happens.
struct FakeAppPlaceholderView: View {
    let appName: String
    var onBack: () -> Void = {}

    var body: some View {
        VStack(spacing: 16) {
            HStack {
                Button(action: onBack) {
                    Text("←")
                        .font(.system(size: 18))
                        .foregroundStyle(Theme.textPrimary)
                        .padding(8)
                }
                Spacer()
            }
            Spacer()
            Text("You're in \(appName) now.")
                .font(.system(size: 18, weight: .semibold))
                .foregroundStyle(Theme.textPrimary)
            Text("(Fake App screen not built yet this session)")
                .font(.system(size: 12))
                .foregroundStyle(Theme.textMuted)
            Spacer()
        }
        .padding(20)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Theme.background)
        .ignoresSafeArea()
        .statusBarHidden()
    }
}
