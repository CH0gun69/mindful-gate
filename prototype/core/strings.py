"""
Minimal i18n strings for the Phone Home and Dashboard screens ONLY.

Deliberately scoped -- Interruption, Set Your Intention, and Fake App
remain English-only for now (see CLAUDE.md for why). Real app brand names
(Instagram, TikTok, etc.) are never translated anywhere, on either screen
-- they're proper nouns, not UI copy.
"""

STRINGS = {
    "en": {
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
        "shuffle": "Shuffle",
        "light": "Light",
        "dark": "Dark",
    },
    "th": {
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
        "shuffle": "สุ่ม",
        "light": "สว่าง",
        "dark": "มืด",
    },
}

DEFAULT_LANGUAGE = "en"


def t(key, lang=DEFAULT_LANGUAGE):
    """Look up `key` in `lang`'s strings, falling back to English for a
    missing key/language rather than crashing or showing a raw key --
    mirrors icon_path_for()/time_spent_today_for()'s missing-data-safe
    pattern elsewhere in core/."""
    table = STRINGS.get(lang, STRINGS[DEFAULT_LANGUAGE])
    return table.get(key, STRINGS[DEFAULT_LANGUAGE].get(key, key))
