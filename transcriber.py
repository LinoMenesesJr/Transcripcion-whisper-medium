import logging

import torch
from transformers import pipeline

logger = logging.getLogger(__name__)


class Transcriber:
    """Whisper-medium transcription wrapper with automatic CPU/GPU detection."""

    def __init__(self):
        if not torch.cuda.is_available():
            logger.error("No GPU detected! This service requires an NVIDIA GPU to run.")
            raise RuntimeError("NVIDIA GPU required but not found.")

        self.device = "cuda:0"
        torch_dtype = torch.float16

        gpu_name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        logger.info("GPU detected: %s (%.1f GB VRAM) — using float16", gpu_name, vram)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-medium",
            device=self.device,
            torch_dtype=torch_dtype,
        )
        logger.info("Model loaded on %s", self.device)

    def transcribe(self, audio_path: str) -> str:
        """Transcribe an audio file and return the raw text."""
        result = self.pipe(audio_path)
        return result["text"].strip()

    def get_device_info(self) -> dict:
        """Return hardware information for health-check endpoints."""
        info = {
            "device": self.device,
            "cuda_available": True,
            "gpu_name": torch.cuda.get_device_name(0),
            "vram_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2)
        }
        return info
