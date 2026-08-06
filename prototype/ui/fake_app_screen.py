from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt, Signal

from core.mock_data import (
    glyph_for, icon_path_for, style_for,
    mock_image_path, mock_image_index_for,
    MOCK_FEED_POSTS, MOCK_SHORTS_CAPTION, MOCK_CONTACTS, MOCK_CHAT,
)
from ui.widgets.svg_icon import white_svg_pixmap
from ui.widgets.image_utils import cover_pixmap


class FakeAppScreen(QWidget):
    """A mock "you opened the app" screen, reconfigured per-app via
    set_app() instead of building one bespoke screen per app. Shares one
    header (back button + avatar + title) across every app, then picks one
    of 3 body styles based on core.mock_data.style_for(name):

    - "feed": Instagram/Facebook/X (Twitter)/Reddit -- a short vertical
      feed of post cards (avatar + username, photo, caption). Same card
      layout for all four, just re-skinned per app's own accent color.
    - "shorts": TikTok/YouTube -- one full-bleed vertical photo with a
      caption overlay at the bottom and engagement icons down the right.
    - "messages": Messages -- a contact sidebar + a chat bubble view.

    Everything here is clearly-labeled placeholder content (mock captions,
    invented names, local CC0 stock photos), matching the rest of this
    prototype's hardcoded-mock-data approach -- see assets/images/README.md.
    """

    go_back = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("fakeAppScreen")
        self._body = None
        self._build_ui()

    def _build_ui(self):
        self._root_layout = QVBoxLayout(self)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)
        self._root_layout.addWidget(self._build_header())

    def _build_header(self):
        header = QFrame()
        header.setObjectName("fakeAppHeader")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        back_btn = QPushButton("←")
        back_btn.setObjectName("fakeAppBackBtn")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.go_back.emit())
        layout.addWidget(back_btn)

        self.avatar = QLabel()
        self.avatar.setObjectName("fakeAppAvatar")
        self.avatar.setFixedSize(36, 36)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.avatar)

        self.title = QLabel()
        self.title.setObjectName("fakeAppTitle")
        layout.addWidget(self.title)
        layout.addStretch()

        return header

    def set_app(self, name):
        glyph, color = glyph_for(name)
        self.title.setText(name)

        self.avatar.setStyleSheet(f"background-color: {color}; border-radius: 10px;")
        icon_path = icon_path_for(name)
        if icon_path:
            # setPixmap() clears any previously-set text automatically (and
            # vice versa below) -- QLabel only ever shows one or the other.
            self.avatar.setPixmap(white_svg_pixmap(icon_path, 22))
        else:
            self.avatar.setText(glyph)
            self.avatar.setStyleSheet(
                self.avatar.styleSheet()
                + " color: #ffffff; font-size: 16px; font-weight: 600;"
            )

        if self._body is not None:
            self._root_layout.removeWidget(self._body)
            # setParent(None) detaches (and hides) it immediately --
            # removeWidget() alone only unmanages it from the layout, so
            # without this it stays visible until deleteLater() actually
            # runs on a later event-loop pass. Same bug/fix as
            # DashboardScreen._refresh_legend earlier this session.
            self._body.setParent(None)
            self._body.deleteLater()

        style = style_for(name)
        if style == "shorts":
            self._body = self._build_shorts_body(name)
        elif style == "messages":
            self._body = self._build_messages_body()
        else:
            self._body = self._build_feed_body(name, color)

        self._root_layout.addWidget(self._body, 1)

    # ===== "feed" style: Instagram / Facebook / X (Twitter) / Reddit =====

    def _build_feed_body(self, name, color):
        wrap = QWidget()
        layout = QVBoxLayout(wrap)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        for i, (username, caption) in enumerate(MOCK_FEED_POSTS):
            image_index = mock_image_index_for(name, offset=i)
            layout.addWidget(self._build_feed_post(username, caption, color, image_index))

        layout.addStretch()
        return wrap

    def _build_feed_post(self, username, caption, color, image_index):
        card = QFrame()
        card.setObjectName("feedPostCard")
        v = QVBoxLayout(card)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        header = QHBoxLayout()
        header.setContentsMargins(10, 10, 10, 8)
        header.setSpacing(8)

        avatar = QLabel(username[0].upper())
        avatar.setFixedSize(28, 28)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(
            f"background-color: {color}; border-radius: 14px; "
            "color: #ffffff; font-weight: 600; font-size: 12px;"
        )
        header.addWidget(avatar)

        uname = QLabel(username)
        uname.setObjectName("feedUsername")
        header.addWidget(uname)
        header.addStretch()
        v.addLayout(header)

        photo = QLabel()
        photo.setObjectName("feedPhoto")
        photo.setFixedHeight(160)
        photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_path = mock_image_path(image_index)
        if image_path:
            photo.setPixmap(cover_pixmap(image_path, 400, 160))
        v.addWidget(photo)

        cap = QLabel(f"{username} {caption}")
        cap.setObjectName("feedCaption")
        cap.setWordWrap(True)
        cap.setContentsMargins(10, 8, 10, 10)
        v.addWidget(cap)

        return card

    # ===== "shorts" style: TikTok / YouTube =====

    def _build_shorts_body(self, name):
        wrap = QFrame()
        wrap.setObjectName("shortsWrap")
        grid = QGridLayout(wrap)
        grid.setContentsMargins(0, 0, 0, 0)

        image_label = QLabel()
        image_label.setObjectName("shortsImage")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Expanding + scaledContents so this actually fills the whole
        # screen edge-to-edge (the "full-screen vertical" feel) instead of
        # sitting centered at its pixmap's native size with black bars
        # around it. Pre-cropped to roughly this phone's own content-area
        # aspect ratio so the final stretch-to-fit is barely noticeable.
        image_label.setScaledContents(True)
        image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_path = mock_image_path(mock_image_index_for(name))
        if image_path:
            image_label.setPixmap(cover_pixmap(image_path, 390, 700))
        grid.addWidget(image_label, 0, 0)
        grid.setRowStretch(0, 1)
        grid.setColumnStretch(0, 1)

        caption_bar = QFrame()
        caption_bar.setObjectName("shortsCaptionBar")
        cap_layout = QVBoxLayout(caption_bar)
        cap_layout.setContentsMargins(16, 10, 60, 16)
        cap_layout.setSpacing(4)
        username = QLabel(f"@{name.lower().replace(' ', '').replace('(', '').replace(')', '')}_demo")
        username.setObjectName("shortsUsername")
        caption = QLabel(MOCK_SHORTS_CAPTION)
        caption.setObjectName("shortsCaption")
        caption.setWordWrap(True)
        cap_layout.addWidget(username)
        cap_layout.addWidget(caption)
        # Same cell as image_label -- overlaying two widgets in one
        # QGridLayout cell instead of a separate absolute-positioning
        # mechanism, same trick ClipPortal's ClipCard uses for its
        # content/gradient-overlay stack.
        grid.addWidget(caption_bar, 0, 0, Qt.AlignmentFlag.AlignBottom)
        caption_bar.raise_()

        icons_col = QFrame()
        icons_col.setObjectName("shortsIconsCol")
        icons_layout = QVBoxLayout(icons_col)
        icons_layout.setContentsMargins(8, 8, 12, 40)
        icons_layout.setSpacing(14)
        for icon_glyph, count in (("♥", "24.5K"), ("💬", "312"), ("↗", "1.2K")):
            icon_lbl = QLabel(icon_glyph)
            icon_lbl.setObjectName("shortsEngageIcon")
            icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            count_lbl = QLabel(count)
            count_lbl.setObjectName("shortsEngageCount")
            count_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icons_layout.addWidget(icon_lbl)
            icons_layout.addWidget(count_lbl)
        grid.addWidget(
            icons_col, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )
        icons_col.raise_()

        return wrap

    # ===== "messages" style =====

    def _build_messages_body(self):
        wrap = QWidget()
        h = QHBoxLayout(wrap)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        h.addWidget(self._build_contacts_sidebar())
        h.addWidget(self._build_chat_view(), 1)

        return wrap

    def _build_contacts_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("messagesSidebar")
        sidebar.setFixedWidth(128)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(6, 10, 6, 10)
        layout.setSpacing(4)

        for i, (contact_name, preview) in enumerate(MOCK_CONTACTS):
            row = QFrame()
            row.setObjectName("messagesContactRowActive" if i == 0 else "messagesContactRow")
            row_layout = QVBoxLayout(row)
            row_layout.setContentsMargins(8, 6, 8, 6)
            row_layout.setSpacing(2)

            name_lbl = QLabel(contact_name)
            name_lbl.setObjectName("messagesContactName")
            name_lbl.setWordWrap(True)
            preview_lbl = QLabel(preview)
            preview_lbl.setObjectName("messagesContactPreview")
            preview_lbl.setWordWrap(True)
            row_layout.addWidget(name_lbl)
            row_layout.addWidget(preview_lbl)

            layout.addWidget(row)

        layout.addStretch()
        return sidebar

    def _build_chat_view(self):
        chat_wrap = QWidget()
        chat_wrap.setObjectName("messagesChatView")
        layout = QVBoxLayout(chat_wrap)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        for sender, text in MOCK_CHAT:
            layout.addWidget(self._build_chat_bubble(sender, text))
        layout.addStretch()

        return chat_wrap

    def _build_chat_bubble(self, sender, text):
        is_me = sender == "me"

        bubble = QLabel(text)
        bubble.setObjectName("chatBubbleMe" if is_me else "chatBubbleThem")
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(170)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        if is_me:
            row.addStretch()
            row.addWidget(bubble)
        else:
            row.addWidget(bubble)
            row.addStretch()

        container = QWidget()
        container.setLayout(row)
        return container
