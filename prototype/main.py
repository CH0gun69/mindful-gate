import sys
import os
import argparse

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from ui.phone_home import PhoneHomeScreen
from ui.dashboard import DashboardScreen
from ui.intention_setup import IntentionSetupScreen
from ui.interruption import InterruptionScreen
from ui.insights import InsightsScreen
from ui.fake_app_screen import FakeAppScreen
from core.mock_data import DEFAULT_INTENTION

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --screen names -> the screen class to build in debug mode.
DEBUG_SCREENS = {
    "phone_home": PhoneHomeScreen,
    "dashboard": DashboardScreen,
    "setup": IntentionSetupScreen,
    "interruption": InterruptionScreen,
    "insights": InsightsScreen,
    "fake_app": FakeAppScreen,
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mindful-gate — prototype")
        self.resize(390, 780)  # roughly phone-shaped for the demo

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.current_intention = "Only reply to messages"
        self.current_app = "Instagram"
        # Which screen triggered the interruption, so Continue/Go Back know
        # where to return to: "phone_home" -> fake app screen / phone home,
        # "dashboard" -> back to the Dashboard (existing simulate-button flow).
        self._interruption_source = "dashboard"

        self.phone_home = PhoneHomeScreen()
        self.dashboard = DashboardScreen()
        self.setup = IntentionSetupScreen()
        self.interruption = InterruptionScreen()
        self.insights = InsightsScreen()
        self.fake_app = FakeAppScreen()

        for screen in (
            self.phone_home, self.dashboard, self.setup,
            self.interruption, self.insights, self.fake_app,
        ):
            self.stack.addWidget(screen)

        self._wire_navigation()
        self.stack.setCurrentWidget(self.phone_home)

    def _wire_navigation(self):
        self.phone_home.app_tapped.connect(self._on_phone_home_app_tapped)
        self.phone_home.open_dashboard.connect(lambda: self.stack.setCurrentWidget(self.dashboard))

        self.dashboard.go_to_setup.connect(lambda: self.stack.setCurrentWidget(self.setup))
        self.dashboard.go_to_insights.connect(lambda: self.stack.setCurrentWidget(self.insights))
        self.dashboard.simulate_open.connect(self._trigger_interruption)
        self.dashboard.go_home.connect(lambda: self.stack.setCurrentWidget(self.phone_home))

        self.setup.go_back.connect(lambda: self.stack.setCurrentWidget(self.dashboard))
        self.setup.activated.connect(self._on_intention_activated)

        self.interruption.continue_clicked.connect(self._on_interruption_continue)
        self.interruption.go_back_clicked.connect(self._on_interruption_go_back)

        self.insights.go_back.connect(lambda: self.stack.setCurrentWidget(self.dashboard))

        self.fake_app.go_back.connect(lambda: self.stack.setCurrentWidget(self.phone_home))

    def _on_intention_activated(self, intention, protected_apps):
        self.current_intention = intention
        self.phone_home.set_protected_apps(protected_apps)
        self.dashboard.set_focus_active(True, intention)
        self.stack.setCurrentWidget(self.dashboard)

    def _on_phone_home_app_tapped(self, app_name, protected):
        if protected:
            self._trigger_interruption(app_name, source="phone_home")
        else:
            self._open_fake_app(app_name)

    def _trigger_interruption(self, app_name, source="dashboard"):
        self.current_app = app_name
        self._interruption_source = source
        self.interruption.set_context(app_name, self.current_intention)
        self.stack.setCurrentWidget(self.interruption)

    def _on_interruption_continue(self):
        if self._interruption_source == "phone_home":
            self._open_fake_app(self.current_app)
        else:
            self.stack.setCurrentWidget(self.dashboard)

    def _on_interruption_go_back(self):
        if self._interruption_source == "phone_home":
            self.stack.setCurrentWidget(self.phone_home)
        else:
            self.stack.setCurrentWidget(self.dashboard)

    def _open_fake_app(self, app_name):
        self.fake_app.set_app(app_name)
        self.stack.setCurrentWidget(self.fake_app)


class DebugWindow(QMainWindow):
    """Launches a single screen in isolation for visual QA — same window
    size/stylesheet as the real app, but skips the rest of the stack and
    all navigation wiring."""

    def __init__(self, screen_name, app_name):
        super().__init__()
        self.setWindowTitle(f"mindful-gate — DEBUG: {screen_name}")
        self.resize(390, 780)

        screen = DEBUG_SCREENS[screen_name]()

        # Screens that need data to render meaningfully get populated with
        # sensible mock values so they don't show up empty/broken.
        if screen_name == "interruption":
            screen.set_context(app_name, DEFAULT_INTENTION)
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
        window = DebugWindow(args.screen, args.app)
    else:
        window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
