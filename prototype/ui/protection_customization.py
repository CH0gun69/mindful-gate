from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QButtonGroup
)
from PySide6.QtCore import Qt, Signal

from core.mock_data import (
    glyph_for, icon_path_for, DEFAULT_APP_PROTECTION_LEVELS, PROTECTION_LEVELS,
)
from ui.widgets.svg_icon import white_svg_pixmap

ROW_AVATAR_SIZE = 40


class ProtectionCustomizationScreen(QWidget):
    """Replaces the old Insights screen. Lets the user pick a 1/2/3
    protection level per currently-protected app -- how much calm friction
    InterruptionScreen adds before "Continue Anyway" unlocks (see
    core.mock_data.PROTECTION_LEVELS). Instant-apply per tap, no separate
    Save button, matching the rest of the app's live-update pattern (Setup's
    checkboxes driving Dashboard/PhoneHome the same way)."""

    go_back = Signal()
    level_changed = Signal(str, int)  # app_name, new level

    def __init__(self):
        super().__init__()
        self._protected = []  # ordered list of currently-protected app names
        self._levels = dict(DEFAULT_APP_PROTECTION_LEVELS)  # app_name -> level
        self._button_groups = {}  # app_name -> QButtonGroup, kept alive here
        self._build_ui()
        self._refresh_rows()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(20)

        title = QLabel("Protection Customization")
        title.setObjectName("screenTitle")
        root.addWidget(title)

        subtitle = QLabel("Choose how firmly each app should ask you to pause.")
        subtitle.setObjectName("caption")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        self._rows_layout = QVBoxLayout()
        self._rows_layout.setSpacing(10)
        root.addLayout(self._rows_layout)

        root.addStretch()

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("primaryBtn")
        back_btn.clicked.connect(lambda: self.go_back.emit())
        root.addWidget(back_btn)

    def set_protected_apps(self, protected_apps):
        """Which apps to list -- same name/shape as DashboardScreen's
        method, called by MainWindow whenever Setup's app selection
        changes."""
        self._protected = list(protected_apps)
        self._refresh_rows()

    def set_levels(self, levels: dict):
        """Full app_name -> level dict, pushed down by MainWindow whenever
        it changes (including on startup). Apps not present fall back to
        DEFAULT_APP_PROTECTION_LEVELS via _level_for()."""
        self._levels = dict(levels)
        self._refresh_rows()

    def _level_for(self, app_name):
        return self._levels.get(app_name, DEFAULT_APP_PROTECTION_LEVELS.get(app_name, 1))

    def _refresh_rows(self):
        # Same detach-and-deleteLater rebuild pattern as
        # DashboardScreen._refresh_legend() -- setParent(None) detaches
        # (and hides) immediately, deleteLater() actually frees it on the
        # next event-loop pass.
        while self._rows_layout.count():
            item = self._rows_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self._button_groups.clear()

        for app in self._protected:
            self._rows_layout.addWidget(self._build_row(app))

    def _build_row(self, app_name):
        row = QFrame()
        row.setObjectName("appRow")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        avatar = QLabel()
        avatar.setFixedSize(ROW_AVATAR_SIZE, ROW_AVATAR_SIZE)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        glyph, color = glyph_for(app_name)
        avatar.setStyleSheet(
            f"background-color: {color}; border-radius: {ROW_AVATAR_SIZE // 4}px;"
        )
        icon_path = icon_path_for(app_name)
        if icon_path:
            avatar.setPixmap(white_svg_pixmap(icon_path, int(ROW_AVATAR_SIZE * 0.6)))
        else:
            avatar.setText(glyph)
            avatar.setStyleSheet(
                avatar.styleSheet() + " color: #ffffff; font-size: 18px; font-weight: 600;"
            )
        layout.addWidget(avatar)

        name_lbl = QLabel(app_name)
        name_lbl.setObjectName("appName")
        layout.addWidget(name_lbl)
        layout.addStretch()

        current_level = self._level_for(app_name)
        group = QButtonGroup(row)
        group.setExclusive(True)
        pills_row = QHBoxLayout()
        pills_row.setSpacing(4)
        for level in sorted(PROTECTION_LEVELS):
            btn = QPushButton(str(level))
            btn.setObjectName("levelPill")
            btn.setCheckable(True)
            btn.setChecked(level == current_level)
            btn.setFixedSize(30, 30)
            group.addButton(btn, level)
            pills_row.addWidget(btn)
        # idClicked only fires on user interaction, not on setChecked()
        # during a rebuild -- so pushing set_levels()/set_protected_apps()
        # down never spuriously re-emits level_changed.
        group.idClicked.connect(
            lambda level, app=app_name: self._on_level_clicked(app, level)
        )
        self._button_groups[app_name] = group
        layout.addLayout(pills_row)

        return row

    def _on_level_clicked(self, app_name, level):
        self._levels[app_name] = level
        self.level_changed.emit(app_name, level)
