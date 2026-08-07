from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QLineEdit
)
from PySide6.QtCore import Signal

from core.mock_data import PROTECTABLE_APPS, DEFAULT_INTENTION, DEFAULT_PROTECTED_APPS


class IntentionSetupScreen(QWidget):
    protection_toggled = Signal(bool, str, list)  # enabled, intention text, protected apps
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

        self.toggle_btn = QPushButton("Activate Protection")
        self.toggle_btn.setObjectName("secondaryBtn")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.clicked.connect(self._on_toggle_clicked)
        root.addWidget(self.toggle_btn)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("linkBtn")
        back_btn.clicked.connect(lambda: self.go_back.emit())
        root.addWidget(back_btn)

    def _on_toggle_clicked(self):
        enabled = self.toggle_btn.isChecked()
        self._apply_toggle_style(enabled)
        selected = [app for app, cb in self.checkboxes.items() if cb.isChecked()]
        intention = self.intention_input.text().strip() or DEFAULT_INTENTION
        self.protection_toggled.emit(enabled, intention, selected)

    def set_enabled_state(self, enabled: bool):
        """Sync the toggle's visual state to MainWindow's real
        protection_enabled flag, WITHOUT emitting protection_toggled --
        call this every time the screen is navigated to. Otherwise the
        toggle would visually reset to OFF on every re-visit even while
        protection is still active, and the next tap would incorrectly
        flip it off."""
        self.toggle_btn.setChecked(enabled)
        self._apply_toggle_style(enabled)

    def _apply_toggle_style(self, enabled):
        self.toggle_btn.setText("Protection ON" if enabled else "Activate Protection")
        # objectName swaps don't auto-repaint under Qt style sheets --
        # unpolish/polish forces the new selector to actually apply.
        self.toggle_btn.setObjectName("primaryBtn" if enabled else "secondaryBtn")
        self.toggle_btn.style().unpolish(self.toggle_btn)
        self.toggle_btn.style().polish(self.toggle_btn)