import os
import tempfile
import shutil

import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)

from transcriber import Transcriber

app = FastAPI(title="Whisper-Medium API")
model = Transcriber()


@app.get("/health")
async def health_check():
    """Return service status and detected hardware."""
    return JSONResponse(content={
        "status": "ok",
        "hardware": model.get_device_info(),
    })


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Receive an audio file and return its transcription as JSON."""
    tmp_path = None
    try:
        suffix = os.path.splitext(file.filename or ".wav")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        text = model.transcribe(tmp_path)
        return JSONResponse(content={"transcription": text})

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
