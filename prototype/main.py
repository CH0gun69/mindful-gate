import sys
import os
import argparse

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from ui.phone_home import PhoneHomeScreen
from ui.dashboard import DashboardScreen
from ui.interruption import InterruptionScreen
from ui.protection_customization import ProtectionCustomizationScreen
from ui.fake_app_screen import FakeAppScreen
from core.mock_data import DEFAULT_INTENTION, DEFAULT_PROTECTED_APPS, DEFAULT_APP_PROTECTION_LEVELS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --screen names -> the screen class to build in debug mode.
DEBUG_SCREENS = {
    "phone_home": PhoneHomeScreen,
    "dashboard": DashboardScreen,
    "interruption": InterruptionScreen,
    "protection_customization": ProtectionCustomizationScreen,
    "fake_app": FakeAppScreen,
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mindful-gate — prototype")
        # Fixed, not just an initial size -- a real phone screen doesn't
        # resize either, and letting the window grow/maximize stretched
        # the shorts screen's pre-cropped image disproportionately (caught
        # via manual testing). setFixedSize also disables the maximize
        # control on most window managers.
        self.setFixedSize(390, 780)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.current_intention = "Only reply to messages"
        self.current_app = "Instagram"
        # Single source of truth for which apps currently interrupt — handed
        # to both Phone Home (real tap behavior) and Dashboard (Protected
        # badges) so neither can drift out of sync with Setup.
        self.protected_apps = set(DEFAULT_PROTECTED_APPS)
        # Whether protection is currently active at all -- separate from
        # protected_apps (which apps are chosen) so toggling this off and
        # back on never loses the chosen apps/intention/levels. Defaults
        # True to match the app's previous always-on behavior.
        self.protection_enabled = True
        # Per-app protection level (1/2/3), single source of truth handed
        # to InterruptionScreen (via _trigger_interruption) and kept in
        # sync with ProtectionCustomizationScreen's own display.
        self.app_protection_levels = dict(DEFAULT_APP_PROTECTION_LEVELS)

        self.phone_home = PhoneHomeScreen(protected_apps=self.protected_apps)
        self.dashboard = DashboardScreen(protected_apps=self.protected_apps)
        self.interruption = InterruptionScreen()
        self.protection_screen = ProtectionCustomizationScreen()
        self.fake_app = FakeAppScreen()

        for screen in (
            self.phone_home, self.dashboard,
            self.interruption, self.protection_screen, self.fake_app,
        ):
            self.stack.addWidget(screen)

        self._wire_navigation()
        self.stack.setCurrentWidget(self.phone_home)

    def _wire_navigation(self):
        self.phone_home.app_tapped.connect(self._on_phone_home_app_tapped)
        self.phone_home.open_dashboard.connect(lambda: self.stack.setCurrentWidget(self.dashboard))

        # "Activate/Deactivate Focus Mode" toggles protection_enabled in
        # place, staying on Dashboard -- it reuses whatever apps/intention/
        # levels are already configured. "Set your intention" is the
        # separate action that navigates to the merged screen to change
        # those.
        self.dashboard.focus_toggled.connect(self._on_focus_toggled)
        self.dashboard.go_to_protection.connect(self._on_open_protection_screen)
        self.dashboard.go_home.connect(lambda: self.stack.setCurrentWidget(self.phone_home))

        self.protection_screen.protection_toggled.connect(self._on_protection_toggled)
        self.protection_screen.go_back.connect(lambda: self.stack.setCurrentWidget(self.dashboard))
        self.protection_screen.level_changed.connect(self._on_level_changed)

        self.interruption.continue_clicked.connect(self._on_interruption_continue)
        self.interruption.go_back_clicked.connect(self._on_interruption_go_back)

        self.fake_app.go_back.connect(lambda: self.stack.setCurrentWidget(self.phone_home))

    def _on_open_protection_screen(self):
        # Sync the toggle's visual state to reality every time this screen
        # is entered -- otherwise it'd visually desync from
        # protection_enabled, and the next tap would flip it the wrong way.
        self.protection_screen.set_enabled_state(self.protection_enabled)
        self.stack.setCurrentWidget(self.protection_screen)

    def _on_focus_toggled(self):
        # Dashboard's button only ever flips the on/off state -- WHICH
        # apps/levels/intention stay exactly as last configured (never
        # touched here), same "protection_enabled is separate from the
        # configuration" split as _on_protection_toggled below.
        self.protection_enabled = not self.protection_enabled
        self.dashboard.set_focus_active(self.protection_enabled)

    def _on_protection_toggled(self, enabled, intention, protected_apps):
        self.protection_enabled = enabled
        self.current_intention = intention
        self.protected_apps = set(protected_apps)
        self.phone_home.set_protected_apps(self.protected_apps)
        self.dashboard.set_protected_apps(self.protected_apps)
        self.dashboard.set_focus_active(enabled)
        self.stack.setCurrentWidget(self.dashboard)

    def _on_level_changed(self, app_name, level):
        self.app_protection_levels[app_name] = level

    def _on_phone_home_app_tapped(self, app_name, protected):
        if protected and self.protection_enabled:
            self._trigger_interruption(app_name)
        else:
            self._open_fake_app(app_name)

    def _trigger_interruption(self, app_name):
        self.current_app = app_name
        level = self.app_protection_levels.get(app_name, 1)
        self.interruption.set_context(app_name, self.current_intention, level)
        self.stack.setCurrentWidget(self.interruption)

    def _on_interruption_continue(self):
        self.interruption.stop_timers()
        self._open_fake_app(self.current_app)

    def _on_interruption_go_back(self):
        self.interruption.stop_timers()
        self.stack.setCurrentWidget(self.phone_home)

    def _open_fake_app(self, app_name):
        self.fake_app.set_app(app_name)
        self.stack.setCurrentWidget(self.fake_app)


class DebugWindow(QMainWindow):
    """Launches a single screen in isolation for visual QA — same window
    size/stylesheet as the real app, but skips the rest of the stack and
    all navigation wiring."""

    def __init__(self, screen_name, app_name, level=1):
        super().__init__()
        self.setWindowTitle(f"mindful-gate — DEBUG: {screen_name}")
        self.setFixedSize(390, 780)  # same reasoning as MainWindow

        screen = DEBUG_SCREENS[screen_name]()

        # Screens that need data to render meaningfully get populated with
        # sensible mock values so they don't show up empty/broken.
        # protection_customization needs nothing extra -- it seeds its own
        # rows from PROTECTABLE_APPS/DEFAULT_PROTECTED_APPS/
        # DEFAULT_APP_PROTECTION_LEVELS internally.
        if screen_name == "interruption":
            screen.set_context(app_name, DEFAULT_INTENTION, level=level)
        elif screen_name == "fake_app":
            screen.set_app(app_name)

        self.setCentralWidget(screen)


def parse_args():
    parser = argparse.ArgumentParser(description="mindful-gate prototype")
    parser.add_argument(
        "--screen",
        choices=sorted(DEBUG_SCREENS),
        default=None,
        help="Launch directly into a single screen for visual QA, instead of "
             "the normal phone_home-first navigation flow.",
    )
    parser.add_argument(
        "--app",
        default="Instagram",
        help="App name to populate the interruption/fake_app screens with "
             "when used together with --screen (default: Instagram).",
    )
    parser.add_argument(
        "--level",
        type=int,
        default=1,
        choices=[1, 2, 3],
        help="Protection level to populate the interruption screen with in "
             "--screen debug mode (default: 1).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Keep sys.argv[1:] (our own --screen/--app flags) away from QApplication,
    # which otherwise tries to interpret unrecognized arguments itself.
    app = QApplication(sys.argv[:1])

    with open(
        os.path.join(BASE_DIR, "ui", "styles.qss"),
        "r",
        encoding="utf-8"
    ) as f:
        app.setStyleSheet(f.read())

    if args.screen:
        window = DebugWindow(args.screen, args.app, args.level)
    else:
        window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
