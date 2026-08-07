from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal

from core.mock_data import (
    SCREEN_TIME_TODAY, UNLOCKS_TODAY, NOTIFICATIONS_TODAY,
    DEFAULT_PROTECTED_APPS, usage_breakdown, is_high_usage, usage_color,
)
from ui.widgets.stat_card import StatCard
from ui.widgets.usage_ring_chart import UsageRingChart


class DashboardScreen(QWidget):
    go_to_setup = Signal()
    go_to_protection = Signal()
    go_home = Signal()

    def __init__(self, protected_apps=None):
        super().__init__()
        self.focus_active = False
        self._protected = set(
            DEFAULT_PROTECTED_APPS if protected_apps is None else protected_apps
        )
        self._build_ui()
        self._refresh_legend()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(20)

        title = QLabel("Dashboard")
        title.setObjectName("screenTitle")
        root.addWidget(title)

        root.addWidget(self._build_screen_time_card())

        stats_row = QHBoxLayout()
        stats_row.addWidget(StatCard("Unlocks", str(UNLOCKS_TODAY)))
        stats_row.addWidget(StatCard("Notifications", str(NOTIFICATIONS_TODAY)))
        root.addLayout(stats_row)

        root.addStretch()

        self.focus_btn = QPushButton("Activate Focus Mode")
        self.focus_btn.setObjectName("primaryBtn")
        self.focus_btn.clicked.connect(lambda: self.go_to_setup.emit())
        root.addWidget(self.focus_btn)

        protection_btn = QPushButton("Set your intention")
        protection_btn.setObjectName("linkBtn")
        protection_btn.clicked.connect(lambda: self.go_to_protection.emit())
        root.addWidget(protection_btn)

        home_btn = QPushButton("⌂ Home")
        home_btn.setObjectName("linkBtn")
        home_btn.clicked.connect(lambda: self.go_home.emit())
        root.addWidget(home_btn)

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
        screen_time = QLabel(SCREEN_TIME_TODAY)
        screen_time.setObjectName("bigScreenTime")
        screen_time.setStyleSheet(f"color: {tint};")
        caption = QLabel("Screen time today")
        caption.setObjectName("caption")
        text_block.addWidget(screen_time)
        text_block.addWidget(caption)
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

        name_lbl = QLabel(name)
        name_lbl.setObjectName("appName")
        layout.addWidget(name_lbl)

        if protected:
            badge = QLabel("Protected")
            badge.setObjectName("badge")
            layout.addWidget(badge)

        layout.addStretch()

        time_lbl = QLabel(time_str)
        time_lbl.setObjectName("appTime")
        layout.addWidget(time_lbl)

        return row

    def set_focus_active(self, active: bool, intention: str = ""):
        self.focus_active = active
        if active:
            self.focus_btn.setText(f"Focus Mode ON — “{intention}”")
        else:
            self.focus_btn.setText("Activate Focus Mode")

    def set_protected_apps(self, protected_apps):
        """Update which apps are currently protected, e.g. after Setup is
        activated — refreshes the legend's "Protected" badges so they don't
        go stale."""
        self._protected = set(protected_apps)
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
