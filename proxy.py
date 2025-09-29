from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import httpx

app = FastAPI()

origins = ["https://outfitforyou.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dirección backend HTTP Servidor Remoto
BACKEND_URL = "http://127.0.0.1:8000"
#"http://93.127.213.95:8035"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    url = f"{BACKEND_URL}/{path}"

    # Construir la request original
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient(timeout=95.0) as client:
        response = await client.request(method, url, headers=headers, content=body)
    
    print("Respuesta proxy:", response.text)
    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))
