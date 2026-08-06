from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen
from PySide6.QtCore import QRectF, QSize

RING_THICKNESS = 16
GAP_DEGREES = 3  # small visual gap between adjacent segments
# Reuses the palette's existing border/divider color (see styles.qss) as a
# thin outline on every segment -- not a new color. Needed because at least
# one app's own accent color (X (Twitter) -> #1d2026) is identical to this
# card's background; without an outline that segment would be invisible.
BORDER_COLOR = "#3a3f47"


class UsageRingChart(QWidget):
    """A simple donut/ring chart: each segment gets an arc proportional to
    its share of the total. Not pixel-perfect -- a handful of solid-color
    arced segments is enough for this prototype.

    segments: list of (label, minutes, color_hex) tuples. Drawn starting
    from 12 o'clock, clockwise, in the order given.
    """

    def __init__(self, segments=None, diameter=112, parent=None):
        super().__init__(parent)
        self._segments = segments or []
        self._diameter = diameter
        self.setFixedSize(diameter, diameter)

    def set_segments(self, segments):
        self._segments = segments
        self.update()

    def sizeHint(self):
        return QSize(self._diameter, self._diameter)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        total = sum(minutes for _, minutes, _ in self._segments)
        if total <= 0:
            painter.end()
            return

        margin = RING_THICKNESS / 2 + 1
        outer = QRectF(
            margin, margin,
            self.width() - 2 * margin, self.height() - 2 * margin,
        )
        inner_margin = margin + RING_THICKNESS
        inner = QRectF(
            inner_margin, inner_margin,
            self.width() - 2 * inner_margin, self.height() - 2 * inner_margin,
        )

        border_pen = QPen(QColor(BORDER_COLOR))
        border_pen.setWidthF(1)
        painter.setPen(border_pen)

        # Qt angles: 0 deg = 3 o'clock, positive = counter-clockwise.
        # Start at 12 o'clock (90 deg) and step clockwise (subtracting).
        start = 90.0
        for _, minutes, color in self._segments:
            span = (minutes / total) * 360
            drawn_span = max(span - GAP_DEGREES, 0)

            path = QPainterPath()
            path.arcMoveTo(outer, start)
            path.arcTo(outer, start, -drawn_span)
            path.arcTo(inner, start - drawn_span, drawn_span)
            path.closeSubpath()

            painter.setBrush(QColor(color))
            painter.drawPath(path)

            start -= span

        painter.end()
