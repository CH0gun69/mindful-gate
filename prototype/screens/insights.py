from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Signal

from data.mock_data import INSIGHTS


class InsightsScreen(QWidget):
    go_back = Signal()

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(20)

        title = QLabel("Insights")
        title.setObjectName("screenTitle")
        root.addWidget(title)

        kept = INSIGHTS["intentions_kept"]
        total = INSIGHTS["intentions_total"]

        card = QFrame()
        card.setObjectName("statCard")
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(self._stat(f"{kept} / {total}", "Intentions kept this week"))
        card_layout.addWidget(self._stat(INSIGHTS["time_saved_this_week"], "Time saved"))
        card_layout.addWidget(self._stat(INSIGHTS["most_interrupted_app"], "Most interrupted app"))
        root.addWidget(card)

        root.addStretch()

        back_btn = QPushButton("Back to Dashboard")
        back_btn.setObjectName("primaryBtn")
        back_btn.clicked.connect(lambda: self.go_back.emit())
        root.addWidget(back_btn)

    def _stat(self, value, label):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 8, 0, 8)
        v = QLabel(value)
        v.setObjectName("statValue")
        l = QLabel(label)
        l.setObjectName("statLabel")
        layout.addWidget(v)
        layout.addWidget(l)
        return w