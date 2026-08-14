import SwiftUI

struct FeedActionButton: View {
    enum Style {
        case icon(size: CGFloat, fontSize: CGFloat)  // Instagram (34/20) or X small (28/15)
        case labeled                                  // Facebook
        case vote                                     // Reddit's ▲/▼
    }

    let icon: String
    var label: String? = nil
    let style: Style
    let flashColor: Color
    var colorOnlyFlash: Bool = false

    @State private var flashing = false

    var body: some View {
        content
            .contentShape(Rectangle())
            .onTapGesture(perform: trigger)
    }

    @ViewBuilder
    private var content: some View {
        switch style {
        case .icon(let size, let fontSize):
            Text(icon)
                .font(.system(size: fontSize))
                .foregroundStyle(flashing ? flashColor : Color(hex: "#e8e8e8"))
                .frame(width: size, height: size)
                .background(
                    Circle().fill(flashing && !colorOnlyFlash ? flashColor.opacity(0.24) : .clear)
                )
        case .labeled:
            HStack(spacing: 6) {
                Text(icon)
                Text(label ?? "")
            }
            .font(.system(size: 12, weight: .semibold))
            .foregroundStyle(flashing ? flashColor : Color(hex: "#b8b8b8"))
            .frame(maxWidth: .infinity)
            .padding(.vertical, 8)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(flashing ? flashColor.opacity(0.24) : .clear)
            )
        case .vote:
            Text(icon)
                .font(.system(size: 13))
                .foregroundStyle(flashing ? flashColor : Color(hex: "#818384"))
                .padding(8)
        }
    }

    private func trigger() {
        print("FLASH_DEBUG trigger fired for \(icon)")
        flashing = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
            flashing = false
        }
    }
}
