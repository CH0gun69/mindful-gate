import SwiftUI

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
