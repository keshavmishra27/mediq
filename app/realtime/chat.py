from __future__ import annotations

from collections import defaultdict

from fastapi import WebSocket


class ConnectionManager:
    """
    Minimal WebSocket connection manager.

    For production scale:
    - use Redis pub/sub (or another broker) so multiple API instances can broadcast
    - add auth checks + rate limits + message validation
    """

    def __init__(self) -> None:
        self._rooms: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, room_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self._rooms[room_id].add(ws)

    def disconnect(self, room_id: str, ws: WebSocket) -> None:
        self._rooms[room_id].discard(ws)
        if not self._rooms[room_id]:
            self._rooms.pop(room_id, None)

    async def broadcast(self, room_id: str, data: dict) -> None:
        for ws in list(self._rooms.get(room_id, set())):
            await ws.send_json(data)


manager = ConnectionManager()

