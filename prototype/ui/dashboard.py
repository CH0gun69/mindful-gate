from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt, Signal

from core.mock_data import SCREEN_TIME_TODAY, UNLOCKS_TODAY, NOTIFICATIONS_TODAY, TOP_APPS
from ui.widgets.stat_card import StatCard
from ui.widgets.app_row import AppRow


class DashboardScreen(QWidget):
    go_to_setup = Signal()
    go_to_insights = Signal()
    go_home = Signal()
    simulate_open = Signal(str)

    def __init__(self):
        super().__init__()
        self.focus_active = False
        self._build_ui()

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
        for app in TOP_APPS:
            root.addWidget(AppRow(app))

        root.addStretch()

        self.focus_btn = QPushButton("Activate Focus Mode")
        self.focus_btn.setObjectName("primaryBtn")
        self.focus_btn.clicked.connect(lambda: self.go_to_setup.emit())
        root.addWidget(self.focus_btn)

        sim_btn = QPushButton("▶ Simulate opening Instagram")
        sim_btn.setObjectName("simulateBtn")
        sim_btn.clicked.connect(lambda: self.simulate_open.emit("Instagram"))
        root.addWidget(sim_btn)

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