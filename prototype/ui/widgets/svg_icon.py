import re

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


def white_svg_pixmap(path, size):
    """Rasterize an SVG (assumed single-color/monochrome, like a Simple
    Icons brand mark) filled white, at size x size px.

    Simple Icons ships path-only SVGs with no explicit fill (defaults to
    black), so we inject fill="white" on the root <svg> tag -- as a CSS
    presentation attribute it cascades to any child <path> that doesn't
    already set its own fill, which is the case for every icon this
    prototype uses. Rendered white (not each brand's own color) so it
    stays visible on every avatar's colored background regardless of hue --
    including apps like X (Twitter) whose brand color is near-black.

    Shared by AppIcon (phone home grid/dock) and FakeAppScreen (its header
    avatar) so both render app icons the same way instead of one of them
    silently staying on the old emoji-only path.
    """
    with open(path, "r", encoding="utf-8") as f:
        svg_text = f.read()
    svg_text = re.sub(r'\sfill="[^"]*"', "", svg_text)
    svg_text = svg_text.replace("<svg ", '<svg fill="white" ', 1)

    renderer = QSvgRenderer(QByteArray(svg_text.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap
