from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal

from core.mock_data import (
    UNLOCKS_TODAY, NOTIFICATIONS_TODAY,
    DEFAULT_PROTECTED_APPS, usage_breakdown, is_high_usage, usage_color,
    current_screen_time_today,
)
from core.strings import t, DEFAULT_LANGUAGE
from ui.widgets.stat_card import StatCard
from ui.widgets.usage_ring_chart import UsageRingChart


class DashboardScreen(QWidget):
    focus_toggled = Signal()  # user clicked Activate/Deactivate Focus Mode
    go_to_protection = Signal()
    go_home = Signal()

    def __init__(self, protected_apps=None):
        super().__init__()
        self.focus_active = False
        self._language = DEFAULT_LANGUAGE
        self._protected = set(
            DEFAULT_PROTECTED_APPS if protected_apps is None else protected_apps
        )
        self._build_ui()
        self._refresh_legend()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(20)

        self.title = QLabel(t("dashboard_title", self._language))
        self.title.setObjectName("screenTitle")
        root.addWidget(self.title)

        root.addWidget(self._build_screen_time_card())

        stats_row = QHBoxLayout()
        self.unlocks_card = StatCard(t("unlocks", self._language), str(UNLOCKS_TODAY))
        self.notifications_card = StatCard(t("notifications", self._language), str(NOTIFICATIONS_TODAY))
        stats_row.addWidget(self.unlocks_card)
        stats_row.addWidget(self.notifications_card)
        root.addLayout(stats_row)

        root.addStretch()

        self.focus_label = QLabel(t("focus_mode", self._language))
        self.focus_label.setObjectName("sectionLabel")
        root.addWidget(self.focus_label)

        self.focus_btn = QPushButton(t("activate_focus_mode", self._language))
        self.focus_btn.setObjectName("focusBtnIdle")
        # Toggles protection in place -- does NOT navigate anywhere. Now
        # that the button visually reads as a direct on/off control (gray
        # idle / green active), sending the user to a whole separate
        # screen just to flip it would contradict that. Configuring WHICH
        # apps/levels/intention is still a separate action via "Set your
        # intention" below.
        self.focus_btn.clicked.connect(lambda: self.focus_toggled.emit())
        root.addWidget(self.focus_btn)

        self.protection_btn = QPushButton(t("set_your_intention", self._language))
        self.protection_btn.setObjectName("linkBtn")
        self.protection_btn.clicked.connect(lambda: self.go_to_protection.emit())
        root.addWidget(self.protection_btn)

        self.home_btn = QPushButton(t("home", self._language))
        self.home_btn.setObjectName("linkBtn")
        self.home_btn.clicked.connect(lambda: self.go_home.emit())
        root.addWidget(self.home_btn)

    def _build_screen_time_card(self):
        """Screen time today, as a value + a ring chart showing the
        proportion of time per app, with a color-matched legend list below.
        The ring's data comes straight from usage_breakdown() (derived from
        TOP_APPS) rather than a separate hardcoded dataset. The legend also
        doubles as the app list -- it carries the "Protected" badge that used
        to live in a separate, now-removed "Top apps" section, since showing
        the same apps/times twice on one screen was redundant."""
        card = QFrame()
        card.setObjectName("screenTimeCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)

        top_row = QHBoxLayout()
        top_row.setSpacing(16)

        # Ambient 2-state tint (no numeric score, no warning text) -- see
        # core.mock_data.usage_color()/is_high_usage(). Applied directly on
        # this specific label rather than through a QSS selector, since it
        # depends on runtime mock data, not a fixed style class.
        tint = usage_color(is_high_usage())

        text_block = QVBoxLayout()
        text_block.setSpacing(2)
        self.screen_time_label = QLabel(current_screen_time_today())
        self.screen_time_label.setObjectName("bigScreenTime")
        self.screen_time_label.setStyleSheet(f"color: {tint};")
        self.screen_time_caption = QLabel(t("screen_time_today", self._language))
        self.screen_time_caption.setObjectName("caption")
        text_block.addWidget(self.screen_time_label)
        text_block.addWidget(self.screen_time_caption)
        text_block.addStretch()
        top_row.addLayout(text_block)
        top_row.addStretch()

        # The ambient tint stays on the screen-time text only (above) --
        # the ring keeps its own fixed, neutral border regardless of
        # ambient state (that border exists purely so a dark segment like
        # X (Twitter)'s isn't invisible against the card background, see
        # UsageRingChart's own docstring; tinting it teal/amber read as
        # visually off and conflated two different signals).
        self._breakdown = usage_breakdown()
        self.ring_chart = UsageRingChart(
            [(name, minutes, color) for name, minutes, _, color in self._breakdown],
        )
        top_row.addWidget(self.ring_chart)
        card_layout.addLayout(top_row)

        self._legend_layout = QVBoxLayout()
        self._legend_layout.setSpacing(10)
        card_layout.addLayout(self._legend_layout)

        return card

    def _build_legend_row(self, name, time_str, color, protected):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        dot = QLabel()
        dot.setObjectName("usageLegendDot")
        dot.setFixedSize(10, 10)
        # Per-instance color, same reasoning as AppIcon/FakeAppScreen's
        # avatar styling elsewhere in this codebase -- the color varies per
        # app so it can't live in the shared stylesheet. The border reuses
        # the palette's existing #3a3f47 so the dot stays visible even for
        # apps whose own color (e.g. X (Twitter)) matches a card background.
        dot.setStyleSheet(
            f"background-color: {color}; border-radius: 5px; "
            "border: 1px solid #3a3f47;"
        )
        layout.addWidget(dot)

        # App name is a real brand name -- never translated, same rule as
        # every other screen in this app.
        name_lbl = QLabel(name)
        name_lbl.setObjectName("appName")
        layout.addWidget(name_lbl)

        if protected:
            badge = QLabel(t("protected", self._language))
            badge.setObjectName("badge")
            layout.addWidget(badge)

        layout.addStretch()

        time_lbl = QLabel(time_str)
        time_lbl.setObjectName("appTime")
        layout.addWidget(time_lbl)

        return row

    def set_focus_active(self, active: bool):
        self.focus_active = active
        self._apply_focus_text()
        self.focus_btn.setObjectName("focusBtnActive" if active else "focusBtnIdle")
        # objectName swaps don't auto-repaint under Qt style sheets --
        # unpolish/polish forces the new selector to actually apply (same
        # idiom used for the Set Your Intention screen's overall toggle).
        self.focus_btn.style().unpolish(self.focus_btn)
        self.focus_btn.style().polish(self.focus_btn)

    def _apply_focus_text(self):
        key = "deactivate_focus_mode" if self.focus_active else "activate_focus_mode"
        self.focus_btn.setText(t(key, self._language))

    def set_protected_apps(self, protected_apps):
        """Update which apps are currently protected, e.g. after Setup is
        activated — refreshes the legend's "Protected" badges so they don't
        go stale."""
        self._protected = set(protected_apps)
        self._refresh_legend()

    def set_language(self, lang):
        """Retranslate this screen's own UI copy -- app names stay
        untranslated (real brand names), everything else (labels, section
        headers, button text) switches. Scoped deliberately to Phone Home
        + Dashboard only, see CLAUDE.md."""
        self._language = lang
        self.title.setText(t("dashboard_title", lang))
        self.screen_time_caption.setText(t("screen_time_today", lang))
        self.unlocks_card.set_label(t("unlocks", lang))
        self.notifications_card.set_label(t("notifications", lang))
        self.focus_label.setText(t("focus_mode", lang))
        self._apply_focus_text()
        self.protection_btn.setText(t("set_your_intention", lang))
        self.home_btn.setText(t("home", lang))
        self._refresh_legend()  # "Protected" badges need the new language too

    def refresh_usage_data(self):
        """Recompute the screen-time total/tint/ring/legend from current
        (possibly shuffled) mock data -- called by MainWindow after
        Shuffle so this screen doesn't keep showing stale numbers."""
        self._breakdown = usage_breakdown()
        tint = usage_color(is_high_usage())
        self.screen_time_label.setText(current_screen_time_today())
        self.screen_time_label.setStyleSheet(f"color: {tint};")
        self.ring_chart.set_segments(
            [(name, minutes, color) for name, minutes, _, color in self._breakdown]
        )
        self._refresh_legend()

    def _refresh_legend(self):
        while self._legend_layout.count():
            item = self._legend_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                # setParent(None) detaches (and hides) it immediately --
                # takeAt() alone only unmanages it from the layout, so
                # without this it stays visible at its old position until
                # deleteLater() actually runs on a later event-loop pass.
                widget.setParent(None)
                widget.deleteLater()
        for name, _, time_str, color in self._breakdown:
            self._legend_layout.addWidget(
                self._build_legend_row(name, time_str, color, name in self._protected)
            )
