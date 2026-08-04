import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from screens.dashboard import DashboardScreen
from screens.intention_setup import IntentionSetupScreen
from screens.interruption import InterruptionScreen
from screens.insights import InsightsScreen

STYLESHEET = """
QWidget {
    background-color: #14161a;
    color: #eef0f2;
    font-family: "Segoe UI", "SF Pro Text", sans-serif;
}
QLabel#screenTitle {
    font-size: 24px;
    font-weight: 600;
}
QLabel#bigScreenTime {
    font-size: 44px;
    font-weight: 700;
    color: #8fd3c7;
}
QLabel#caption {
    color: #9aa1ab;
    font-size: 13px;
}
QLabel#sectionLabel {
    font-size: 14px;
    font-weight: 600;
    color: #c9cdd3;
    margin-top: 8px;
}
QFrame#statCard {
    background-color: #1d2026;
    border-radius: 10px;
    padding: 12px;
}
QLabel#statValue {
    font-size: 20px;
    font-weight: 700;
}
QLabel#statLabel {
    color: #9aa1ab;
    font-size: 12px;
}
QFrame#appRow {
    background-color: #1d2026;
    border-radius: 8px;
    padding: 8px;
}
QLabel#appName {
    font-weight: 500;
}
QLabel#badge {
    color: #8fd3c7;
    font-size: 11px;
    margin-left: 8px;
}
QLabel#appTime {
    color: #9aa1ab;
}
QPushButton#primaryBtn {
    background-color: #8fd3c7;
    color: #0e1012;
    border-radius: 10px;
    padding: 12px;
    font-weight: 600;
    font-size: 14px;
}
QPushButton#primaryBtn:hover {
    background-color: #a3ded3;
}
QPushButton#secondaryBtn {
    background-color: transparent;
    color: #eef0f2;
    border: 1px solid #3a3f47;
    border-radius: 10px;
    padding: 12px;
    font-size: 14px;
}
QPushButton#linkBtn, QPushButton#simulateBtn {
    background-color: transparent;
    color: #9aa1ab;
    border: none;
    padding: 8px;
    font-size: 13px;
    text-decoration: underline;
}
QLabel#interruptTitle {
    font-size: 18px;
    color: #9aa1ab;
}
QLabel#interruptQuestion {
    font-size: 30px;
    font-weight: 700;
}
QLabel#intentionQuote {
    font-size: 16px;
    font-style: italic;
    color: #8fd3c7;
    padding: 16px;
    background-color: #1d2026;
    border-radius: 10px;
}
QCheckBox {
    font-size: 14px;
    padding: 4px;
}
QLineEdit#intentionInput {
    background-color: #1d2026;
    border: 1px solid #3a3f47;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mindful-gate — prototype")
        self.resize(390, 780)  # roughly phone-shaped for the demo

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.current_intention = "Only reply to messages"
        self.current_app = "Instagram"

        self.dashboard = DashboardScreen()
        self.setup = IntentionSetupScreen()
        self.interruption = InterruptionScreen()
        self.insights = InsightsScreen()

        for screen in (self.dashboard, self.setup, self.interruption, self.insights):
            self.stack.addWidget(screen)

        self._wire_navigation()
        self.stack.setCurrentWidget(self.dashboard)

    def _wire_navigation(self):
        self.dashboard.go_to_setup.connect(lambda: self.stack.setCurrentWidget(self.setup))
        self.dashboard.go_to_insights.connect(lambda: self.stack.setCurrentWidget(self.insights))
        self.dashboard.simulate_open.connect(self._trigger_interruption)

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
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()