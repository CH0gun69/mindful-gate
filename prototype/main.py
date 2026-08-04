import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from ui.phone_home import PhoneHomeScreen
from ui.dashboard import DashboardScreen
from ui.intention_setup import IntentionSetupScreen
from ui.interruption import InterruptionScreen
from ui.insights import InsightsScreen

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

        self.phone_home = PhoneHomeScreen()
        self.dashboard = DashboardScreen()
        self.setup = IntentionSetupScreen()
        self.interruption = InterruptionScreen()
        self.insights = InsightsScreen()

        for screen in (self.phone_home, self.dashboard, self.setup, self.interruption, self.insights):
            self.stack.addWidget(screen)

        self._wire_navigation()
        self.stack.setCurrentWidget(self.phone_home)

    def _wire_navigation(self):
        self.phone_home.app_opened.connect(self._trigger_interruption)

        self.dashboard.go_to_setup.connect(lambda: self.stack.setCurrentWidget(self.setup))
        self.dashboard.go_to_insights.connect(lambda: self.stack.setCurrentWidget(self.insights))
        self.dashboard.simulate_open.connect(self._trigger_interruption)
        self.dashboard.go_home.connect(lambda: self.stack.setCurrentWidget(self.phone_home))

        self.setup.go_back.connect(lambda: self.stack.setCurrentWidget(self.dashboard))
        self.setup.activated.connect(self._on_intention_activated)

        self.interruption.continue_clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard))
        self.interruption.go_back_clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard))

        self.insights.go_back.connect(lambda: self.stack.setCurrentWidget(self.dashboard))

    def _on_intention_activated(self, intention, protected_apps):
        self.current_intention = intention
        self.dashboard.set_focus_active(True, intention)
        self.stack.setCurrentWidget(self.dashboard)

    def _trigger_interruption(self, app_name):
        self.interruption.set_context(app_name, self.current_intention)
        self.stack.setCurrentWidget(self.interruption)


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
