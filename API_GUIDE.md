# Guía de Integración — Whisper-Medium API

Esta guía detalla cómo integrar el servicio de transcripción en otros proyectos mediante su API REST.

## 1. Configuración del Servicio
Asegúrate de que el contenedor esté corriendo. Por defecto, el servicio escucha en:
`http://localhost:5000`

## 2. Endpoints Disponibles

### [POST] `/transcribe`
Recibe un archivo de audio y devuelve la transcripción.

- **Content-Type:** `multipart/form-data`
- **Body:**
  - `file`: Archivo de audio (formato `.wav`, `.mp3`, `.m4a`, etc.).
- **Response (200 OK):**
  ```json
  {
    "transcription": "Texto transcrito..."
  }
  ```

### [GET] `/health`
Verifica el estado del servicio y el hardware detectado.

- **Response (200 OK):**
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

---

## 3. Ejemplos de Implementación

### Python (usando `requests`)
```python
import requests

def transcribe_audio(file_path):
    url = "http://localhost:5000/transcribe"
    
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return response.json()["transcription"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Uso
texto = transcribe_audio("mi_grabacion.wav")
print(texto)
```

### JavaScript / Node.js (usando `fetch`)
```javascript
async function transcribeAudio(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/transcribe', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        return data.transcription;
    } else {
        console.error('Error en la transcripción');
    }
}
```

### cURL
```bash
curl -X POST http://localhost:5000/transcribe \
  -F "file=@audio.mp3"
```

---

## 4. Manejo de Errores
El servicio devuelve errores estándar de HTTP:
- `422 Unprocessable Entity`: Falta el archivo en el body o el formato es incorrecto.
- `500 Internal Server Error`: Error al procesar el audio o falla del modelo. La respuesta JSON incluirá el detalle en el campo `detail`.

## 5. Recomendaciones
- **Timeout:** El tiempo de respuesta depende de la duración del audio. Se recomienda configurar un timeout generoso (> 30s) en el cliente.
- **Formatos:** Se recomienda usar `.wav` o `.mp3` para asegurar máxima compatibilidad con el backend (ffmpeg).
