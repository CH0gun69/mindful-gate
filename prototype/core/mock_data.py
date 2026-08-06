"""
Hardcoded mock data for the mindful-gate prototype.
No real usage tracking — this is purely for demo purposes.
"""

import os

ASSETS_ICONS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icons"
)
ASSETS_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images"
)

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


# Real brand-logo SVGs (Simple Icons, MIT-licensed, simpleicons.org) for apps
# that have one, keyed off the same names as APP_GLYPHS. "Messages" is a
# fictional stand-in app with no real-world brand to match, so it's
# intentionally absent here and keeps falling back to its emoji avatar via
# glyph_for() -- see icon_path_for()'s docstring.
APP_ICON_FILES = {
    "Instagram": "instagram.svg",
    "TikTok": "tiktok.svg",
    "X (Twitter)": "x.svg",
    "YouTube": "youtube.svg",
    "Facebook": "facebook.svg",
    "Reddit": "reddit.svg",
}


def icon_path_for(name):
    """Absolute path to name's real brand-logo SVG, or None if it doesn't
    have one -- callers (AppIcon) fall back to glyph_for()'s emoji/letter
    avatar in that case. Also None if the file is unexpectedly missing on
    disk, so a bad asset degrades to the existing fallback instead of
    crashing."""
    filename = APP_ICON_FILES.get(name)
    if not filename:
        return None
    path = os.path.join(ASSETS_ICONS_DIR, filename)
    return path if os.path.isfile(path) else None


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


# ===== Fake App mock content =====
# Local CC0 placeholder photos (Picsum Photos, picsum.photos -- static files
# downloaded once, not fetched at runtime, so this works fully offline). No
# identifiable people in any of them. See assets/images/README.md.
MOCK_IMAGES = [
    "lake_forest.jpg", "waterfall.jpg", "flower_field.jpg", "cat_closeup.jpg",
    "yellow_flower.jpg", "foggy_road.jpg", "hay_bales.jpg", "foggy_trees.jpg",
    "sunset_field.jpg", "bare_tree.jpg",
]


def mock_image_path(index):
    """Absolute path to one of the local mock images, cycling through
    MOCK_IMAGES by index. None if the file is unexpectedly missing (same
    missing-file-safe pattern as icon_path_for)."""
    name = MOCK_IMAGES[index % len(MOCK_IMAGES)]
    path = os.path.join(ASSETS_IMAGES_DIR, name)
    return path if os.path.isfile(path) else None


def mock_image_index_for(name, offset=0):
    """Deterministic (not Python's randomized hash()) pseudo-random index
    into MOCK_IMAGES, seeded by an app/screen name -- so the same app always
    shows the same picture across a run (and between test runs), while
    different apps/posts still get visual variety. offset lets one screen
    request several different images (e.g. 3 feed posts) off the same name.
    Position-weighted (not a plain character sum) so similarly-lettered
    names like "Instagram"/"Facebook"/"Reddit" don't collide on the same
    bucket as often as a plain sum would."""
    weighted = sum((i + 1) * ord(c) for i, c in enumerate(name))
    return (weighted + offset) % len(MOCK_IMAGES)


# (username, caption) pairs shared by every "feed"-style app (Instagram,
# Facebook, X (Twitter), Reddit) -- same card pattern for all four, just
# re-skinned with that app's own accent color/name, per the brief.
MOCK_FEED_POSTS = [
    ("wanderlust.jane", "chasing golden hour again 🌅"),
    ("dev.marcus", "small wins today, one commit at a time"),
    ("plant.mama", "she's finally blooming 🌸"),
]

# Caption shown on the "shorts"-style screens (TikTok, YouTube).
MOCK_SHORTS_CAPTION = "wait for it... 😅"

# Fictional contacts for the "messages" style -- invented generic names, not
# real people. The first contact is who MOCK_CHAT is "with"; "Alex" in that
# chat is the app's own (also fictional) user, not a contact, so it's
# deliberately not reused as a contact name here.
MOCK_CONTACTS = [
    ("Jamie Chen", "Good to hear 🙂"),
    ("Jordan Lee", "See you at 6?"),
    ("Sam Park", "Sent the files 📎"),
    ("Taylor Kim", "Haha exactly 😂"),
]

# (sender, text) pairs for the messages style's chat view -- with Jamie Chen
# (MOCK_CONTACTS[0]). sender is "me" (the app's user, Alex) or "them" (Jamie).
MOCK_CHAT = [
    ("them", "Hey Alex! How's it going?"),
    ("me", "It's going well, thanks!"),
    ("them", "Good to hear 🙂"),
]

# Which visual style each real app uses on the Fake App screen. Data-driven
# on purpose -- one small dict instead of repeated if/elif app-name checks.
APP_STYLE = {
    "Instagram": "feed",
    "Facebook": "feed",
    "X (Twitter)": "feed",
    "Reddit": "feed",
    "TikTok": "shorts",
    "YouTube": "shorts",
    "Messages": "messages",
}


def style_for(name):
    """Which Fake App layout to use for an app name. Defaults to "feed" for
    anything unlisted, since that's the most generic/reusable of the three."""
    return APP_STYLE.get(name, "feed")