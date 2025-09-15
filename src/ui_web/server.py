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
try:
    from fastapi.templating import Jinja2Templates  # type: ignore
except Exception:  # pragma: no cover
    Jinja2Templates = None  # type: ignore
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
if Jinja2Templates:
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
else:
    templates = None  # type: ignore
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
    if not templates:
                fallback_html = """
                <html lang='de'>
                <head>
                        <meta charset='utf-8'>
                        <title>ColorChecker (Fallback)</title>
                        <style>
                                body{font-family:Arial,sans-serif;margin:1rem;background:#f4f4f4;color:#222}
                                h1{margin-top:0}
                                .stream-wrapper{max-width:640px;position:relative;margin-bottom:.5rem}
                                .stream-aspect{position:relative;width:100%;background:#000;border:1px solid #222;border-radius:4px;overflow:hidden;aspect-ratio:4/3;display:flex;align-items:center;justify-content:center}
                                #video-stream{width:100%;height:100%;object-fit:cover;display:block}
                                #stream-overlay{position:absolute;inset:0;background:rgba(0,0,0,.55);color:#fff;font-size:.95rem;display:flex;align-items:center;justify-content:center;text-align:center;padding:.5rem}
                                #stream-overlay.hidden{display:none}
                                .stream-actions{display:flex;gap:.5rem;margin-bottom:.5rem}
                                button{background:#35424a;color:#fff;border:none;padding:.6rem 1rem;border-radius:4px;cursor:pointer;font-size:.85rem}
                                button:hover{background:#47606a}
                                .hint{font-size:.75rem;color:#555;max-width:640px}
                        </style>
                        <script>
                        document.addEventListener('DOMContentLoaded',()=>{
                                const img=document.getElementById('video-stream');
                                const overlay=document.getElementById('stream-overlay');
                                const reloadBtn=document.getElementById('reload-stream');
                                function show(msg){overlay.textContent=msg;overlay.classList.remove('hidden');}
                                function hide(){overlay.classList.add('hidden');}
                                function reload(force){show('Lade Stream...');img.src='/stream'+(force?'?t='+Date.now():'');}
                                if(reloadBtn){reloadBtn.addEventListener('click',()=>reload(true));}
                                if(img){img.addEventListener('error',()=>{show('Fehler beim Stream. Neuer Versuch...');setTimeout(()=>reload(true),2000);});}
                                show('Verbinde zum Kamera-Stream...');
                        });
                        </script>
                </head>
                <body>
                        <h1>ColorChecker (Fallback)</h1>
                        <p>Templates nicht verfügbar (jinja2 fehlt).</p>
                        <div class='stream-wrapper'>
                            <div class='stream-aspect'>
                                <img id='video-stream' src='/stream' alt='Live Kamera Stream' />
                                <div id='stream-overlay'>Initialisiere...</div>
                            </div>
                        </div>
                        <div class='stream-actions'>
                            <button id='reload-stream' type='button'>Reload Stream</button>
                        </div>
                        <p class='hint'>Diese vereinfachte Ansicht wird angezeigt, weil die Template Engine nicht installiert ist.</p>
                </body>
                </html>
                """
                return HTMLResponse(fallback_html)
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy"}


# Kein __main__ Block: Start via uvicorn (CLI oder programmatic in main.py)