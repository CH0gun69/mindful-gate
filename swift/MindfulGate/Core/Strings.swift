import Foundation

enum Strings {
    static let defaultLanguage = "en"

    static let table: [String: [String: String]] = [
        "en": [
            // แดชบอร์ด
            "dashboard_title": "Dashboard",
            "screen_time_today": "Screen time today",
            "unlocks": "Unlocks",
            "notifications": "Notifications",
            "protected": "Protected",
            "focus_mode": "Focus Mode",
            "activate_focus_mode": "Activate Focus Mode",
            "deactivate_focus_mode": "Deactivate Focus Mode",
            "set_your_intention": "Set your intention",
            "home": "⌂ Home",
            // ปุ่มควบคุม Phone Home
            "shuffle": "Shuffle",
            "light": "Light",
            "dark": "Dark",
            // หน้าขัดจังหวะ
            "you_opened": "You opened {app}.",
            "still_on_purpose": "Still on purpose?",
            "go_back": "Go Back",
            "continue_anyway": "Continue Anyway",
            "continue_anyway_countdown": "Continue Anyway ({seconds}s)",
            "time_spent_nudge": "You've spent {time} on {app} today.",
            // ตั้งเป้าหมาย
            "set_your_intention_title": "Set Your Intention",
            "protection_subtitle": "Choose which apps to protect, how firmly each should ask you to pause, and why you're using them.",
            "your_message": "Your message",
            "level_label": "Level {level}:",
            "back": "Back",
        ],
        "th": [
            // แดชบอร์ด
            "dashboard_title": "แดชบอร์ด",
            "screen_time_today": "เวลาหน้าจอวันนี้",
            "unlocks": "การปลดล็อก",
            "notifications": "การแจ้งเตือน",
            "protected": "ป้องกันอยู่",
            "focus_mode": "โหมดโฟกัส",
            "activate_focus_mode": "เปิดใช้งานโฟกัส",
            "deactivate_focus_mode": "ปิดโหมดโฟกัส",
            "set_your_intention": "ตั้งเป้าหมายของคุณ",
            "home": "⌂ หน้าหลัก",
            // ปุ่มควบคุม Phone Home
            "shuffle": "สุ่ม",
            "light": "สว่าง",
            "dark": "มืด",
            // หน้าขัดจังหวะ
            "you_opened": "คุณเปิด {app}",
            "still_on_purpose": "ยังตั้งใจอยู่ไหม?",
            "go_back": "ย้อนกลับ",
            "continue_anyway": "ดำเนินการต่อ",
            "continue_anyway_countdown": "ดำเนินการต่อ ({seconds} วิ)",
            "time_spent_nudge": "วันนี้คุณใช้เวลา {time} กับ {app}",
            // ตั้งเป้าหมาย
            "set_your_intention_title": "ตั้งเป้าหมายของคุณ",
            "protection_subtitle": "เลือกแอปที่ต้องการป้องกัน กำหนดความเข้มงวดในการหยุดพัก และเหตุผลที่คุณใช้งานแอปเหล่านี้",
            "your_message": "ข้อความของคุณ",
            "level_label": "ระดับ {level}:",
            "back": "ย้อนกลับ",
        ],
    ]

    static func t(_ key: String, lang: String = defaultLanguage) -> String {
        let langTable = table[lang] ?? table[defaultLanguage]!
        return langTable[key] ?? table[defaultLanguage]![key] ?? key
    }
}

extension String {
    func filling(_ replacements: [String: String]) -> String {
        var result = self
        for (key, value) in replacements {
            result = result.replacingOccurrences(of: "{\(key)}", with: value)
        }
        return result
    }
}
