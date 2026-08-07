from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QButtonGroup, QCheckBox, QLineEdit,
)
from PySide6.QtCore import Qt, Signal

from core.mock_data import (
    glyph_for, icon_path_for, PROTECTABLE_APPS, DEFAULT_PROTECTED_APPS,
    DEFAULT_APP_PROTECTION_LEVELS, PROTECTION_LEVELS, DEFAULT_INTENTION,
)
from ui.widgets.svg_icon import white_svg_pixmap

ROW_AVATAR_SIZE = 40


class ProtectionCustomizationScreen(QWidget):
    """Single combined destination for setting up protection -- merges what
    used to be two separate screens (Setup + Protection Customization) into
    one: pick which apps to protect, write an intention, set each app's
    friction level (1/2/3, see core.mock_data.PROTECTION_LEVELS), and flip
    protection on/off overall. One row per app: checkbox + icon/name + the
    3-level pill picker (pills only meaningful/enabled once that app is
    checked). Intention text and the ON/OFF toggle live once, not per row.

    The row list itself never changes (always all of PROTECTABLE_APPS), so
    unlike the old screens this doesn't need a rebuild-on-update pattern --
    rows are built once in _build_ui() and just get enabled/disabled or
    re-checked in place."""

    protection_toggled = Signal(bool, str, list)  # enabled, intention, protected apps
    level_changed = Signal(str, int)  # app_name, new level
    go_back = Signal()

    def __init__(self):
        super().__init__()
        self.checkboxes = {}  # app_name -> QCheckBox
        self._levels = dict(DEFAULT_APP_PROTECTION_LEVELS)  # app_name -> level
        self._pill_buttons = {}  # app_name -> list[QPushButton], for enable/disable
        self._button_groups = {}  # app_name -> QButtonGroup, kept alive here
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(16)

        title = QLabel("Set Your Intention")
        title.setObjectName("screenTitle")
        root.addWidget(title)

        subtitle = QLabel(
            "Choose which apps to protect, how firmly each should ask you "
            "to pause, and why you're using them."
        )
        subtitle.setObjectName("caption")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        rows_layout = QVBoxLayout()
        rows_layout.setSpacing(10)
        for app in PROTECTABLE_APPS:
            rows_layout.addWidget(self._build_row(app))
        root.addLayout(rows_layout)

        intent_label = QLabel("Your intention")
        intent_label.setObjectName("sectionLabel")
        root.addWidget(intent_label)

        self.intention_input = QLineEdit(DEFAULT_INTENTION)
        self.intention_input.setObjectName("intentionInput")
        root.addWidget(self.intention_input)

        root.addStretch()

        self.toggle_btn = QPushButton("Activate Protection")
        self.toggle_btn.setObjectName("secondaryBtn")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self._on_toggle_clicked)
        root.addWidget(self.toggle_btn)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("linkBtn")
        back_btn.clicked.connect(lambda: self.go_back.emit())
        root.addWidget(back_btn)

    def _build_row(self, app_name):
        row = QFrame()
        row.setObjectName("appRow")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        checked = app_name in DEFAULT_PROTECTED_APPS
        cb = QCheckBox()
        cb.setChecked(checked)
        self.checkboxes[app_name] = cb
        layout.addWidget(cb)

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

        current_level = self._levels.get(app_name, 1)
        group = QButtonGroup(row)
        group.setExclusive(True)
        pills_row = QHBoxLayout()
        pills_row.setSpacing(4)
        pill_buttons = []
        for level in sorted(PROTECTION_LEVELS):
            btn = QPushButton(str(level))
            btn.setObjectName("levelPill")
            btn.setCheckable(True)
            btn.setChecked(level == current_level)
            btn.setFixedSize(30, 30)
            btn.setEnabled(checked)  # only meaningful once the app is protected
            group.addButton(btn, level)
            pills_row.addWidget(btn)
            pill_buttons.append(btn)
        # idClicked only fires on user interaction, not on setChecked() --
        # safe from spuriously re-emitting level_changed.
        group.idClicked.connect(
            lambda level, app=app_name: self._on_level_clicked(app, level)
        )
        self._button_groups[app_name] = group
        self._pill_buttons[app_name] = pill_buttons
        layout.addLayout(pills_row)

        cb.toggled.connect(lambda on, app=app_name: self._on_checkbox_toggled(app, on))

        return row

    def _on_checkbox_toggled(self, app_name, checked):
        for btn in self._pill_buttons[app_name]:
            btn.setEnabled(checked)

    def _on_level_clicked(self, app_name, level):
        self._levels[app_name] = level
        self.level_changed.emit(app_name, level)

    def _on_toggle_clicked(self):
        enabled = self.toggle_btn.isChecked()
        self._apply_toggle_style(enabled)
        selected = [app for app, cb in self.checkboxes.items() if cb.isChecked()]
        intention = self.intention_input.text().strip() or DEFAULT_INTENTION
        self.protection_toggled.emit(enabled, intention, selected)

    def set_enabled_state(self, enabled: bool):
        """Sync the toggle's visual state to MainWindow's real
        protection_enabled flag, WITHOUT emitting protection_toggled --
        call this every time the screen is navigated to. Otherwise the
        toggle could visually desync from the real state, and the next tap
        would flip it the wrong way."""
        self.toggle_btn.setChecked(enabled)
        self._apply_toggle_style(enabled)

    def _apply_toggle_style(self, enabled):
        self.toggle_btn.setText("Protection ON" if enabled else "Activate Protection")
        # objectName swaps don't auto-repaint under Qt style sheets --
        # unpolish/polish forces the new selector to actually apply.
        self.toggle_btn.setObjectName("primaryBtn" if enabled else "secondaryBtn")
        self.toggle_btn.style().unpolish(self.toggle_btn)
        self.toggle_btn.style().polish(self.toggle_btn)
