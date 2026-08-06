"""
Hardcoded mock data for the mindful-gate prototype.
No real usage tracking — this is purely for demo purposes.
"""

SCREEN_TIME_TODAY = "4h 32m"
UNLOCKS_TODAY = 87
NOTIFICATIONS_TODAY = 143

TOP_APPS = [
    {"name": "Instagram", "time": "1h 48m", "protected": True},
    {"name": "YouTube", "time": "1h 05m", "protected": False},
    {"name": "TikTok", "time": "52m", "protected": True},
    {"name": "Messages", "time": "31m", "protected": False},
    {"name": "X (Twitter)", "time": "16m", "protected": True},
]

PROTECTABLE_APPS = ["Instagram", "TikTok", "X (Twitter)", "YouTube", "Facebook", "Reddit"]

# Which of PROTECTABLE_APPS start out checked/protected before the user has
# ever visited Setup — single source of truth shared by IntentionSetupScreen
# (checkbox defaults) and PhoneHomeScreen (initial interrupt behavior), so
# they can't drift out of sync with each other.
DEFAULT_PROTECTED_APPS = ["Instagram", "TikTok", "X (Twitter)"]

INSIGHTS = {
    "intentions_kept": 12,
    "intentions_total": 18,
    "time_saved_this_week": "3h 20m",
    "most_interrupted_app": "Instagram",
}

DEFAULT_INTENTION = "Only reply to messages"

# Decorative glyph + accent color per app, keyed off the names already used
# in TOP_APPS / PROTECTABLE_APPS above. Purely presentational — shared by the
# phone home screen and the fake app screen so apps not listed here just fall
# back to an initial-letter avatar instead of needing to stay in sync.
APP_GLYPHS = {
    "Instagram": ("📸", "#e1306c"),
    "TikTok": ("🎵", "#111214"),
    "X (Twitter)": ("𝕏", "#1d2026"),
    "YouTube": ("▶", "#ff0000"),
    "Messages": ("💬", "#34c759"),
    "Facebook": ("📘", "#1877f2"),
    "Reddit": ("👽", "#ff4500"),
}


def glyph_for(name):
    return APP_GLYPHS.get(name, (name[0].upper(), "#3a3f47"))


def _parse_minutes(time_str):
    """Parse a mock 'Xh Ym' / 'Ym' time string (as used in TOP_APPS) into
    total minutes."""
    hours = 0
    minutes = 0
    for part in time_str.split():
        if part.endswith("h"):
            hours = int(part[:-1])
        elif part.endswith("m"):
            minutes = int(part[:-1])
    return hours * 60 + minutes


def usage_breakdown():
    """(name, minutes, time_str, color) tuples derived from TOP_APPS, for
    Dashboard's screen-time ring chart + legend -- deliberately not a
    separate hardcoded dataset, so it can't drift out of sync with TOP_APPS
    (their minutes already sum to exactly SCREEN_TIME_TODAY)."""
    return [
        (app["name"], _parse_minutes(app["time"]), app["time"], glyph_for(app["name"])[1])
        for app in TOP_APPS
    ]