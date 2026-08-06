# Images

Local placeholder photos used as mock feed/shorts thumbnails on the Fake App screen —
static files, downloaded once and committed, never fetched over the network at
runtime (this needs to work fully offline).

Source: [Picsum Photos](https://picsum.photos/) (`picsum.photos`), which serves
photos licensed for free use (sourced from Unsplash, itself CC0/Unsplash-License).
Downloaded at higher resolution then resized to ~560px on the long edge and
JPEG-compressed locally (each file kept under 100 KB, ~730 KB total) — the originals
were not committed.

Manually reviewed to exclude anything with a real identifiable person, since these
are just mock content for a demo, not attributed editorial photos.

Used by `core/mock_data.mock_image_path()` / `mock_image_index_for()`, consumed by
`ui/fake_app_screen.py`'s "feed" and "shorts" mock layouts.
