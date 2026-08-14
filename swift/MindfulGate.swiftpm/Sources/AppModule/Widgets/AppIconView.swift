import SwiftUI

struct AppIconView: View {
    let name: String
    var avatarSize: CGFloat = 56
    var isDecorative: Bool = false
    var glyphOverride: String? = nil
    var onTap: (() -> Void)? = nil

    private var glyph: (glyph: String, color: String) { MockData.glyph(for: name) }
    private var iconAsset: String? { isDecorative ? nil : MockData.iconAssetName(for: name) }
    private var avatarColor: Color {
        isDecorative ? Theme.borderDefault : Color(hex: glyph.color)
    }

    var body: some View {
        Button(action: { onTap?() }) {
            VStack(spacing: 6) {
                ZStack {
                    RoundedRectangle(cornerRadius: avatarSize / 4)
                        .fill(avatarColor)
                        .frame(width: avatarSize, height: avatarSize)
                    if let iconAsset {
                        Image(iconAsset)
                            .renderingMode(.template)
                            .resizable()
                            .scaledToFit()
                            .frame(width: avatarSize * 0.6, height: avatarSize * 0.6)
                            .foregroundStyle(.white)
                    } else {
                        Text(glyphOverride ?? glyph.glyph)
                            .font(.system(size: avatarSize / 2, weight: .semibold))
                            .foregroundStyle(.white)
                    }
                }
                Text(name)
                    .font(.system(size: isDecorative ? 10 : 11))
                    .foregroundStyle(isDecorative ? Theme.textMuted : Theme.textSecondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(2)
                    .frame(width: avatarSize + 20)
            }
            .padding(4)
        }
        .buttonStyle(AppIconButtonStyle())
        .frame(width: avatarSize + 20, height: avatarSize + 44)
    }
}

private struct AppIconButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(configuration.isPressed ? Theme.teal.opacity(0.15) : Color.clear)
            )
    }
}
