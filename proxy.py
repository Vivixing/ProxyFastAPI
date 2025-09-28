from fastapi import FastAPI, Request
import httpx

app = FastAPI()

# Dirección backend HTTP Servidor Remoto
BACKEND_URL = "http://93.127.213.95:8035"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    url = f"{BACKEND_URL}/{path}"

    # Construir la request original
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, content=body)

    return response.text
