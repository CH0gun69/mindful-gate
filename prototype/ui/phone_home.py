from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt, Signal

from core.mock_data import (
    TOP_APPS, PROTECTABLE_APPS, DEFAULT_PROTECTED_APPS, glyph_for, icon_path_for,
)
from core.strings import t, DEFAULT_LANGUAGE
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


def _build_app_roster():
    """Merge TOP_APPS + PROTECTABLE_APPS into one ordered name list, without
    hardcoding a separate app roster. Protected/not-protected is decided
    separately (see PhoneHomeScreen._protected) so it can change at runtime
    based on what's actually selected in Setup."""
    names = [app["name"] for app in TOP_APPS]
    for name in PROTECTABLE_APPS:
        if name not in names:
            names.append(name)
    return names


class PhoneHomeScreen(QWidget):
    """Mock phone lock/home screen — the entry point of the demo.
    Tapping any app icon fires app_tapped(name, protected) — the caller
    decides whether that means "show the interruption" (protected) or
    "just open the fake app window" (not protected). Dock icons stay inert.

    Which apps count as "protected" is runtime state (see set_protected_apps),
    driven by whatever was last checked on the Setup screen — it defaults to
    DEFAULT_PROTECTED_APPS before Setup has ever been visited."""

    app_tapped = Signal(str, bool)
    open_dashboard = Signal()
    # Referee/demo utility controls -- deliberately plain no-arg signals,
    # same as DashboardScreen.focus_toggled: MainWindow owns the actual
    # shuffle/theme/language state and tells this screen (and others) what
    # to display afterward, this screen just reports "the button was
    # tapped".
    shuffle_clicked = Signal()
    theme_toggle_clicked = Signal()
    language_toggle_clicked = Signal()

    def __init__(self, protected_apps=None):
        super().__init__()
        self.setObjectName("phoneHomeScreen")
        self._protected = set(
            DEFAULT_PROTECTED_APPS if protected_apps is None else protected_apps
        )
        self._build_ui()

    def set_protected_apps(self, protected_apps):
        """Update which apps trigger the interruption screen when tapped,
        e.g. after the user activates a new selection on the Setup screen."""
        self._protected = set(protected_apps)

    def refresh_screen_time(self):
        """Re-read the (possibly shuffled) total -- called by MainWindow
        after Shuffle."""
        self.screen_time_widget.refresh_screen_time()

    def set_theme_button_state(self, dark: bool):
        # Icon/label always shows what tapping it would switch TO (matches
        # a typical OS dark/light toggle affordance), same pattern as the
        # language button below. English-only regardless of the TH/EN
        # toggle -- these three are meta/demo controls, not simulated
        # phone UI, so they're deliberately exempt from translation.
        self.theme_btn.setText("☀️ Light" if dark else "🌙 Dark")

    def set_language_button_state(self, lang):
        self.lang_btn.setText("TH" if lang == "en" else "EN")

    def set_language(self, lang):
        """Retranslate this screen's own UI copy -- app names and dock
        labels stay untranslated (real/app-like brand names, not UI
        copy), only the screen-time widget's captions change."""
        self.screen_time_widget.set_language(lang)
        self.shuffle_btn.setText(f"🔀 {t('shuffle', lang)}")

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 20)
        root.setSpacing(0)

        root.addWidget(self._build_status_bar())
        root.addWidget(self._build_app_grid())
        root.addWidget(self._build_screen_time_widget())
        root.addWidget(self._build_controls_row())
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

        for index, name in enumerate(_build_app_roster()):
            glyph, color = glyph_for(name)
            icon = AppIcon(name, glyph, color, icon_path=icon_path_for(name))
            icon.clicked.connect(
                lambda checked=False, n=name: self.app_tapped.emit(n, n in self._protected)
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

        self.screen_time_widget = ScreenTimeWidget()
        self.screen_time_widget.clicked.connect(lambda: self.open_dashboard.emit())
        layout.addWidget(self.screen_time_widget)

        return wrap

    def _build_controls_row(self):
        """Three compact referee/demo utility controls directly below the
        screen-time widget, styled like small versions of the same card
        (see QPushButton#miniControlBtn in styles.qss) -- Shuffle (randomize
        mock usage data live), Light/Dark (swap the whole app's stylesheet),
        TH/EN (retranslate Phone Home + Dashboard). All three just emit a
        signal; MainWindow owns the actual state and tells every affected
        screen what to show afterward, same split as everything else in
        this app."""
        wrap = QWidget()
        wrap.setObjectName("phoneHomeScreenTimeWrap")  # same transparent bg + inset as above
        layout = QHBoxLayout(wrap)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(8)

        self.shuffle_btn = QPushButton(f"🔀 {t('shuffle', DEFAULT_LANGUAGE)}")
        self.shuffle_btn.setObjectName("miniControlBtn")
        self.shuffle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.shuffle_btn.clicked.connect(lambda: self.shuffle_clicked.emit())
        layout.addWidget(self.shuffle_btn)

        self.theme_btn = QPushButton("☀️ Light")  # dark is the default starting theme
        self.theme_btn.setObjectName("miniControlBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(lambda: self.theme_toggle_clicked.emit())
        layout.addWidget(self.theme_btn)

        self.lang_btn = QPushButton("TH")  # en is the default starting language
        self.lang_btn.setObjectName("miniControlBtn")
        self.lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lang_btn.clicked.connect(lambda: self.language_toggle_clicked.emit())
        layout.addWidget(self.lang_btn)

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
