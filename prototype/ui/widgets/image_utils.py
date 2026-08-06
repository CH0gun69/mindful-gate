from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


def cover_pixmap(path, width, height):
    """Load an image and scale+center-crop it to exactly width x height,
    filling the whole box with no distortion and no letterboxing -- the
    same "object-fit: cover" technique browsers use. Used for the Fake App
    screen's feed/shorts mock photos, which come from square source images
    but need to fill rectangular (often portrait) boxes.

    Returns a null QPixmap if the file can't be loaded, so callers can
    treat that the same as no image being available at all.
    """
    pixmap = QPixmap(path)
    if pixmap.isNull():
        return pixmap

    scaled = pixmap.scaled(
        width, height, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation,
    )
    x = max((scaled.width() - width) // 2, 0)
    y = max((scaled.height() - height) // 2, 0)
    return scaled.copy(x, y, width, height)
