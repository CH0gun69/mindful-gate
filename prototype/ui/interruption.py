from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QTimer

from core.mock_data import (
    glyph_for, icon_path_for, PROTECTION_LEVELS, BREATHING_PHRASES, BREATHING_CYCLE_MS,
)
from ui.widgets.svg_icon import white_svg_pixmap

AVATAR_SIZE = 72


class InterruptionScreen(QWidget):
    continue_clicked = Signal()
    go_back_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("interruptionScreen")
        self._level_cfg = PROTECTION_LEVELS[1]
        self._breathing_index = 0

        # Persistent timers, reused across every set_context() call (this
        # screen instance is shared for every app tap, never recreated) --
        # both stopped/restarted fresh each time so no leftover countdown
        # or breathing-cycle state from a previous app/level can leak into
        # the next.
        self._unlock_timer = QTimer(self)
        self._unlock_timer.setSingleShot(True)
        self._unlock_timer.timeout.connect(self._on_delay_elapsed)

        self._breathing_timer = QTimer(self)
        self._breathing_timer.setInterval(BREATHING_CYCLE_MS)
        self._breathing_timer.timeout.connect(self._cycle_breathing_text)

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

        # Level 3 only: a deliberate reaffirm tap, anchored right under the
        # intention quote it's reaffirming. Hidden until the breathing
        # delay elapses (see _on_delay_elapsed).
        self.reaffirm_btn = QPushButton("Still on purpose?")
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

        # Levels 2/3 only: cycling breathe-in/breathe-out text under the
        # icon while Continue Anyway is locked. Separate label from
        # self.icon so the app-icon avatar is never overwritten.
        self.breathing_label = QLabel("")
        self.breathing_label.setObjectName("breathingText")
        self.breathing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.breathing_label.hide()
        root.addWidget(self.breathing_label)

        root.addStretch(3)

        back_btn = QPushButton("Go Back")
        back_btn.setObjectName("primaryBtn")
        back_btn.clicked.connect(lambda: self.go_back_clicked.emit())
        root.addWidget(back_btn)

        self.continue_btn = QPushButton("Continue Anyway")
        self.continue_btn.setObjectName("secondaryBtn")
        self.continue_btn.clicked.connect(lambda: self.continue_clicked.emit())
        root.addWidget(self.continue_btn)

    def set_context(self, app_name: str, intention: str, level: int = 1):
        # --- full reset first: this screen instance is reused across
        # every trigger, so nothing from a previous app/level may survive.
        self._unlock_timer.stop()
        self._breathing_timer.stop()
        self._breathing_index = 0
        self.breathing_label.setText("")
        self.breathing_label.hide()
        self.reaffirm_btn.hide()

        self.app_label.setText(f"You opened {app_name}.")
        self.intention_label.setText(f"“{intention}”")

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
        if self._level_cfg["breathing"]:
            self.breathing_label.setText(BREATHING_PHRASES[0])
            self.breathing_label.show()
            self._breathing_timer.start()
        self._unlock_timer.start(self._level_cfg["delay"] * 1000)

    def _cycle_breathing_text(self):
        self._breathing_index = (self._breathing_index + 1) % len(BREATHING_PHRASES)
        self.breathing_label.setText(BREATHING_PHRASES[self._breathing_index])

    def _on_delay_elapsed(self):
        self._breathing_timer.stop()
        if self._level_cfg["reaffirm"]:
            self.reaffirm_btn.show()
        else:
            self.continue_btn.setEnabled(True)

    def _on_reaffirm_clicked(self):
        self.reaffirm_btn.hide()
        self.continue_btn.setEnabled(True)

    def stop_timers(self):
        """Defensive stop for when the screen is navigated away from
        (continue/go-back) mid-countdown -- a hidden widget's QTimer keeps
        firing otherwise, since Qt doesn't pause timers just because their
        owning widget isn't the visible one in a QStackedWidget."""
        self._unlock_timer.stop()
        self._breathing_timer.stop()
