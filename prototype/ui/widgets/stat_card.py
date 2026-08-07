from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatCard(QFrame):
    def __init__(self, label, value):
        super().__init__()
        self.setObjectName("statCard")
        layout = QVBoxLayout(self)
        self.value_lbl = QLabel(value)
        self.value_lbl.setObjectName("statValue")
        self.label_lbl = QLabel(label)
        self.label_lbl.setObjectName("statLabel")
        layout.addWidget(self.value_lbl)
        layout.addWidget(self.label_lbl)

    def set_label(self, label):
        self.label_lbl.setText(label)
