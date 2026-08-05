from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QLineEdit
)
from PySide6.QtCore import Signal

from core.mock_data import PROTECTABLE_APPS, DEFAULT_INTENTION, DEFAULT_PROTECTED_APPS


class IntentionSetupScreen(QWidget):
    activated = Signal(str, list)  # intention text, protected apps
    go_back = Signal()

    def __init__(self):
        super().__init__()
        self.checkboxes = {}
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 32, 32, 32)
        root.setSpacing(16)

        title = QLabel("Set Your Intention")
        title.setObjectName("screenTitle")
        root.addWidget(title)

        subtitle = QLabel("Choose which apps to protect, and why you're using them.")
        subtitle.setObjectName("caption")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        apps_label = QLabel("Protect these apps")
        apps_label.setObjectName("sectionLabel")
        root.addWidget(apps_label)

        for app in PROTECTABLE_APPS:
            cb = QCheckBox(app)
            cb.setChecked(app in DEFAULT_PROTECTED_APPS)
            self.checkboxes[app] = cb
            root.addWidget(cb)

        intent_label = QLabel("Your intention")
        intent_label.setObjectName("sectionLabel")
        root.addWidget(intent_label)

        self.intention_input = QLineEdit(DEFAULT_INTENTION)
        self.intention_input.setObjectName("intentionInput")
        root.addWidget(self.intention_input)

        root.addStretch()

        activate_btn = QPushButton("Activate Protection")
        activate_btn.setObjectName("primaryBtn")
        activate_btn.clicked.connect(self._on_activate)
        root.addWidget(activate_btn)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("linkBtn")
        back_btn.clicked.connect(lambda: self.go_back.emit())
        root.addWidget(back_btn)

    def _on_activate(self):
        selected = [app for app, cb in self.checkboxes.items() if cb.isChecked()]
        intention = self.intention_input.text().strip() or DEFAULT_INTENTION
        self.activated.emit(intention, selected)