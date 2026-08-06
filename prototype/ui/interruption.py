from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal


class InterruptionScreen(QWidget):
    continue_clicked = Signal()
    go_back_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("interruptionScreen")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(48, 64, 48, 48)
        root.setSpacing(24)
        root.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.app_label = QLabel("You opened Instagram.")
        self.app_label.setObjectName("interruptTitle")
        self.app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.app_label)

        question = QLabel("Still on purpose?")
        question.setObjectName("interruptQuestion")
        question.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(question)

        self.intention_label = QLabel()
        self.intention_label.setObjectName("intentionQuote")
        self.intention_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intention_label.setWordWrap(True)
        root.addWidget(self.intention_label)

        root.addStretch(2)

        icon = QLabel("🧘")
        icon.setObjectName("interruptIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(icon)

        root.addStretch(3)

        back_btn = QPushButton("Go Back")
        back_btn.setObjectName("primaryBtn")
        back_btn.clicked.connect(lambda: self.go_back_clicked.emit())
        root.addWidget(back_btn)

        continue_btn = QPushButton("Continue Anyway")
        continue_btn.setObjectName("secondaryBtn")
        continue_btn.clicked.connect(lambda: self.continue_clicked.emit())
        root.addWidget(continue_btn)

    def set_context(self, app_name: str, intention: str):
        self.app_label.setText(f"You opened {app_name}.")
        self.intention_label.setText(f"\u201c{intention}\u201d")