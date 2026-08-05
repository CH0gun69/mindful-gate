from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt, Signal

from core.mock_data import (
    SCREEN_TIME_TODAY, UNLOCKS_TODAY, NOTIFICATIONS_TODAY, TOP_APPS,
    DEFAULT_PROTECTED_APPS,
)
from ui.widgets.stat_card import StatCard
from ui.widgets.app_row import AppRow

SIMULATED_APP = "Instagram"


class DashboardScreen(QWidget):
    go_to_setup = Signal()
    go_to_insights = Signal()
    go_home = Signal()
    simulate_open = Signal(str)

    def __init__(self, protected_apps=None):
        super().__init__()
        self.focus_active = False
        self._protected = set(
            DEFAULT_PROTECTED_APPS if protected_apps is None else protected_apps
        )
        self._build_ui()
        self._refresh_top_apps()
        self._refresh_simulate_btn()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(20)

        title = QLabel("Dashboard")
        title.setObjectName("screenTitle")
        root.addWidget(title)

        screen_time = QLabel(SCREEN_TIME_TODAY)
        screen_time.setObjectName("bigScreenTime")
        caption = QLabel("Screen time today")
        caption.setObjectName("caption")
        root.addWidget(screen_time)
        root.addWidget(caption)

        stats_row = QHBoxLayout()
        stats_row.addWidget(StatCard("Unlocks", str(UNLOCKS_TODAY)))
        stats_row.addWidget(StatCard("Notifications", str(NOTIFICATIONS_TODAY)))
        root.addLayout(stats_row)

        apps_label = QLabel("Top apps")
        apps_label.setObjectName("sectionLabel")
        root.addWidget(apps_label)

        self._top_apps_layout = QVBoxLayout()
        self._top_apps_layout.setSpacing(8)
        root.addLayout(self._top_apps_layout)

        root.addStretch()

        self.focus_btn = QPushButton("Activate Focus Mode")
        self.focus_btn.setObjectName("primaryBtn")
        self.focus_btn.clicked.connect(lambda: self.go_to_setup.emit())
        root.addWidget(self.focus_btn)

        self.sim_btn = QPushButton(f"▶ Simulate opening {SIMULATED_APP}")
        self.sim_btn.setObjectName("simulateBtn")
        self.sim_btn.clicked.connect(self._on_simulate_clicked)
        root.addWidget(self.sim_btn)

        insights_btn = QPushButton("View Insights")
        insights_btn.setObjectName("linkBtn")
        insights_btn.clicked.connect(lambda: self.go_to_insights.emit())
        root.addWidget(insights_btn)

        home_btn = QPushButton("⌂ Home")
        home_btn.setObjectName("linkBtn")
        home_btn.clicked.connect(lambda: self.go_home.emit())
        root.addWidget(home_btn)

    def set_focus_active(self, active: bool, intention: str = ""):
        self.focus_active = active
        if active:
            self.focus_btn.setText(f"Focus Mode ON — \u201c{intention}\u201d")
        else:
            self.focus_btn.setText("Activate Focus Mode")

    def set_protected_apps(self, protected_apps):
        """Update which apps are currently protected, e.g. after Setup is
        activated — refreshes the "Protected" badges in Top apps and the
        Simulate button's enabled state so neither goes stale."""
        self._protected = set(protected_apps)
        self._refresh_top_apps()
        self._refresh_simulate_btn()

    def _refresh_top_apps(self):
        while self._top_apps_layout.count():
            item = self._top_apps_layout.takeAt(0)
            widget = item.widget()
            if widget:
                # setParent(None) detaches (and hides) it immediately —
                # takeAt() alone only unmanages it from the layout, so
                # without this it stays visible at its old position until
                # deleteLater() actually runs on a later event-loop pass.
                widget.setParent(None)
                widget.deleteLater()
        for app in TOP_APPS:
            self._top_apps_layout.addWidget(AppRow(app, app["name"] in self._protected))

    def _refresh_simulate_btn(self):
        is_protected = SIMULATED_APP in self._protected
        self.sim_btn.setEnabled(is_protected)
        self.sim_btn.setToolTip(
            "" if is_protected
            else f"{SIMULATED_APP} isn't currently protected — nothing to simulate."
        )

    def _on_simulate_clicked(self):
        # Defense in depth: the button is disabled whenever this wouldn't
        # apply, but guard the actual emit too in case it's ever triggered
        # programmatically.
        if SIMULATED_APP in self._protected:
            self.simulate_open.emit(SIMULATED_APP)
