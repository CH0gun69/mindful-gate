from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


class LevelSlider(QSlider):
    """A QSlider restricted to a small fixed set of integer positions
    (e.g. 1..3), where clicking or dragging ANYWHERE on the track jumps
    directly to the nearest position instead of Qt's default groove-click
    page-step behavior. Generic -- min/max passed in by the caller, no
    knowledge of PROTECTION_LEVELS or any other app-specific data (matches
    this project's ui/widgets/ convention of reusable, data-agnostic
    widgets)."""

    def __init__(self, minimum, maximum, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setSingleStep(1)
        self.setPageStep(1)

    def _value_from_x(self, x):
        span = max(self.width(), 1)
        fraction = min(max(x / span, 0.0), 1.0)
        raw = self.minimum() + fraction * (self.maximum() - self.minimum())
        return int(round(raw))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setValue(self._value_from_x(event.position().x()))
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.setValue(self._value_from_x(event.position().x()))
            event.accept()
            return
        super().mouseMoveEvent(event)
