import Foundation

/// i18n strings for mindful-gate's OWN UI chrome -- Phone Home, Dashboard,
/// Interruption, and Set Your Intention.
///
/// Fake App is deliberately excluded: its feed captions/usernames/chat
/// messages/shorts captions are mocked-up REAL-APP content (meant to read as
/// "a real app"), not mindful-gate's own UI copy, so it stays English-only by
/// design. Real app brand names (Instagram, TikTok, etc.) are never
/// translated anywhere, on any screen -- they're proper nouns, not UI copy.
/// The user-typed intention/message text itself is also never translated.
///
/// Templated keys (e.g. "{app}", "{time}", "{seconds}", "{level}") are filled
/// in by the caller via string interpolation/replacingOccurrences -- t()
/// itself just does the key/language lookup. Ported 1:1 from
/// prototype/core/strings.py; note there is no fmt() helper in that source.
enum Strings {
    static let defaultLanguage = "en"

    static let table: [String: [String: String]] = [
        "en": [
            // Dashboard
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
            // Phone Home referee controls
            "shuffle": "Shuffle",
            "light": "Light",
            "dark": "Dark",
            // Interruption
            "you_opened": "You opened {app}.",
            "still_on_purpose": "Still on purpose?",
            "go_back": "Go Back",
            "continue_anyway": "Continue Anyway",
            "continue_anyway_countdown": "Continue Anyway ({seconds}s)",
            "time_spent_nudge": "You've spent {time} on {app} today.",
            // Set Your Intention
            "set_your_intention_title": "Set Your Intention",
            "protection_subtitle": "Choose which apps to protect, how firmly each should ask you to pause, and why you're using them.",
            "your_message": "Your message",
            "level_label": "Level {level}:",
            "back": "Back",
        ],
        "th": [
            // Dashboard
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
            // Phone Home referee controls
            "shuffle": "สุ่ม",
            "light": "สว่าง",
            "dark": "มืด",
            // Interruption
            "you_opened": "คุณเปิด {app}",
            "still_on_purpose": "ยังตั้งใจอยู่ไหม?",
            "go_back": "ย้อนกลับ",
            "continue_anyway": "ดำเนินการต่อ",
            "continue_anyway_countdown": "ดำเนินการต่อ ({seconds} วิ)",
            "time_spent_nudge": "วันนี้คุณใช้เวลา {time} กับ {app}",
            // Set Your Intention
            "set_your_intention_title": "ตั้งเป้าหมายของคุณ",
            "protection_subtitle": "เลือกแอปที่ต้องการป้องกัน กำหนดความเข้มงวดในการหยุดพัก และเหตุผลที่คุณใช้งานแอปเหล่านี้",
            "your_message": "ข้อความของคุณ",
            "level_label": "ระดับ {level}:",
            "back": "ย้อนกลับ",
        ],
    ]

    /// Looks up `key` in `lang`'s strings, falling back to English for a
    /// missing key/language rather than crashing or showing a raw key.
    static func t(_ key: String, lang: String = defaultLanguage) -> String {
        let langTable = table[lang] ?? table[defaultLanguage]!
        return langTable[key] ?? table[defaultLanguage]![key] ?? key
    }
}
