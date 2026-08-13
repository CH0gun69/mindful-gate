import SwiftUI

/// Parses the "#rrggbb" hex strings used throughout MockData/the ported
/// palette (mirrors prototype/ui/styles.qss's hardcoded hex colors).
extension Color {
    init(hex: String) {
        var hexString = hex.trimmingCharacters(in: .whitespacesAndNewlines)
        hexString = hexString.replacingOccurrences(of: "#", with: "")
        var value: UInt64 = 0
        Scanner(string: hexString).scanHexInt64(&value)
        let r = Double((value >> 16) & 0xFF) / 255
        let g = Double((value >> 8) & 0xFF) / 255
        let b = Double(value & 0xFF) / 255
        self.init(red: r, green: g, blue: b)
    }
}

/// The dark-theme palette from prototype/ui/styles.qss, kept as named
/// constants so screen code reads like the Python version's objectName-keyed
/// QSS selectors instead of scattering raw hex strings everywhere.
enum Theme {
    static let background = Color(hex: "#14161a")
    static let surface = Color(hex: "#1d2026")
    static let surfacePressed = Color(hex: "#23272f")
    static let borderSubtle = Color(hex: "#22262c")
    static let borderDefault = Color(hex: "#3a3f47")
    static let textPrimary = Color(hex: "#eef0f2")
    static let textSecondary = Color(hex: "#c9cdd3")
    static let textMuted = Color(hex: "#9aa1ab")
    static let textDim = Color(hex: "#7d8590")
    static let teal = Color(hex: "#93cfc4")
    static let tealHover = Color(hex: "#a7dad1")
    static let tealOnColorText = Color(hex: "#0e1012")
    static let focusIdle = Color(hex: "#3a3f47")
    static let focusActive = Color(hex: "#3ebd5e")
    static let disabledText = Color(hex: "#6b7076")
    static let disabledBorder = Color(hex: "#2a2e34")
}
