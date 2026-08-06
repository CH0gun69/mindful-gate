from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt, Signal, QTimer

from core.mock_data import (
    glyph_for, icon_path_for, style_for,
    mock_image_path, mock_image_index_for, feed_actions_for,
    MOCK_FEED_POSTS, MOCK_SHORTS_CAPTION, MOCK_CONTACTS, MOCK_CHAT,
)
from ui.widgets.svg_icon import white_svg_pixmap
from ui.widgets.image_utils import cover_pixmap
from ui.widgets.elastic_scroll_area import ElasticScrollArea


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

    def _wrap_in_scroll_area(self, content, object_name):
        """Wrap content in an ElasticScrollArea so it scrolls (with a
        cosmetic iOS-style rubber-band bounce at the ends) when it
        overflows the visible window instead of clipping or forcing the
        window itself to grow -- setWidgetResizable(True) is what makes
        content stay full-width and only ever grow in height, and content
        inside a scroll area's viewport doesn't propagate its natural size
        upward as a minimum-size constraint on the window the way an
        unwrapped widget would. Used by the feed style and the messages
        chat view; shorts stays single-item/full-bleed, so it's never
        wrapped."""
        scroll = ElasticScrollArea()
        scroll.setObjectName(object_name)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(content)
        return scroll

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
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        for i, (username, caption) in enumerate(MOCK_FEED_POSTS):
            image_index = mock_image_index_for(name, offset=i)
            layout.addWidget(self._build_feed_post(username, caption, color, image_index, name))

        layout.addStretch()
        return self._wrap_in_scroll_area(inner, "feedScrollArea")

    def _build_feed_post(self, username, caption, color, image_index, app_name):
        """One post card. Reddit's config asks for a genuinely different
        layout (a vertical vote rail on the left instead of a bottom action
        row, matching how Reddit actually looks) rather than just different
        icons, so it branches to a distinct structure here -- everything
        else (header/photo/caption) is still built by the same shared
        helpers either way."""
        actions_config = feed_actions_for(app_name)
        if actions_config["layout"] == "vote":
            return self._build_reddit_post(username, caption, color, image_index, actions_config)

        card = QFrame()
        card.setObjectName("feedPostCard")
        v = QVBoxLayout(card)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        v.addLayout(self._build_feed_header(username, color))
        v.addWidget(self._build_feed_photo(image_index))
        v.addWidget(self._build_feed_caption(username, caption))
        v.addWidget(self._build_feed_actions(actions_config))

        return card

    def _build_feed_header(self, username, color):
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
        return header

    def _build_feed_photo(self, image_index):
        photo = QLabel()
        photo.setObjectName("feedPhoto")
        photo.setFixedHeight(160)
        photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_path = mock_image_path(image_index)
        if image_path:
            photo.setPixmap(cover_pixmap(image_path, 400, 160))
        return photo

    def _build_feed_caption(self, username, caption):
        cap = QLabel(f"{username} {caption}")
        cap.setObjectName("feedCaption")
        cap.setWordWrap(True)
        cap.setContentsMargins(10, 8, 10, 10)
        return cap

    # --- action-button row: one shared entry point, branching on layout ---

    def _build_feed_actions(self, config):
        if config["layout"] == "labeled":
            return self._build_actions_labeled(config["buttons"])
        return self._build_actions_icons(config["buttons"], small=config.get("size") == "small")

    def _build_actions_icons(self, buttons, small=False):
        """Instagram/X's style: evenly-spaced icon-only buttons, no labels."""
        row = QFrame()
        row.setObjectName("feedActionsIcons")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(10, 4, 10, 8)
        layout.setSpacing(0)

        layout.addStretch()
        for btn_cfg in buttons:
            btn = self._make_action_button(
                btn_cfg["icon"], "feedActionIconSmall" if small else "feedActionIcon",
                btn_cfg.get("flash"),
            )
            layout.addWidget(btn)
            layout.addStretch()

        return row

    def _build_actions_labeled(self, buttons):
        """Facebook's style: full-width text-label buttons, thin dividers
        between them, one shared icon+label per button."""
        row = QFrame()
        row.setObjectName("feedActionsLabeled")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(0)

        for i, btn_cfg in enumerate(buttons):
            if i > 0:
                divider = QFrame()
                divider.setObjectName("feedActionDivider")
                divider.setFixedWidth(1)
                layout.addWidget(divider)
            btn = self._make_action_button(
                f"{btn_cfg['icon']}  {btn_cfg['label']}", "feedActionLabeled",
                btn_cfg.get("flash"),
            )
            layout.addWidget(btn, 1)

        return row

    def _build_reddit_post(self, username, caption, color, image_index, config):
        """Reddit's post shape: a vertical vote cluster on the left instead
        of a bottom action row, with comment count shown separately below
        the caption -- matches how Reddit's real layout actually differs
        from the other three, not just its colors/icons."""
        card = QFrame()
        card.setObjectName("feedPostCard")
        h = QHBoxLayout(card)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        h.addWidget(self._build_vote_cluster(config))

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addLayout(self._build_feed_header(username, color))
        content_layout.addWidget(self._build_feed_photo(image_index))
        content_layout.addWidget(self._build_feed_caption(username, caption))

        comment_count = QLabel(f"💬  {config['comment_count']}")
        comment_count.setObjectName("feedCommentCount")
        comment_count.setContentsMargins(10, 0, 10, 8)
        content_layout.addWidget(comment_count)

        h.addWidget(content, 1)

        return card

    def _build_vote_cluster(self, config):
        cluster = QFrame()
        cluster.setObjectName("voteCluster")
        layout = QVBoxLayout(cluster)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        up = self._make_action_button("▲", "voteArrowUp", config.get("upvote_flash"))
        layout.addWidget(up, alignment=Qt.AlignmentFlag.AlignCenter)

        count = QLabel(config["vote_count"])
        count.setObjectName("voteCount")
        count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(count)

        down = self._make_action_button("▼", "voteArrowDown", config.get("downvote_flash"))
        layout.addWidget(down, alignment=Qt.AlignmentFlag.AlignCenter)

        return cluster

    def _make_action_button(self, text, object_name, flash_color):
        btn = QPushButton(text)
        btn.setObjectName(object_name)
        btn.setFlat(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if flash_color:
            btn.clicked.connect(
                lambda checked=False, b=btn, c=flash_color: self._flash_button(b, c)
            )
        return btn

    # Reddit's vote arrows kept the simpler text-color-only flash rather
    # than the background pill used everywhere else -- compared both live
    # and preferred the plain look here specifically.
    _COLOR_ONLY_FLASH = {"voteArrowUp", "voteArrowDown"}

    def _flash_button(self, btn, color):
        """Cosmetic-only press feedback: briefly recolor the button on
        click, then revert -- e.g. Instagram's heart flashing red, Reddit's
        arrow highlighting orange. No real like/vote/etc. state is tracked
        or persisted anywhere; this is purely a "yep, that registered"
        visual cue, same as every other screen's placeholder content.
        Applied as an instance-level stylesheet override (not a shared QSS
        rule) since buttons sharing one object name -- e.g. X's 4 icons --
        each need their own different flash color.

        Most buttons get a text-color change AND a translucent background
        pill -- color emoji glyphs (💬, 🔖, 👍) are rendered through the
        system's color-emoji font as multi-color glyphs with their own
        embedded color data, so `color:` alone has no visible effect on
        them (confirmed by manual testing: plain-symbol buttons like
        ♡/➤ flashed fine with color alone, every emoji-led one didn't).
        border-radius is deliberately NOT set here -- it comes from each
        button's own QSS rule instead (a fixed circle for icon buttons,
        so the pill doesn't crop unevenly around each glyph's own
        inconsistent rendered bounding box; keeps Facebook's already-fine
        rounded-rect look as-is)."""
        if btn.objectName() in self._COLOR_ONLY_FLASH:
            btn.setStyleSheet(f"color: {color};")
        else:
            r, g, b = (int(color[i:i+2], 16) for i in (1, 3, 5))
            btn.setStyleSheet(f"color: {color}; background-color: rgba({r}, {g}, {b}, 60);")
        QTimer.singleShot(450, lambda: btn.setStyleSheet(""))

    # ===== "shorts" style: TikTok / YouTube =====

    # TikTok and YouTube happen to land on the same MOCK_IMAGES bucket via
    # mock_image_index_for()'s general-purpose hash (confirmed via manual
    # testing -- both apps showed the identical photo). Shorts only ever
    # has these two apps, so just guarantee they differ explicitly here
    # rather than reworking the general hash (which needs to keep working
    # well for the feed style's many distinct per-post indices).
    SHORTS_IMAGE_OFFSET = {"TikTok": 0, "YouTube": 3}

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
        offset = self.SHORTS_IMAGE_OFFSET.get(name, 0)
        image_path = mock_image_path(mock_image_index_for(name, offset=offset))
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
        inner = QWidget()
        inner.setObjectName("messagesChatView")
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        for sender, text in MOCK_CHAT:
            layout.addWidget(self._build_chat_bubble(sender, text))
        layout.addStretch()

        return self._wrap_in_scroll_area(inner, "messagesChatScrollArea")

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
