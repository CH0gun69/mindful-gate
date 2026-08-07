from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import (
    Qt, QSize, QPropertyAnimation, QSequentialAnimationGroup, QEasingCurve, Property,
)

# #93cfc4 (this session's softened teal) at ~40% opacity -- calm fill,
# no new colors introduced.
FILL_COLOR = QColor(147, 207, 196, 100)


class BreathingCircle(QWidget):
    """A circle that smoothly grows then shrinks on a repeating loop,
    replacing InterruptionScreen's old cycling breathe-in/breathe-out TEXT
    entirely -- a wordless visual pulse instead. Generic -- min/max
    diameter and cycle length are constructor args, no knowledge of
    PROTECTION_LEVELS/BREATHING_CYCLE_MS.

    A single looping QPropertyAnimation would sawtooth-reset (start->end,
    snap back to start, repeat) rather than breathe in and out, so this
    uses a QSequentialAnimationGroup of two chained animations -- grow
    then shrink, each half of cycle_ms, both eased with InOutSine so the
    motion settles at both ends instead of snapping. Same custom-Property
    + QPropertyAnimation idiom as ElasticScrollArea's overscroll bounce
    elsewhere in this codebase.
    """

    def __init__(self, min_diameter=36, max_diameter=64, cycle_ms=2500, parent=None):
        super().__init__(parent)
        self._min_d = min_diameter
        self._max_d = max_diameter
        self._cycle_ms = cycle_ms
        self._diameter = float(min_diameter)
        # Fixed widget size so the bounding box never reflows the layout --
        # only the drawn circle inside grows/shrinks.
        self.setFixedSize(max_diameter, max_diameter)
        self._group = None

    def start(self):
        """(Re)start the breathing loop from a clean min-diameter state --
        rebuilding the animation group each call avoids any stale
        animation state carrying over from a previous app/level, since
        this widget instance is reused across every InterruptionScreen
        trigger."""
        self.stop()
        self._diameter = float(self._min_d)
        self.update()

        half = max(self._cycle_ms // 2, 1)
        grow = QPropertyAnimation(self, b"diameter", self)
        grow.setDuration(half)
        grow.setStartValue(float(self._min_d))
        grow.setEndValue(float(self._max_d))
        grow.setEasingCurve(QEasingCurve.Type.InOutSine)

        shrink = QPropertyAnimation(self, b"diameter", self)
        shrink.setDuration(half)
        shrink.setStartValue(float(self._max_d))
        shrink.setEndValue(float(self._min_d))
        shrink.setEasingCurve(QEasingCurve.Type.InOutSine)

        self._group = QSequentialAnimationGroup(self)
        self._group.addAnimation(grow)
        self._group.addAnimation(shrink)
        self._group.setLoopCount(-1)
        self._group.start()

    def stop(self):
        if self._group is not None:
            self._group.stop()
            self._group = None
        self._diameter = float(self._min_d)
        self.update()

    def _get_diameter(self):
        return self._diameter

    def _set_diameter(self, value):
        self._diameter = value
        self.update()

    diameter = Property(float, _get_diameter, _set_diameter)

    def sizeHint(self):
        return QSize(self._max_d, self._max_d)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(FILL_COLOR)
        cx, cy = self.width() / 2, self.height() / 2
        r = self._diameter / 2
        painter.drawEllipse(int(cx - r), int(cy - r), int(self._diameter), int(self._diameter))
        painter.end()
