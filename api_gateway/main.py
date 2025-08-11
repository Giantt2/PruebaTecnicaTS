import httpx
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging as log
import websockets

# Se instancia la aplicacion
app = FastAPI()

# URL del microservicio de usuarios
USER_SERVICE_URL = "http://127.0.0.1:8000"
AUTH_SERVICE_URL = "http://127.0.0.1:8002"
WEBSOCKET_SERVICE_URL_GO = "ws://127.0.0.1:8081/ws"

# Configuracion de CORS para el gateway
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- WebSocket ---
@app.websocket("/ws")
async def websocket_proxy(websocket: WebSocket):
    await websocket.accept()
    log.info(f"Cliente WebSocket aceptado desde {websocket.client.host}")

    try:
        # Se realiza la conexion al websocket de Go
        async with websockets.connect(WEBSOCKET_SERVICE_URL_GO) as service_ws:
            log.info("Proxy conectado exitosamente al servicio WebSocket de Go.")

            # Funcion para reenviar mensajes del cliente al servicio
            async def forward_to_service():
                while True:
                    data = await websocket.receive_text()
                    await service_ws.send(data)
            
            # Funcion para reenviar mensajes del servicio al cliente
            async def forward_to_client():
                while True:
                    data = await service_ws.recv()
                    await websocket.send_text(data)

            # Se ejecutan ambas tareas
            import asyncio
            task_to_service = asyncio.create_task(forward_to_service())
            task_to_client = asyncio.create_task(forward_to_client())
            await asyncio.gather(task_to_service, task_to_client)

    except Exception as e:
        log.error(f"Error en el proxy de WebSocket: {e}")
    finally:
        log.info(f"Cerrando conexion con el cliente.")

# --- Rutas ---

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def reverse_proxy(request: Request, path: str):
    base_url = None

    # Se elige a que servicio redirigir la peticion
    if path.startswith("token"):
        base_url = AUTH_SERVICE_URL
    elif path.startswith("users"):
        base_url = USER_SERVICE_URL
    
    # Si no hay servicio al cual redirigir, se retorna un error
    if not base_url:
        return Response(status_code=404, content="Ruta no encontrada en el gateway")

    # Se crea un cliente nuevo para cada peticion con la URL base correcta
    async with httpx.AsyncClient(base_url=base_url) as client:
        # Se construye la URL del servicio de destino
        url = httpx.URL(path=f"/{path}", query=request.url.query.encode("utf-8"))

        # Se realiza la peticion al microservicio
        rp_req = client.build_request(
            method=request.method,
            url=url,
            headers=request.headers.raw,
            content=await request.body()
        )

        # Se envia la peticion y se obtiene la respuesta
        rp_resp = await client.send(rp_req)

        # Se devuelve la respuesta al cliente
        return Response(
            content=rp_resp.content,
            status_code=rp_resp.status_code,
            headers=dict(rp_resp.headers),
        )

    # Se envia la peticion y se obtiene la respuesta
    rp_resp = await client.send(rp_req)

    # Se devuelve la respuesta al cliente
    return Response(
        content=rp_resp.content,
        status_code=rp_resp.status_code,
        headers=dict(rp_resp.headers),
    )