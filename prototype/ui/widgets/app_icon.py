from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize

from ui.widgets.svg_icon import white_svg_pixmap


class AppIcon(QPushButton):
    """A single tappable app icon: rounded avatar + name label underneath.

    Used by the phone home screen grid and dock. The avatar color/glyph is
    supplied by the caller so this stays a dumb, reusable presentation widget —
    same pattern as StatCard. When icon_path is given (a real brand-logo SVG,
    see core.mock_data.icon_path_for), it's rendered white on the colored
    avatar background instead of the text glyph -- apps without a real logo
    (icon_path=None) keep rendering their emoji/letter glyph exactly as before.
    """

    def __init__(self, name, glyph, color, avatar_size=56, icon_path=None):
        super().__init__()
        self.setObjectName("appIcon")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.avatar = QLabel()
        self.avatar.setObjectName("appIconAvatar")
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setFixedSize(avatar_size, avatar_size)
        self.avatar.setStyleSheet(
            f"background-color: {color}; border-radius: {avatar_size // 4}px;"
        )

        if icon_path:
            # Some padding around the mark so it doesn't touch the rounded
            # corners -- real app icons never bleed edge-to-edge either.
            mark_size = int(avatar_size * 0.6)
            self.avatar.setPixmap(white_svg_pixmap(icon_path, mark_size))
        else:
            self.avatar.setText(glyph)
            self.avatar.setStyleSheet(
                self.avatar.styleSheet()
                + f" color: #ffffff; font-size: {avatar_size // 2}px; font-weight: 600;"
            )

        # Let clicks on the avatar/label fall through to this button instead
        # of being swallowed by the child widget under the cursor.
        self.avatar.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.name_label = QLabel(name)
        self.name_label.setObjectName("appIconLabel")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setFixedWidth(avatar_size + 20)
        self.name_label.setWordWrap(True)
        self.name_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(self.name_label)

        # QPushButton.sizeHint() ignores the child layout entirely (it only
        # sizes for the button's own text/icon), which otherwise squashes
        # the layout down to a sliver. Force a size that fits the content.
        self._fixed_size = QSize(avatar_size + 20, avatar_size + 44)
        self.setFixedSize(self._fixed_size)

    def sizeHint(self):
        return self._fixed_size
