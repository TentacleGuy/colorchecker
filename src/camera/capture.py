"""Kamera Capture & MJPEG Streaming.

Verwendet OpenCV. Auf Raspberry Pi mit libcamera-Stack ggf. `opencv-python` nutzt v4l2.
Falls keine Kamera verfügbar ist, werden Dummy Frames erzeugt.
"""
from __future__ import annotations

import cv2  # type: ignore
import time
import threading
import logging
from typing import Generator, Optional

log = logging.getLogger("colorchecker.camera")

_capture_lock = threading.Lock()
_cap: Optional[cv2.VideoCapture] = None

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
JPEG_QUALITY = 80
READ_RETRY_SLEEP = 0.05


def _ensure_capture() -> Optional[cv2.VideoCapture]:
    global _cap
    if _cap is not None and _cap.isOpened():
        return _cap
    with _capture_lock:
        if _cap is None or not _cap.isOpened():
            _cap = cv2.VideoCapture(0)
            if _cap is None or not _cap.isOpened():
                log.warning("Kamera konnte nicht geöffnet werden – Dummy Mode aktiv")
                return None
            _cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            _cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    return _cap


def capture_frame():
    cap = _ensure_capture()
    if cap is None:
        # Dummy Frame (einfarbig grau) als Fallback
        import numpy as np

        return (np.ones((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8) * 128)
    ok, frame = cap.read()
    if not ok or frame is None:
        log.debug("Frame read fehlgeschlagen – retry")
        time.sleep(READ_RETRY_SLEEP)
        return None
    return frame


def _frame_to_jpeg_bytes(frame) -> bytes:
    import numpy as np  # noqa

    ok, buf = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
    if not ok:
        return b""
    return buf.tobytes()


def start_stream() -> Generator[bytes, None, None]:
    """Generator für MJPEG Stream.

    Yields bereits korrekt formatierte multipart frame Chunks.
    """
    while True:
        frame = capture_frame()
        if frame is None:
            continue
        jpeg = _frame_to_jpeg_bytes(frame)
        if not jpeg:
            continue
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Content-Length: " + str(len(jpeg)).encode() + b"\r\n\r\n" + jpeg + b"\r\n"
        )
        # leichte Entlastung
        time.sleep(0.05)