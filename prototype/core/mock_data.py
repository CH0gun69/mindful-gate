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

INSIGHTS = {
    "intentions_kept": 12,
    "intentions_total": 18,
    "time_saved_this_week": "3h 20m",
    "most_interrupted_app": "Instagram",
}

DEFAULT_INTENTION = "Only reply to messages"