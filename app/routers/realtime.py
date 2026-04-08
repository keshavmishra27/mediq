from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.clinical import ChatMessage
from app.realtime.chat import manager

router = APIRouter(tags=["realtime"])


@router.websocket("/ws/chat/{appointment_id}")
async def chat_ws(websocket: WebSocket, appointment_id: str) -> None:
    """
    Simple real-time chat channel per appointment.

    Auth note:
    - For MVP, this endpoint is open.
    - In production, require a JWT (query param or subprotocol) and verify
      the user belongs to the appointment.
    """

    await manager.connect(appointment_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg = str(data.get("message", "")).strip()
            sender_user_id = str(data.get("sender_user_id", "")).strip()
            if not msg or not sender_user_id:
                await websocket.send_json({"error": "message and sender_user_id are required"})
                continue

            # Persist message
            db: Session = SessionLocal()
            try:
                db.add(ChatMessage(appointment_id=appointment_id, sender_user_id=sender_user_id, message=msg))
                db.commit()
            finally:
                db.close()

            await manager.broadcast(appointment_id, {"appointment_id": appointment_id, "sender_user_id": sender_user_id, "message": msg})
    except WebSocketDisconnect:
        manager.disconnect(appointment_id, websocket)

