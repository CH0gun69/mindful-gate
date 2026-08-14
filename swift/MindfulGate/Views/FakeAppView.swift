import SwiftUI

/// Mock "you opened the app" screen, reconfigured per-app rather than one
/// bespoke screen per app. Ported from prototype/ui/fake_app_screen.py.
/// Shares one header (back button + avatar + title) across every app, then
/// picks a body style via MockData.styleFor(name). Entirely English-only,
/// no translation at all -- this is mocked "real app" content, not
/// mindful-gate's own UI copy, same reasoning as the rest of this screen.
struct FakeAppView: View {
    let appName: String
    var onBack: () -> Void = {}

    private static let avatarSize: CGFloat = 36

    private var glyph: (glyph: String, color: String) { MockData.glyph(for: appName) }
    private var iconAsset: String? { MockData.iconAssetName(for: appName) }
    private var timeSpent: String? { MockData.timeSpentTodayFor(appName) }

    var body: some View {
        VStack(spacing: 0) {
            header
            Group {
                switch MockData.styleFor(appName) {
                case "shorts":
                    ShortsBodyView(appName: appName)
                case "messages":
                    MessagesBodyView()
                default:
                    FeedBodyView(appName: appName, accentColor: Color(hex: glyph.color))
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .background(Theme.background)
        // Unlike PhoneHome/Interruption, this screen doesn't draw its own
        // fake status bar row -- respect the top safe area so the header
        // clears the Dynamic Island/notch (no such hardware concern existed
        // in the prototype's chrome-less desktop window) while still
        // letting body content run edge-to-edge at the bottom.
        .ignoresSafeArea(edges: .bottom)
        .statusBarHidden()
    }

    private var header: some View {
        HStack(spacing: 12) {
            Button(action: onBack) {
                Image(systemName: "chevron.left")
                    .font(.system(size: 18, weight: .semibold))
            }
            .buttonStyle(.plain)
            .foregroundStyle(Theme.textPrimary)

            ZStack {
                RoundedRectangle(cornerRadius: 10)
                    .fill(Color(hex: glyph.color))
                    .frame(width: Self.avatarSize, height: Self.avatarSize)
                if let iconAsset {
                    Image(iconAsset)
                        .renderingMode(.template)
                        .resizable()
                        .scaledToFit()
                        .frame(width: 22, height: 22)
                        .foregroundStyle(.white)
                } else {
                    Text(glyph.glyph)
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundStyle(.white)
                }
            }

            VStack(alignment: .leading, spacing: 0) {
                Text(appName)
                    .font(.system(size: 17, weight: .semibold))
                    .foregroundStyle(Theme.textPrimary)
                // Hardcoded English, not through Strings.t() -- this screen
                // is entirely untranslated, same as the Python source.
                if let timeSpent {
                    Text("\(timeSpent) today")
                        .font(.system(size: 11))
                        .foregroundStyle(Theme.textMuted)
                }
            }

            Spacer()
        }
        .padding(16)
        .background(Theme.background)
        .overlay(alignment: .bottom) {
            Rectangle().fill(Theme.borderSubtle).frame(height: 1)
        }
    }
}
