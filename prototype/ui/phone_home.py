from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Signal

from core.mock_data import TOP_APPS, PROTECTABLE_APPS, glyph_for
from ui.widgets.app_icon import AppIcon
from ui.widgets.screen_time_widget import ScreenTimeWidget

# Always-available dock icons. Decorative only — tapping them is a no-op.
DOCK_APPS = [
    ("📞", "Phone"),
    ("📷", "Camera"),
    ("⚙", "Settings"),
    ("💬", "Messages"),
]

GRID_COLUMNS = 4


def _build_app_list():
    """Merge TOP_APPS + PROTECTABLE_APPS into one (name, protected) list,
    without hardcoding a separate app roster."""
    apps = {app["name"]: app["protected"] for app in TOP_APPS}
    for name in PROTECTABLE_APPS:
        apps.setdefault(name, True)
    return list(apps.items())


class PhoneHomeScreen(QWidget):
    """Mock phone lock/home screen — the entry point of the demo.
    Tapping any app icon fires app_tapped(name, protected) — the caller
    decides whether that means "show the interruption" (protected) or
    "just open the fake app window" (not protected). Dock icons stay inert."""

    app_tapped = Signal(str, bool)
    open_dashboard = Signal()

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
        root.addWidget(self._build_screen_time_widget())
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
            glyph, color = glyph_for(name)
            icon = AppIcon(name, glyph, color)
            icon.clicked.connect(
                lambda checked=False, n=name, p=protected: self.app_tapped.emit(n, p)
            )
            row, col = divmod(index, GRID_COLUMNS)
            grid.addWidget(icon, row, col)

        return wrap

    def _build_screen_time_widget(self):
        wrap = QWidget()
        wrap.setObjectName("phoneHomeScreenTimeWrap")
        layout = QVBoxLayout(wrap)
        # Same 20px horizontal inset as the app grid above it, so it lines
        # up instead of feeling bolted on.
        layout.setContentsMargins(20, 8, 20, 8)

        widget = ScreenTimeWidget()
        widget.clicked.connect(lambda: self.open_dashboard.emit())
        layout.addWidget(widget)

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
