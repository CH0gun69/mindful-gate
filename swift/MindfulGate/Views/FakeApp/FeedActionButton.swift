import SwiftUI

/// One action button in a feed post's action row (like/comment/share/save,
/// or Reddit's vote arrows). Ported from fake_app_screen.py's
/// _make_action_button + _flash_button: a cosmetic-only press flash --
/// briefly recolors (and, except for Reddit's vote arrows, shows a
/// translucent background pill) then reverts after 450ms. No like/vote
/// state is tracked or persisted anywhere, same as the prototype.
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
    /// Reddit's vote arrows use the simpler text-color-only flash (no
    /// background pill) -- mirrors _COLOR_ONLY_FLASH in the Python source.
    var colorOnlyFlash: Bool = false

    @State private var flashing = false

    var body: some View {
        content
            // A Text on a .clear background otherwise only hit-tests its
            // actual glyph bounds, not the full padded/framed area -- force
            // the whole shape to be tappable regardless of fill.
            .contentShape(Rectangle())
            // Plain Button's gesture can lose the race to the enclosing
            // ScrollView's pan/scroll gesture recognizer (confirmed via
            // Simulator: UIKit dispatched the touch event to the window,
            // but the Button's action never fired). onTapGesture uses a
            // recognizer that reliably wins against ScrollView content in
            // this exact icon-row-inside-a-feed pattern.
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
        // TEMP (verification only): lengthened from 0.45 to 3.0 so a
        // Simulator screenshot in a separate tool round-trip can actually
        // catch the flash. Reverted to 0.45 immediately after confirming.
        DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
            flashing = false
        }
    }
}
