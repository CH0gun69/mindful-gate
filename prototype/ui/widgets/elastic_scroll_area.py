from PySide6.QtWidgets import QScrollArea
from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Property, QEvent


class ElasticScrollArea(QScrollArea):
    """A QScrollArea with a purely-visual iOS-style rubber-band overscroll
    bounce: keep scrolling past the top/bottom and the content stretches a
    little before springing back, instead of stopping dead.

    This never touches the actual scroll position/value or what content is
    shown -- it only nudges the viewport's margins by a temporary offset
    while wheel input keeps arriving at a boundary (viewport margins are a
    mechanism Qt expects external code to drive, unlike the content
    widget's own position, which QScrollArea re-asserts on its own the
    moment anything else nudges it -- moving the widget directly was tried
    first and silently got overridden on the very next event), then
    animates that offset back to 0 with a springy easing curve once input
    stops. Purely cosmetic, same as this session's button-flash feedback.

    Reusable on purpose -- used for both the feed screens and the Messages
    chat view instead of duplicating this per screen.
    """

    MAX_OVERSCROLL = 36  # px, how far the content can visibly stretch
    PX_PER_NOTCH = 8  # how much one wheel "notch" (120 angleDelta units) nudges it
    SETTLE_DELAY_MS = 180  # no further overscroll input for this long -> spring back
    SPRING_DURATION_MS = 280

    def __init__(self, parent=None):
        super().__init__(parent)
        self._offset = 0.0
        self._anim = None

        self._settle_timer = QTimer(self)
        self._settle_timer.setSingleShot(True)
        self._settle_timer.setInterval(self.SETTLE_DELAY_MS)
        self._settle_timer.timeout.connect(self._spring_back)

        # Wheel events land on the viewport, not the QScrollArea itself.
        self.viewport().installEventFilter(self)

    def _get_offset(self):
        return self._offset

    def _set_offset(self, value):
        self._offset = value
        # Positive value = pulled past the top -> push the viewport down
        # (top margin), revealing a gap above the content, like it's being
        # stretched off its anchored top edge. Negative = pulled past the
        # bottom -> same idea, bottom margin.
        top = max(0, int(round(value)))
        bottom = max(0, int(round(-value)))
        self.setViewportMargins(0, top, 0, bottom)
        # The top case moves the viewport (new position -> Qt naturally
        # repaints the freed region above it). The bottom case only
        # resizes it in place (same top-left origin, just shorter) -- a
        # plain resize-without-move can leave stale backing-store pixels
        # in the newly-freed strip below it on some platforms/themes
        # instead of properly repainting it, which reads as a visible
        # "square" artifact there instead of a clean gap (reported via
        # manual testing on a real display; couldn't be reproduced in this
        # sandbox's offscreen renderer to confirm directly). Forcing a full
        # repaint here covers that gap either way.
        self.update()

    overscrollOffset = Property(float, _get_offset, _set_offset)

    def eventFilter(self, obj, event):
        if obj is self.viewport() and event.type() == QEvent.Type.Wheel:
            if self._maybe_overscroll(event):
                return True
        return super().eventFilter(obj, event)

    def _maybe_overscroll(self, event):
        delta = event.angleDelta().y()

        if self._offset == 0:
            # Only consult the *live* scrollbar to decide whether a NEW
            # overscroll gesture is starting. Once one is underway, our own
            # setViewportMargins() calls change the viewport's height,
            # which changes the scrollbar's maximum() -- so re-checking
            # bar.value()/bar.maximum() mid-gesture would see state we
            # perturbed ourselves (this is what caused the bottom bounce to
            # cut itself short while the top one didn't: shrinking the
            # viewport grows maximum(), which can make value() >=
            # maximum() flip false even though the user kept scrolling the
            # same direction).
            bar = self.verticalScrollBar()
            at_top = bar.value() <= bar.minimum()
            at_bottom = bar.value() >= bar.maximum()
            overscrolling = (delta > 0 and at_top) or (delta < 0 and at_bottom)
            if not overscrolling:
                return False
        else:
            # Gesture already underway -- keep going only while the wheel
            # keeps pushing the same direction it started in.
            same_direction = (self._offset > 0 and delta > 0) or (self._offset < 0 and delta < 0)
            if not same_direction:
                self._spring_back()
                return False

        if self._anim is not None:
            self._anim.stop()
            self._anim = None

        step = (delta / 120.0) * self.PX_PER_NOTCH
        new_offset = max(-self.MAX_OVERSCROLL, min(self.MAX_OVERSCROLL, self._offset + step))
        self._set_offset(new_offset)
        self._settle_timer.start()
        return True

    def _spring_back(self):
        if self._offset == 0:
            return
        self._anim = QPropertyAnimation(self, b"overscrollOffset", self)
        self._anim.setDuration(self.SPRING_DURATION_MS)
        self._anim.setStartValue(self._offset)
        self._anim.setEndValue(0.0)
        self._anim.setEasingCurve(QEasingCurve.Type.OutBack)
        self._anim.start()
