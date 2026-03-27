from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/pts")
async def pts_websocket_ingest(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Placeholder endpoint for hybrid mode ingestion.
            await websocket.send_text(f"ACK:{data[:40]}")
    except WebSocketDisconnect:
        return
