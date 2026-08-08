from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit,
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve

from core.mock_data import (
    glyph_for, icon_path_for, PROTECTABLE_APPS, DEFAULT_PROTECTED_APPS,
    DEFAULT_APP_PROTECTION_LEVELS, PROTECTION_LEVELS, DEFAULT_INTENTION,
)
from core.strings import t, DEFAULT_LANGUAGE
from ui.widgets.svg_icon import white_svg_pixmap
from ui.widgets.toggle_switch import ToggleSwitch
from ui.widgets.level_slider import LevelSlider
from ui.widgets.elastic_scroll_area import ElasticScrollArea

ROW_AVATAR_SIZE = 40
LEVEL_ANIM_MS = 180


class ProtectionCustomizationScreen(QWidget):
    """Single combined destination for setting up protection -- merges what
    used to be two separate screens (Setup + Protection Customization) into
    one: pick which apps to protect, write a message, and set each app's
    friction level (1/2/3, see core.mock_data.PROTECTION_LEVELS). The
    overall on/off switch lives on Dashboard only (Activate/Deactivate
    Focus Mode) -- this screen has no master toggle of its own, so every
    change here applies live/instantly instead of needing a commit action.

    One row per app: an icon/name line ending in a "Protect" ToggleSwitch,
    and -- revealed with a smooth expand/collapse only while that app's
    switch is on -- a labeled LevelSlider for its 1/2/3 friction level.

    The row list itself never changes (always all of PROTECTABLE_APPS), so
    unlike a dynamic list this doesn't need a rebuild-on-update pattern --
    rows are built once in _build_ui() and just get enabled/disabled or
    re-checked in place."""

    protected_apps_changed = Signal(list)  # live -- fires on every per-app switch toggle
    intention_changed = Signal(str)  # live -- fires when the message field loses focus
    level_changed = Signal(str, int)  # app_name, new level
    go_back = Signal()

    def __init__(self):
        super().__init__()
        self.switches = {}  # app_name -> ToggleSwitch
        self._levels = dict(DEFAULT_APP_PROTECTION_LEVELS)  # app_name -> level
        self._level_containers = {}  # app_name -> QWidget wrapping the level row
        self._level_sliders = {}  # app_name -> LevelSlider
        self._level_labels = {}  # app_name -> QLabel
        self._level_anims = {}  # app_name -> QPropertyAnimation, kept alive
        self._language = DEFAULT_LANGUAGE
        self._build_ui()

    def _build_ui(self):
        # This screen has grown a lot since the Setup+Customization merge
        # (6 app rows, each able to expand a level control) -- tall enough
        # that with several apps protected at once, the fixed 780px window
        # had no room left and Qt was silently compressing every row below
        # its natural size to fit (confirmed via sizeHint()/actual-height
        # mismatch: a level row's container measured shorter than its own
        # sizeHint), which is what made the slider visually spill outside
        # its row's box when expanded. Wrapping the body in a scroll area
        # (same ElasticScrollArea used for Fake App's feed/messages) lets
        # it scroll instead of being forced to overlap.
        page_root = QVBoxLayout(self)
        page_root.setContentsMargins(0, 0, 0, 0)
        page_root.setSpacing(0)

        header = QVBoxLayout()
        header.setContentsMargins(32, 32, 32, 0)
        header.setSpacing(16)

        self.title = QLabel(t("set_your_intention_title", self._language) or "")
        self.title.setObjectName("screenTitle")
        header.addWidget(self.title)

        self.subtitle = QLabel(t("protection_subtitle", self._language) or "")
        self.subtitle.setObjectName("caption")
        self.subtitle.setWordWrap(True)
        header.addWidget(self.subtitle)

        page_root.addLayout(header)

        body = QWidget()
        root = QVBoxLayout(body)
        root.setContentsMargins(32, 16, 32, 32)
        root.setSpacing(16)

        rows_layout = QVBoxLayout()
        rows_layout.setSpacing(10)
        for app in PROTECTABLE_APPS:
            rows_layout.addWidget(self._build_row(app))
        root.addLayout(rows_layout)

        self.intent_label = QLabel(t("your_message", self._language) or "")
        self.intent_label.setObjectName("sectionLabel")
        root.addWidget(self.intent_label)

        # The message text itself (both the placeholder default and
        # whatever the user types) is USER INPUT, never translated -- same
        # rule as Interruption's intention quote.
        self.intention_input = QLineEdit(DEFAULT_INTENTION)
        self.intention_input.setObjectName("intentionInput")
        # Live/instant like everything else on this screen -- no master
        # toggle here to gate a "commit" action on, so the message just
        # applies whenever the field loses focus (editingFinished), same
        # as a per-app switch or level slider applying immediately on
        # interaction.
        self.intention_input.editingFinished.connect(self._on_intention_edited)
        root.addWidget(self.intention_input)

        self.back_btn = QPushButton(t("back", self._language) or "")
        self.back_btn.setObjectName("linkBtn")
        self.back_btn.clicked.connect(lambda: self.go_back.emit())
        root.addWidget(self.back_btn)

        scroll = ElasticScrollArea()
        scroll.setObjectName("protectionScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(body)
        page_root.addWidget(scroll, 1)

    def _build_row(self, app_name):
        outer = QFrame()
        outer.setObjectName("appRow")
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(8, 8, 8, 8)
        outer_layout.setSpacing(6)

        checked = app_name in DEFAULT_PROTECTED_APPS

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

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
        top_row.addWidget(avatar)

        name_lbl = QLabel(app_name)
        name_lbl.setObjectName("appName")
        top_row.addWidget(name_lbl)
        top_row.addStretch()

        switch = ToggleSwitch(checked=checked)
        self.switches[app_name] = switch
        top_row.addWidget(switch)
        outer_layout.addLayout(top_row)

        # --- collapsible level control, indented under the app name,
        # only ever meaningful/visible while Protect is on ---
        level_container = QWidget()
        level_layout = QHBoxLayout(level_container)
        level_layout.setContentsMargins(ROW_AVATAR_SIZE + 10, 0, 0, 0)
        level_layout.setSpacing(8)

        current_level = self._levels.get(app_name, 1)
        level_label = QLabel((t("level_label", self._language) or "").format(level=current_level))
        level_label.setObjectName("levelLabel")
        level_layout.addWidget(level_label)

        slider = LevelSlider(min(PROTECTION_LEVELS), max(PROTECTION_LEVELS))
        slider.setObjectName("levelSlider")
        slider.setFixedWidth(120)
        slider.setEnabled(checked)
        # Set the initial value BEFORE connecting valueChanged -- unlike
        # the old QButtonGroup.idClicked (which only ever fired on user
        # clicks), QSlider.valueChanged fires on programmatic setValue()
        # too, so connecting first would fire level_changed spuriously
        # during row construction.
        slider.setValue(current_level)
        slider.valueChanged.connect(
            lambda level, app=app_name: self._on_level_changed(app, level)
        )
        level_layout.addWidget(slider)
        level_layout.addStretch()

        self._level_sliders[app_name] = slider
        self._level_labels[app_name] = level_label
        self._level_containers[app_name] = level_container

        # sizeHint() is computed independent of the current maximumHeight
        # constraint, so this is safe to seed before the row is ever shown.
        level_container.setMaximumHeight(
            level_container.sizeHint().height() if checked else 0
        )
        outer_layout.addWidget(level_container)

        switch.toggled.connect(lambda on, app=app_name: self._on_switch_toggled(app, on))

        return outer

    def _on_switch_toggled(self, app_name, on):
        container = self._level_containers[app_name]
        self._level_sliders[app_name].setEnabled(on)

        anim = QPropertyAnimation(container, b"maximumHeight", self)
        anim.setDuration(LEVEL_ANIM_MS)
        anim.setStartValue(container.maximumHeight())
        anim.setEndValue(container.sizeHint().height() if on else 0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()
        self._level_anims[app_name] = anim  # keep alive until replaced

        selected = [app for app, sw in self.switches.items() if sw.isChecked()]
        self.protected_apps_changed.emit(selected)

    def _on_level_changed(self, app_name, level):
        self._levels[app_name] = level
        self._level_labels[app_name].setText((t("level_label", self._language) or "").format(level=level))
        self.level_changed.emit(app_name, level)

    def _on_intention_edited(self):
        intention = self.intention_input.text().strip() or DEFAULT_INTENTION
        self.intention_changed.emit(intention)

    def set_language(self, lang):
        """Retranslate this screen's own UI copy -- app names and the
        message field's text are never translated (real brand names /
        user input), only static labels/titles/buttons change."""
        self._language = lang
        self.title.setText(t("set_your_intention_title", lang) or "")
        self.subtitle.setText(t("protection_subtitle", lang) or "")
        self.intent_label.setText(t("your_message", lang) or "")
        self.back_btn.setText(t("back", lang) or "")
        for app_name, label in self._level_labels.items():
            label.setText((t("level_label", lang) or "").format(level=self._levels.get(app_name, 1)))
