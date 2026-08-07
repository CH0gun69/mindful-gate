from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QTimer

from core.mock_data import (
    glyph_for, icon_path_for, PROTECTION_LEVELS, BREATHING_CYCLE_MS,
    time_spent_today_for,
)
from core.strings import t, DEFAULT_LANGUAGE
from ui.widgets.svg_icon import white_svg_pixmap
from ui.widgets.breathing_circle import BreathingCircle

AVATAR_SIZE = 72


class InterruptionScreen(QWidget):
    continue_clicked = Signal()
    go_back_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("interruptionScreen")
        self._level_cfg = PROTECTION_LEVELS[1]
        self._seconds_left = 0
        self._language = DEFAULT_LANGUAGE
        self._current_app = ""  # so set_language can re-render "You opened {app}." mid-flow

        # Persistent timers, reused across every set_context() call (this
        # screen instance is shared for every app tap, never recreated) --
        # both stopped/restarted fresh each time so no leftover countdown
        # state from a previous app/level can leak into the next. The
        # breathing phase itself is driven by BreathingCircle's own
        # internal animation loop, not a QTimer.
        self._unlock_timer = QTimer(self)
        self._unlock_timer.setSingleShot(True)
        self._unlock_timer.timeout.connect(self._on_delay_elapsed)

        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(1000)
        self._countdown_timer.timeout.connect(self._tick_countdown)

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

        self.question_label = QLabel(t("still_on_purpose", self._language))
        self.question_label.setObjectName("interruptQuestion")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.question_label)

        self.intention_label = QLabel()
        self.intention_label.setObjectName("intentionQuote")
        self.intention_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intention_label.setWordWrap(True)
        root.addWidget(self.intention_label)

        # Small, muted "time spent today" nudge -- sourced from
        # core.mock_data.TOP_APPS via time_spent_today_for(), hidden
        # gracefully if the app has no mock usage entry. Understated on
        # purpose: a text line, not a popup or blocking dialog.
        self.time_spent_label = QLabel("")
        self.time_spent_label.setObjectName("timeSpentNote")
        self.time_spent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_spent_label.hide()
        root.addWidget(self.time_spent_label)

        # Level 3 only: a deliberate reaffirm tap, anchored right under the
        # intention quote it's reaffirming. Hidden until the breathing
        # delay elapses (see _on_delay_elapsed).
        self.reaffirm_btn = QPushButton(t("still_on_purpose", self._language))
        self.reaffirm_btn.setObjectName("reaffirmChip")
        self.reaffirm_btn.clicked.connect(self._on_reaffirm_clicked)
        self.reaffirm_btn.hide()
        root.addWidget(self.reaffirm_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        root.addStretch(2)

        self.icon = QLabel()
        self.icon.setObjectName("interruptIcon")
        self.icon.setFixedSize(AVATAR_SIZE, AVATAR_SIZE)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Levels 2/3 only: a wordless pulsing circle under the icon while
        # Continue Anyway is locked -- grows/shrinks in a repeating loop
        # (see BreathingCircle), replacing the old cycling breathe-in/
        # breathe-out text entirely. Separate widget from self.icon so the
        # app-icon avatar is never overwritten.
        self.breathing_circle = BreathingCircle(cycle_ms=BREATHING_CYCLE_MS)
        self.breathing_circle.hide()
        root.addWidget(self.breathing_circle, alignment=Qt.AlignmentFlag.AlignHCenter)

        root.addStretch(3)

        self.back_btn = QPushButton(t("go_back", self._language))
        self.back_btn.setObjectName("primaryBtn")
        self.back_btn.clicked.connect(lambda: self.go_back_clicked.emit())
        root.addWidget(self.back_btn)

        self.continue_btn = QPushButton(t("continue_anyway", self._language))
        self.continue_btn.setObjectName("secondaryBtn")
        self.continue_btn.clicked.connect(lambda: self.continue_clicked.emit())
        root.addWidget(self.continue_btn)

    def set_context(self, app_name: str, intention: str, level: int = 1):
        # --- full reset first: this screen instance is reused across
        # every trigger, so nothing from a previous app/level may survive.
        self._unlock_timer.stop()
        self._countdown_timer.stop()
        self.breathing_circle.stop()  # also resets diameter back to minimum
        self.breathing_circle.hide()
        self.reaffirm_btn.hide()

        self._current_app = app_name
        self.app_label.setText(t("you_opened", self._language).format(app=app_name))
        # The intention/message text is USER INPUT, never translated --
        # same rule as Set Your Intention's message field.
        self.intention_label.setText(f"“{intention}”")

        time_spent = time_spent_today_for(app_name)
        if time_spent:
            self.time_spent_label.setText(
                t("time_spent_nudge", self._language).format(time=time_spent, app=app_name)
            )
            self.time_spent_label.show()
        else:
            self.time_spent_label.hide()

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

        # --- level-driven gating: Continue Anyway starts locked every
        # time, and only Continue Anyway is ever gated -- Go Back stays
        # immediately clickable at every level, always an escape hatch.
        self._level_cfg = PROTECTION_LEVELS.get(level, PROTECTION_LEVELS[1])
        self.continue_btn.setEnabled(False)
        self._seconds_left = self._level_cfg["delay"]
        self._update_continue_text()
        if self._level_cfg["breathing"]:
            self.breathing_circle.show()
            self.breathing_circle.start()
        self._unlock_timer.start(self._level_cfg["delay"] * 1000)
        self._countdown_timer.start()

    def _tick_countdown(self):
        self._seconds_left = max(self._seconds_left - 1, 0)
        self._update_continue_text()
        if self._seconds_left <= 0:
            self._countdown_timer.stop()

    def _update_continue_text(self):
        if self.continue_btn.isEnabled():
            self.continue_btn.setText(t("continue_anyway", self._language))
        else:
            self.continue_btn.setText(
                t("continue_anyway_countdown", self._language).format(seconds=self._seconds_left)
            )

    def _on_delay_elapsed(self):
        self.breathing_circle.stop()
        self._countdown_timer.stop()
        if self._level_cfg["reaffirm"]:
            # Delay's over but still gated -- drop the stale "(0s)" suffix
            # rather than leave a countdown showing next to a button that
            # isn't actually about to unlock on its own.
            self.continue_btn.setText(t("continue_anyway", self._language))
            self.reaffirm_btn.show()
        else:
            self.continue_btn.setEnabled(True)
            self._update_continue_text()

    def _on_reaffirm_clicked(self):
        self.reaffirm_btn.hide()
        self.continue_btn.setEnabled(True)
        self._update_continue_text()

    def set_language(self, lang):
        """Retranslate this screen's own UI copy. The intention/message
        text (self.intention_label) is user input, never translated --
        same rule as Set Your Intention's message field."""
        self._language = lang
        if self._current_app:
            self.app_label.setText(t("you_opened", lang).format(app=self._current_app))
            time_spent = time_spent_today_for(self._current_app)
            if time_spent:
                self.time_spent_label.setText(
                    t("time_spent_nudge", lang).format(time=time_spent, app=self._current_app)
                )
        self.question_label.setText(t("still_on_purpose", lang))
        self.reaffirm_btn.setText(t("still_on_purpose", lang))
        self.back_btn.setText(t("go_back", lang))
        self._update_continue_text()

    def stop_timers(self):
        """Defensive stop for when the screen is navigated away from
        (continue/go-back) mid-countdown -- a hidden widget's QTimer keeps
        firing otherwise, since Qt doesn't pause timers just because their
        owning widget isn't the visible one in a QStackedWidget."""
        self._unlock_timer.stop()
        self._countdown_timer.stop()
        self.breathing_circle.stop()
