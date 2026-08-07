from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, Property, QRectF, QSize

TRACK_WIDTH = 44
TRACK_HEIGHT = 24
THUMB_MARGIN = 2
ANIM_DURATION_MS = 175  # within the requested ~150-200ms

ON_COLOR = "#93cfc4"   # this session's softened teal accent
OFF_COLOR = "#3a3f47"  # existing muted border/divider gray
THUMB_COLOR = "#eef0f2"


class ToggleSwitch(QWidget):
    """A generic on/off switch: rounded track, circular thumb that slides
    between two x-positions with a short QPropertyAnimation -- used in
    place of a checkbox/text button wherever an on/off choice should read
    as a physical switch (see ProtectionCustomizationScreen's per-app
    "Protect" control). Purely presentational + isChecked()/setChecked()/
    toggled -- no app-specific knowledge, matching this project's
    ui/widgets/ convention of reusable, data-agnostic widgets (see AppIcon,
    StatCard, UsageRingChart). Same custom-Property + QPropertyAnimation
    idiom as ElasticScrollArea's overscroll bounce elsewhere in this
    codebase.
    """

    toggled = Signal(bool)

    def __init__(self, checked=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(TRACK_WIDTH, TRACK_HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = checked
        thumb_d = TRACK_HEIGHT - 2 * THUMB_MARGIN
        self._on_x = TRACK_WIDTH - THUMB_MARGIN - thumb_d
        self._off_x = THUMB_MARGIN
        self._thumb_x = float(self._on_x if checked else self._off_x)
        self._anim = None

    def isChecked(self):
        return self._checked

    def setChecked(self, checked, animate=True):
        """Programmatic set -- does NOT emit `toggled`, only a user click
        does (mirrors the old QButtonGroup.idClicked-only-on-user-click
        behavior), so seeding initial per-app state never spuriously
        triggers downstream signal handlers."""
        if checked == self._checked:
            return
        self._checked = checked
        target = float(self._on_x if checked else self._off_x)
        if animate and self.isVisible():
            self._animate_to(target)
        else:
            self._thumb_x = target
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            new_state = not self._checked
            self._checked = new_state
            self._animate_to(float(self._on_x if new_state else self._off_x))
            self.toggled.emit(new_state)
        event.accept()

    def _animate_to(self, target):
        if self._anim is not None:
            self._anim.stop()
        self._anim = QPropertyAnimation(self, b"thumbX", self)
        self._anim.setDuration(ANIM_DURATION_MS)
        self._anim.setStartValue(self._thumb_x)
        self._anim.setEndValue(target)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._anim.start()

    def _get_thumb_x(self):
        return self._thumb_x

    def _set_thumb_x(self, value):
        self._thumb_x = value
        self.update()

    thumbX = Property(float, _get_thumb_x, _set_thumb_x)

    def sizeHint(self):
        return QSize(TRACK_WIDTH, TRACK_HEIGHT)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        track_color = QColor(ON_COLOR if self._checked else OFF_COLOR)
        painter.setBrush(track_color)
        track_rect = QRectF(0, 0, TRACK_WIDTH, TRACK_HEIGHT)
        painter.drawRoundedRect(track_rect, TRACK_HEIGHT / 2, TRACK_HEIGHT / 2)

        thumb_d = TRACK_HEIGHT - 2 * THUMB_MARGIN
        painter.setBrush(QColor(THUMB_COLOR))
        thumb_rect = QRectF(self._thumb_x, THUMB_MARGIN, thumb_d, thumb_d)
        painter.drawEllipse(thumb_rect)
        painter.end()
