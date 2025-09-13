"""Processing Pipeline für ColorChecker.

Zentrale Schnittstelle für: capture → preprocess → convert → match
Aktuell Platzhalter; reale Implementierungen in preprocessing.py, converter.py, matcher.py ergänzen.
"""
from __future__ import annotations
from typing import Any, Dict, List

try:  # placeholder imports
    from camera.capture import capture_frame
except Exception:  # pragma: no cover
    def capture_frame():  # type: ignore
        return None

try:
    from processing import preprocessing, converter, matcher
except Exception:  # pragma: no cover
    preprocessing = converter = matcher = None  # type: ignore


class PipelineResult(dict):
    @classmethod
    def empty(cls) -> "PipelineResult":
        return cls(status="empty")


def capture_and_match() -> PipelineResult:
    frame = capture_frame()
    if frame is None:
        return PipelineResult.empty()
    # TODO: preprocess
    # TODO: color conversion
    # TODO: load reference db and match
    return PipelineResult(status="ok", matches=[], meta={})
