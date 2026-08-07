from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

from core.mock_data import glyph_for, icon_path_for
from ui.widgets.svg_icon import white_svg_pixmap

AVATAR_SIZE = 72


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

        self.icon = QLabel()
        self.icon.setObjectName("interruptIcon")
        self.icon.setFixedSize(AVATAR_SIZE, AVATAR_SIZE)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignHCenter)

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

        # Show the real app's icon (brand-logo SVG if it has one, else its
        # emoji/letter glyph) instead of a generic icon, matching how
        # Phone Home / Fake App render the same app -- see AppIcon /
        # FakeAppScreen.set_app() for the same pattern.
        glyph, color = glyph_for(app_name)
        self.icon.setStyleSheet(
            f"background-color: {color}; border-radius: {AVATAR_SIZE // 4}px;"
        )
        icon_path = icon_path_for(app_name)
        if icon_path:
            self.icon.setPixmap(white_svg_pixmap(icon_path, int(AVATAR_SIZE * 0.6)))
        else:
            self.icon.setText(glyph)
            self.icon.setStyleSheet(
                self.icon.styleSheet()
                + f" color: #ffffff; font-size: {AVATAR_SIZE // 2}px; font-weight: 600;"
            )