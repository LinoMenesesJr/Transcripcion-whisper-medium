# Whisper-Medium API

Microservicio modular que expone una API REST para transcripción de audio usando el modelo **whisper-medium** de OpenAI (vía Hugging Face Transformers). Detecta automáticamente el hardware disponible y funciona tanto en **CPU** como en **GPU (CUDA)**.

## Estructura del proyecto

```text
├── transcriber.py           # Lógica del modelo (clase Transcriber)
├── main.py                  # Servidor FastAPI (/transcribe, /health)
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Imagen con CUDA para GPU
├── docker-compose.yml       # Configuración de Docker Compose (GPU)
└── README.md
```

## Requisitos previos

- **Docker** ≥ 20.10
- **Docker Compose** ≥ 2.0
- *(Solo para GPU)* **NVIDIA Container Toolkit** y drivers CUDA 11.8

## Construcción y ejecución

```bash
docker compose up --build -d
```

### Verificar estado

```bash
# Logs (la primera ejecución descarga el modelo ~1.5 GB)
docker compose logs -f whisper-api

# Health check — muestra el dispositivo detectado (cpu / cuda)
curl http://localhost:5000/health
```

## Uso de la API

### `POST /transcribe`

```bash
curl -X POST http://localhost:5000/transcribe \
  -F "file=@mi_audio.wav"
```

**Respuesta:**

```json
{
  "transcription": "Texto transcrito del audio..."
}
```

### `GET /health`

```bash
curl http://localhost:5000/health
```

**Respuesta (GPU):**

```json
{
  "status": "ok",
  "hardware": {
    "device": "cuda:0",
    "cuda_available": true,
    "gpu_name": "NVIDIA GeForce RTX 3060",
    "vram_gb": 12.0
  }
}
```

## Detener el servicio

```bash
docker compose down
```
