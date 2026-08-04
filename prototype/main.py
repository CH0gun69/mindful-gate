import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from ui.phone_home import PhoneHomeScreen
from ui.dashboard import DashboardScreen
from ui.intention_setup import IntentionSetupScreen
from ui.interruption import InterruptionScreen
from ui.insights import InsightsScreen
from ui.fake_app_screen import FakeAppScreen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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


def main():
    app = QApplication(sys.argv)

    with open(
        os.path.join(BASE_DIR, "ui", "styles.qss"),
        "r",
        encoding="utf-8"
    ) as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
