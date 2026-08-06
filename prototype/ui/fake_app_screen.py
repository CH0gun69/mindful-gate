from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal

from core.mock_data import glyph_for


class FakeAppScreen(QWidget):
    """A generic 'you opened the app' mock screen. Reconfigured per-app via
    set_app() instead of building one bespoke UI per app — everything here
    is clearly-labeled placeholder content, matching the rest of this
    prototype's hardcoded-mock-data approach."""

    go_back = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("fakeAppScreen")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        self._body_layout = QVBoxLayout()
        self._body_layout.setContentsMargins(20, 20, 20, 20)
        self._body_layout.setSpacing(12)
        body_wrap = QWidget()
        body_wrap.setLayout(self._body_layout)
        root.addWidget(body_wrap)

        root.addStretch()

    def _build_header(self):
        header = QFrame()
        header.setObjectName("fakeAppHeader")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        back_btn = QPushButton("←")
        back_btn.setObjectName("fakeAppBackBtn")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.go_back.emit())
        layout.addWidget(back_btn)

        self.avatar = QLabel()
        self.avatar.setObjectName("fakeAppAvatar")
        self.avatar.setFixedSize(36, 36)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.avatar)

        self.title = QLabel()
        self.title.setObjectName("fakeAppTitle")
        layout.addWidget(self.title)
        layout.addStretch()

        return header

    def set_app(self, name):
        glyph, color = glyph_for(name)
        self.title.setText(name)
        self.avatar.setText(glyph)
        self.avatar.setStyleSheet(
            f"background-color: {color}; border-radius: 10px; "
            "color: #ffffff; font-size: 16px; font-weight: 600;"
        )

        while self._body_layout.count():
            item = self._body_layout.takeAt(0)
            if item is None:
                continue
            w = item.widget()
            if w is not None:
                w.deleteLater()

        note = QLabel(f"This is a mock {name} screen for the demo — no real content is loaded.")
        note.setObjectName("fakeAppNote")
        note.setWordWrap(True)
        self._body_layout.addWidget(note)

        for i in range(1, 5):
            card = QFrame()
            card.setObjectName("fakeAppCard")
            card_layout = QVBoxLayout(card)
            card_layout.addWidget(QLabel(f"Fake {name} content #{i}"))
            self._body_layout.addWidget(card)
