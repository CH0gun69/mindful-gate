from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatCard(QFrame):
    def __init__(self, label, value):
        super().__init__()
        self.setObjectName("statCard")
        layout = QVBoxLayout(self)
        value_lbl = QLabel(value)
        value_lbl.setObjectName("statValue")
        label_lbl = QLabel(label)
        label_lbl.setObjectName("statLabel")
        layout.addWidget(value_lbl)
        layout.addWidget(label_lbl)
