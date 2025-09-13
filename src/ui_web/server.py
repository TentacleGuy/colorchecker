"""FastAPI Server für ColorChecker.

Endpoints:
 - GET /stream : MJPEG Stream (multipart/x-mixed-replace)
 - GET /api/settings : Aktuelle Einstellungen
 - POST /api/settings : Einstellungen aktualisieren
 - POST /api/capture : Einzelnes Capture + Matching (Platzhalter)
"""

from typing import Optional, Dict, Any
from fastapi import FastAPI, APIRouter, BackgroundTasks, Request
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import logging
from pydantic import BaseModel

try:  # optionale Imports (Platzhalter-Implementierungen vorhanden?)
    from camera.capture import capture_frame, start_stream
except Exception:  # fallback stub
    def capture_frame():  # type: ignore
        return None

    def start_stream():  # type: ignore
        while True:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + b"" + b"\r\n"

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(title="ColorChecker API", version="0.1.0")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    logging.getLogger("colorchecker").warning("Static-Verzeichnis fehlt: %s", STATIC_DIR)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
router = APIRouter()


class SettingsModel(BaseModel):
    roi: Optional[str] = None
    sample_count: Optional[int] = 5
    led_enabled: Optional[bool] = True


CURRENT_SETTINGS: Dict[str, Any] = {
    "roi": None,
    "sample_count": 5,
    "led_enabled": True,
}


def mjpeg_generator():
    # Erwartet: start_stream liefert bereits JPEG-Frames mit Boundary
    gen = start_stream()
    for chunk in gen:
        yield chunk


@router.get("/stream")
def stream_endpoint():
    return StreamingResponse(
        mjpeg_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.get("/api/settings")
def get_settings():
    return CURRENT_SETTINGS


@router.post("/api/settings")
def update_settings(settings: SettingsModel):
    data = settings.dict(exclude_unset=True)
    CURRENT_SETTINGS.update(data)
    return {"status": "ok", "settings": CURRENT_SETTINGS}


def run_capture_and_match() -> Dict[str, Any]:  # Placeholder bis Pipeline existiert
    frame = capture_frame()
    # TODO: Processing Pipeline einbinden
    if frame is None:
        return {"status": "no_frame"}
    return {"status": "ok", "result": {"matches": [], "meta": {}}}


@router.post("/api/capture")
def capture_endpoint(background: BackgroundTasks):
    # Kurzfristig synchrone Antwort, optional async Verarbeitung
    result = run_capture_and_match()
    return JSONResponse(result)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy"}


# Kein __main__ Block: Start via uvicorn (CLI oder programmatic in main.py)