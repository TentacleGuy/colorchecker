"""Einstiegspunkt für ColorChecker.

Startet:
 - Kamera Producer Thread (Platzhalter)
 - FastAPI App (uvicorn)
 - Optional weitere Hintergrundservices (Buttons, OLED etc.)

Kann via systemd mit: /path/.venv/bin/python -m colorchecker.src.main
oder direkt: python -m colorchecker.src.main
"""
from __future__ import annotations
import threading
import time
import signal
import sys
import logging
from typing import Optional

import uvicorn

# Konfiguration (Platzhalter: könnte später settings laden)
HOST = "0.0.0.0"
PORT = 8000
LOG_LEVEL = "info"

shutdown_event = threading.Event()
log = logging.getLogger("colorchecker")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Optionale Kamera-Integration
try:
    from camera.capture import capture_frame
except Exception:  # pragma: no cover
    def capture_frame():  # type: ignore
        return None


def camera_producer_loop():
    log.info("Kamera Thread gestartet (Platzhalter)")
    while not shutdown_event.is_set():
        frame = capture_frame()
        # TODO: Frame → Queue legen
        time.sleep(0.1)  # Platzhalter Frequenz
    log.info("Kamera Thread beendet")


def start_camera_thread() -> threading.Thread:
    t = threading.Thread(target=camera_producer_loop, name="camera-producer", daemon=True)
    t.start()
    return t


def install_signal_handlers():
    def handle(sig, frame):  # pragma: no cover
        log.info("Signal %s empfangen – Shutdown eingeleitet", sig)
        shutdown_event.set()
    for s in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(s, handle)
        except Exception:  # pragma: no cover
            pass


def run_uvicorn():
    from ui_web.server import app  # Lazy import damit Module vorher definierbar
    config = uvicorn.Config(app, host=HOST, port=PORT, log_level=LOG_LEVEL)
    server = uvicorn.Server(config)
    return server.run()


def main():
    log.info("Starte ColorChecker Main (FastAPI @ %s:%s)", HOST, PORT)
    install_signal_handlers()
    cam_thread = start_camera_thread()
    try:
        run_uvicorn()
    finally:
        log.info("Shutdown eingeleitet…")
        shutdown_event.set()
        cam_thread.join(timeout=2)
        log.info("Beendet.")


if __name__ == "__main__":  # pragma: no cover
    sys.exit(0 if main() is None else 0)
