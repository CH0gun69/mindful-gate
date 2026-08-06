from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QSize

from core.mock_data import SCREEN_TIME_TODAY, UNLOCKS_TODAY


class ScreenTimeWidget(QPushButton):
    """Compact tappable screen-time summary card for the phone home screen —
    similar to a real phone's home-screen screen-time widget. Tapping it
    opens the Dashboard for the full breakdown."""

    def __init__(self):
        super().__init__()
        self.setObjectName("screenTimeWidget")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(14)

        time_block = QVBoxLayout()
        time_block.setSpacing(2)
        value = QLabel(SCREEN_TIME_TODAY)
        value.setObjectName("screenTimeValue")
        caption = QLabel("Screen time today")
        caption.setObjectName("screenTimeCaption")
        time_block.addWidget(value)
        time_block.addWidget(caption)
        layout.addLayout(time_block)

        layout.addStretch()

        divider = QFrame()
        divider.setObjectName("screenTimeDivider")
        divider.setFixedWidth(1)
        layout.addWidget(divider)

        unlocks_block = QVBoxLayout()
        unlocks_block.setSpacing(2)
        unlocks_value = QLabel(str(UNLOCKS_TODAY))
        unlocks_value.setObjectName("screenTimeUnlocksValue")
        unlocks_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        unlocks_caption = QLabel("Unlocks")
        unlocks_caption.setObjectName("screenTimeUnlocksCaption")
        unlocks_caption.setAlignment(Qt.AlignmentFlag.AlignRight)
        unlocks_block.addWidget(unlocks_value)
        unlocks_block.addWidget(unlocks_caption)
        layout.addLayout(unlocks_block)

        for lbl in (value, caption, unlocks_value, unlocks_caption):
            lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        divider.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # QPushButton.sizeHint() ignores the child layout entirely (same
        # issue as AppIcon) — force a sensible height so it doesn't collapse.
        # Width is left alone: QVBoxLayout still stretches it to full parent
        # width since QPushButton's horizontal size policy is Minimum, not Fixed.
        self._preferred_height = 72
        self.setMinimumHeight(self._preferred_height)

    def sizeHint(self):
        hint = super().sizeHint()
        return QSize(hint.width(), self._preferred_height)
