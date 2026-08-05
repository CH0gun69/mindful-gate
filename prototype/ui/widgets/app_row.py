from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel


class AppRow(QFrame):
    """One row in Dashboard's "Top apps" list. `protected` is passed in
    explicitly by the caller (rather than read off app["protected"]) so the
    badge always reflects whatever the current live protected-apps state is,
    not a static mock_data default that can go stale after Setup changes it."""

    def __init__(self, app, protected):
        super().__init__()
        self.setObjectName("appRow")
        layout = QHBoxLayout(self)
        name = QLabel(app["name"])
        name.setObjectName("appName")
        time = QLabel(app["time"])
        time.setObjectName("appTime")
        layout.addWidget(name)
        if protected:
            badge = QLabel("Protected")
            badge.setObjectName("badge")
            layout.addWidget(badge)
        layout.addStretch()
        layout.addWidget(time)
