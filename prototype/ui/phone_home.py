from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Signal

from core.mock_data import TOP_APPS, PROTECTABLE_APPS
from ui.widgets.app_icon import AppIcon

# Decorative glyph + accent color per app, keyed off the names that already
# exist in core/mock_data.py. Apps not listed here fall back to an initial
# letter avatar, so nothing here needs to stay in sync with the mock data.
APP_GLYPHS = {
    "Instagram": ("📸", "#e1306c"),
    "TikTok": ("🎵", "#111214"),
    "X (Twitter)": ("𝕏", "#1d2026"),
    "YouTube": ("▶", "#ff0000"),
    "Messages": ("💬", "#34c759"),
    "Facebook": ("📘", "#1877f2"),
    "Reddit": ("👽", "#ff4500"),
}

# Always-available dock icons. Decorative only — tapping them is a no-op.
DOCK_APPS = [
    ("📞", "Phone"),
    ("📷", "Camera"),
    ("⚙", "Settings"),
    ("💬", "Messages"),
]

GRID_COLUMNS = 4


def _glyph_for(name):
    return APP_GLYPHS.get(name, (name[0].upper(), "#3a3f47"))


def _build_app_list():
    """Merge TOP_APPS + PROTECTABLE_APPS into one (name, protected) list,
    without hardcoding a separate app roster."""
    apps = {app["name"]: app["protected"] for app in TOP_APPS}
    for name in PROTECTABLE_APPS:
        apps.setdefault(name, True)
    return list(apps.items())


class PhoneHomeScreen(QWidget):
    """Mock phone lock/home screen — the entry point of the demo.
    Tapping a protected app icon fires app_opened(name); everything else
    (non-protected apps, dock icons) is inert."""

    app_opened = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("phoneHomeScreen")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 20)
        root.setSpacing(0)

        root.addWidget(self._build_status_bar())
        root.addWidget(self._build_app_grid())
        root.addStretch()
        root.addWidget(self._build_dock())

    def _build_status_bar(self):
        bar = QFrame()
        bar.setObjectName("phoneStatusBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 12, 20, 12)

        time_label = QLabel("9:41")
        time_label.setObjectName("statusBarTime")
        layout.addWidget(time_label)

        layout.addStretch()

        icons_label = QLabel("•••  5G  🔋")
        icons_label.setObjectName("statusBarIcons")
        layout.addWidget(icons_label)

        return bar

    def _build_app_grid(self):
        wrap = QWidget()
        wrap.setObjectName("phoneHomeGrid")
        grid = QGridLayout(wrap)
        grid.setContentsMargins(20, 32, 20, 16)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(24)

        for index, (name, protected) in enumerate(_build_app_list()):
            glyph, color = _glyph_for(name)
            icon = AppIcon(name, glyph, color)
            icon.clicked.connect(
                lambda checked=False, n=name, p=protected: self._on_app_tapped(n, p)
            )
            row, col = divmod(index, GRID_COLUMNS)
            grid.addWidget(icon, row, col)

        return wrap

    def _build_dock(self):
        dock = QFrame()
        dock.setObjectName("phoneDock")
        layout = QHBoxLayout(dock)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        for glyph, name in DOCK_APPS:
            icon = AppIcon(name, glyph, "#3a3f47", avatar_size=44)
            icon.setObjectName("dockIcon")
            # Intentionally left unconnected: dock icons are decorative only.
            layout.addWidget(icon)

        return dock

    def _on_app_tapped(self, name, protected):
        if protected:
            self.app_opened.emit(name)
        # Non-protected apps: no interruption. The button's own :pressed
        # style (see styles.qss) is the only feedback needed for the mock.
