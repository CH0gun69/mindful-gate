from PySide6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QSize

from core.mock_data import UNLOCKS_TODAY, current_screen_time_today
from core.strings import t, DEFAULT_LANGUAGE


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
        self.value = QLabel(current_screen_time_today())
        self.value.setObjectName("screenTimeValue")
        self.caption = QLabel(t("screen_time_today", DEFAULT_LANGUAGE))
        self.caption.setObjectName("screenTimeCaption")
        time_block.addWidget(self.value)
        time_block.addWidget(self.caption)
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
        self.unlocks_caption = QLabel(t("unlocks", DEFAULT_LANGUAGE))
        self.unlocks_caption.setObjectName("screenTimeUnlocksCaption")
        self.unlocks_caption.setAlignment(Qt.AlignmentFlag.AlignRight)
        unlocks_block.addWidget(unlocks_value)
        unlocks_block.addWidget(self.unlocks_caption)
        layout.addLayout(unlocks_block)

        for lbl in (self.value, self.caption, unlocks_value, self.unlocks_caption):
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

    def refresh_screen_time(self):
        """Re-read the (possibly shuffled) total from mock_data -- called
        after Shuffle so this widget doesn't keep showing a stale value."""
        self.value.setText(current_screen_time_today())

    def set_language(self, lang):
        self.caption.setText(t("screen_time_today", lang))
        self.unlocks_caption.setText(t("unlocks", lang))
