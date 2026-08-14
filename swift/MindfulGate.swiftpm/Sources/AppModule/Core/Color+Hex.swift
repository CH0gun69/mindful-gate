import SwiftUI

/// แปลง hex string ("#rrggbb") เป็นสี ใช้กับค่าสีทั้งหมดใน MockData/Theme
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

/// ชุดสีของแอป รองรับทั้งโหมดมืด/สว่าง (ports prototype/ui/styles.qss +
/// styles_light.qss). `isDark` ถูกอัปเดตจาก AppState.darkMode ทุกครั้งที่
/// ผู้ใช้กดสลับธีม -- View เดิมยังคงเรียก `Theme.xxx` เหมือนเดิมทุกที่
/// ไม่ต้องแก้โค้ดที่อื่น. สีแบรนด์ (teal, focusActive) เหมือนกันทั้งสองธีม
/// ตามต้นฉบับ Python.
enum Theme {
    static var isDark: Bool = true

    static var background: Color { isDark ? Color(hex: "#14161a") : Color(hex: "#f4f5f7") }
    static var surface: Color { isDark ? Color(hex: "#1d2026") : Color(hex: "#ffffff") }
    static var surfacePressed: Color { isDark ? Color(hex: "#23272f") : Color(hex: "#e5e7ea") }
    static var borderSubtle: Color { isDark ? Color(hex: "#22262c") : Color(hex: "#e2e4e8") }
    static var borderDefault: Color { isDark ? Color(hex: "#3a3f47") : Color(hex: "#d7dade") }
    static var textPrimary: Color { isDark ? Color(hex: "#eef0f2") : Color(hex: "#14161a") }
    static var textSecondary: Color { isDark ? Color(hex: "#c9cdd3") : Color(hex: "#3a3f47") }
    static var textMuted: Color { isDark ? Color(hex: "#9aa1ab") : Color(hex: "#6b7280") }
    static var textDim: Color { isDark ? Color(hex: "#7d8590") : Color(hex: "#6b7280") }
    static let teal = Color(hex: "#93cfc4")
    static let tealHover = Color(hex: "#a7dad1")
    static let tealOnColorText = Color(hex: "#0e1012")
    static var focusIdle: Color { isDark ? Color(hex: "#3a3f47") : Color(hex: "#e2e4e8") }
    static let focusActive = Color(hex: "#3ebd5e")
    static var disabledText: Color { isDark ? Color(hex: "#6b7076") : Color(hex: "#9199a3") }
    static var disabledBorder: Color { isDark ? Color(hex: "#2a2e34") : Color(hex: "#e2e4e8") }
}
