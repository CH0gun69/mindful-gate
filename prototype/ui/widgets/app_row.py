from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel


class AppRow(QFrame):
    def __init__(self, app):
        super().__init__()
        self.setObjectName("appRow")
        layout = QHBoxLayout(self)
        name = QLabel(app["name"])
        name.setObjectName("appName")
        time = QLabel(app["time"])
        time.setObjectName("appTime")
        layout.addWidget(name)
        if app["protected"]:
            badge = QLabel("Protected")
            badge.setObjectName("badge")
            layout.addWidget(badge)
        layout.addStretch()
        layout.addWidget(time)
