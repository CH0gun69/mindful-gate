"""
Hardcoded mock data for the mindful-gate prototype.
No real usage tracking — this is purely for demo purposes.
"""

import os
import random

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

# Per-app protection level (1/2/3) before the user has ever visited the
# Protection Customization screen -- level 1 (mildest) for every
# protectable app, single source of truth shared by MainWindow's
# app_protection_levels dict and ProtectionCustomizationScreen's initial
# row state, so a never-configured app can't render with an undefined level.
DEFAULT_APP_PROTECTION_LEVELS = {app: 1 for app in PROTECTABLE_APPS}

# Behavior per interruption level, keyed by level number (1/2/3). Single
# source of truth for InterruptionScreen's timing/UI-gating logic --
# "delay" is seconds Continue Anyway stays disabled before it can unlock,
# "breathing" toggles the animated breathe-in/breathe-out text under the
# icon, "reaffirm" means the delay elapsing does NOT auto-unlock Continue
# Anyway -- the user must additionally tap the "Still on purpose?" chip.
# Modeled after the real "one sec" app's breathing + deliberation-message
# pattern -- calm, escalating friction, never a hard block.
PROTECTION_LEVELS = {
    1: {"delay": 3, "breathing": False, "reaffirm": False},
    2: {"delay": 7, "breathing": True, "reaffirm": False},
    3: {"delay": 12, "breathing": True, "reaffirm": True},
}

# Full breathe-in+breathe-out cycle duration (ms) for the pulsing circle
# shown during levels 2/3 (see ui.widgets.breathing_circle.BreathingCircle).
BREATHING_CYCLE_MS = 2500

DEFAULT_INTENTION = "Only reply to messages"

# Decorative glyph + accent color per app, keyed off the names already used
# in TOP_APPS / PROTECTABLE_APPS above. Purely presentational — shared by the
# phone home screen and the fake app screen so apps not listed here just fall
# back to an initial-letter avatar instead of needing to stay in sync.
APP_GLYPHS = {
    "Instagram": ("📸", "#c44d75"),
    "TikTok": ("🎵", "#111214"),
    "X (Twitter)": ("𝕏", "#1f2024"),
    "YouTube": ("▶", "#d62929"),
    "Messages": ("💬", "#4caf65"),
    "Facebook": ("📘", "#3b7ccf"),
    "Reddit": ("👽", "#d65829"),
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


def _format_minutes(total_minutes):
    """Inverse of _parse_minutes -- total minutes back into the same
    'Xh Ym' / 'Ym' mock format TOP_APPS already uses."""
    hours, minutes = divmod(total_minutes, 60)
    if hours and minutes:
        return f"{hours}h {minutes:02d}m"
    if hours:
        return f"{hours}h"
    return f"{minutes}m"


# Live, in-memory-only "time spent today" overrides, keyed by app name --
# populated by shuffle_top_apps(), cleared by reset_top_apps_shuffle().
# TOP_APPS itself (the constant above) is NEVER mutated, so a fresh
# process (or an explicit reset) always goes back to the real hardcoded
# values -- this is purely a cosmetic, session-only demo control so a
# referee can see the ring chart/dashboard update live instead of always
# showing identical static numbers.
_shuffled_times = None
SHUFFLE_RANGE_MINUTES = (5, 180)  # 5min-3h per app, per the feature ask


def shuffle_top_apps():
    """Randomize every TOP_APPS app's mock 'time spent today' in memory
    only. Never touches TOP_APPS -- callers just need to re-render
    whatever they already built from usage_breakdown()/
    time_spent_today_for()/current_screen_time_today() afterward."""
    global _shuffled_times
    _shuffled_times = {
        app["name"]: _format_minutes(random.randint(*SHUFFLE_RANGE_MINUTES))
        for app in TOP_APPS
    }


def reset_top_apps_shuffle():
    """Back to the real TOP_APPS values -- not currently wired to any UI
    control, but kept as the explicit inverse of shuffle_top_apps() rather
    than only being resettable by restarting the process."""
    global _shuffled_times
    _shuffled_times = None


def _time_for(app):
    """This TOP_APPS entry's current time string -- the live shuffled
    override if a shuffle is active, else its real value."""
    if _shuffled_times is not None:
        return _shuffled_times.get(app["name"], app["time"])
    return app["time"]


def time_spent_today_for(name):
    """This app's current "Xh Ym" time (shuffled if a shuffle is active,
    otherwise its real TOP_APPS entry), or None if it has no mock usage
    entry at all -- e.g. a protectable app the user checked that isn't in
    the mock usage data. Callers (InterruptionScreen, FakeAppScreen)
    should omit their "time spent today" nudge gracefully in that case
    rather than show "0m" or crash."""
    for app in TOP_APPS:
        if app["name"] == name:
            return _time_for(app)
    return None


def usage_breakdown():
    """(name, minutes, time_str, color) tuples derived from TOP_APPS, for
    Dashboard's screen-time ring chart + legend -- deliberately not a
    separate hardcoded dataset, so it can't drift out of sync with TOP_APPS
    (their minutes sum to exactly SCREEN_TIME_TODAY normally, or to
    current_screen_time_today() when a shuffle is active)."""
    return [
        (app["name"], _parse_minutes(_time_for(app)), _time_for(app), glyph_for(app["name"])[1])
        for app in TOP_APPS
    ]


def current_screen_time_today():
    """The big screen-time total shown on Phone Home/Dashboard --
    SCREEN_TIME_TODAY normally (which already equals this sum by
    construction), or the live sum of shuffled per-app times when a
    shuffle is active, so the displayed total never contradicts what's
    shuffled underneath it."""
    if _shuffled_times is None:
        return SCREEN_TIME_TODAY
    total = sum(_parse_minutes(_time_for(app)) for app in TOP_APPS)
    return _format_minutes(total)


# Ambient 2-state color tinting for Dashboard's screen-time display -- no
# numeric score, no "Attention"/"Warning" label anywhere, just a color
# shift on elements that already exist (the big time value + the ring's
# overall tone). 240 min (4h) chosen because SCREEN_TIME_TODAY (4h 32m)
# already crosses it, so both states are demo-visible without faking data.
AMBIENT_THRESHOLD_MINUTES = 240
AMBIENT_COLOR_NORMAL = "#93cfc4"  # softened teal accent, unchanged look below the threshold
AMBIENT_COLOR_HIGH = "#d9a974"  # soft amber, not red -- ambient, not alarming


def is_high_usage():
    """Whether the current screen time total (shuffled if active, else
    SCREEN_TIME_TODAY) is at/above AMBIENT_THRESHOLD_MINUTES -- reads
    current_screen_time_today() rather than the raw constant so the
    ambient tint stays consistent with whatever total is actually
    displayed after a shuffle."""
    return _parse_minutes(current_screen_time_today()) >= AMBIENT_THRESHOLD_MINUTES


def usage_color(is_high: bool) -> str:
    """AMBIENT_COLOR_HIGH or AMBIENT_COLOR_NORMAL depending on state --
    kept as a plain boolean-in function (rather than baking is_high_usage()
    into it) so callers/tests can drive either state directly without
    needing to fake SCREEN_TIME_TODAY."""
    return AMBIENT_COLOR_HIGH if is_high else AMBIENT_COLOR_NORMAL


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

# Per-app action-button config for the "feed" style, so each app is
# recognizable by its button personality, not just its accent color.
# "layout" picks which shared renderer (see FakeAppScreen) builds it:
#   "icons"   -- evenly-spaced icon-only buttons in a row (Instagram, X)
#   "labeled" -- full-width icon+text buttons separated by dividers (Facebook)
#   "vote"    -- a vertical up/count/down cluster + separate comment count,
#                positioned on the post's left side instead of a bottom row
#                (Reddit) -- genuinely different real-world layout, not just
#                different icons, so it's flagged here rather than forced
#                into the same row shape as the other three.
# Each button's "flash" color is what it briefly highlights as on click
# (cosmetic press feedback only -- see FakeAppScreen._flash_action_button),
# picked to match that action's real-world platform color.
FEED_ACTIONS = {
    "Instagram": {
        "layout": "icons",
        "buttons": [
            {"id": "like", "icon": "♡", "flash": "#ff3b5c"},
            {"id": "comment", "icon": "💬", "flash": "#8fd3c7"},
            {"id": "share", "icon": "➤", "flash": "#8fd3c7"},
            {"id": "save", "icon": "🔖", "flash": "#8fd3c7"},
        ],
    },
    "Facebook": {
        "layout": "labeled",
        "buttons": [
            {"id": "like", "icon": "👍", "label": "Like", "flash": "#1877f2"},
            {"id": "comment", "icon": "💬", "label": "Comment", "flash": "#1877f2"},
            {"id": "share", "icon": "↗", "label": "Share", "flash": "#1877f2"},
        ],
    },
    "X (Twitter)": {
        "layout": "icons",
        "size": "small",
        "buttons": [
            {"id": "reply", "icon": "💬", "flash": "#1d9bf0"},
            {"id": "retweet", "icon": "↻", "flash": "#00ba7c"},
            {"id": "like", "icon": "♡", "flash": "#f91880"},
            {"id": "share", "icon": "↗", "flash": "#1d9bf0"},
        ],
    },
    "Reddit": {
        "layout": "vote",
        "vote_count": "1.2K",
        "comment_count": "84 comments",
        "upvote_flash": "#ff4500",
        "downvote_flash": "#7193ff",
    },
}


def feed_actions_for(name):
    """Per-app action-button config for the feed style. Falls back to
    Instagram's icon row for any app that isn't explicitly configured, so
    style_for()'s generic "feed" fallback for unlisted apps never crashes
    here even though it isn't reachable with the current app roster."""
    return FEED_ACTIONS.get(name, FEED_ACTIONS["Instagram"])

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