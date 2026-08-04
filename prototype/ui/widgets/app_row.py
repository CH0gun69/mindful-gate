from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel


class AppRow(QFrame):
    def __init__(self, app):
        super().__init__()
        self.setObjectName("appRow")
        layout = QHBoxLayout(self)
        name = QLabel(app["name"])
        name.setObjectName("appName")
        badge = QLabel("Protected" if app["protected"] else "")
        badge.setObjectName("badge")
        time = QLabel(app["time"])
        time.setObjectName("appTime")
        layout.addWidget(name)
        layout.addWidget(badge)
        layout.addStretch()
        layout.addWidget(time)
