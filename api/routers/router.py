from fastapi import APIRouter, Request
import sqlite3 as sql
from db.schema import connect_db
from pydantic import BaseModel
from datetime import datetime
import asyncio
from fastapi.responses import StreamingResponse
import json

router = APIRouter()

class Metrics(BaseModel):
    id: str
    cpu_usage: float
    mem_usage: float
    disk_usage: float
    bytes_recv: float
    bytes_send: float

subscribers = set()

@router.post("/metrics")
async def write_metrics(payload: Metrics):
    ts = datetime.now().isoformat()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metrics (ts, cpu, mem, disk, bytes_recv, bytes_send) VALUES (?,?,?,?,?,?)",
        (ts, payload.cpu_usage, payload.mem_usage, payload.disk_usage, payload.bytes_recv, payload.bytes_send) 
    )
    conn.commit()
    conn.close()
    
    row = {
        "ts": ts,
        "cpu": payload.cpu_usage,
        "mem": payload.mem_usage,
        "disk": payload.disk_usage,
        "bytes_recv": payload.bytes_recv,
        "bytes_send": payload.bytes_send,
    }

    for q in list(subscribers):
        try:
            await q.put(json.dumps(row))
        except:
            # Remove dead queues
            subscribers.discard(q)
    
    return {"status": "ok"}

@router.get("/metrics")
def read_metrics():
    conn = connect_db()
    cursor = conn.cursor()
    tasks = cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 200").fetchall()
    conn.close()
    return tasks

@router.get("/stream")
async def stream(request: Request):
    q = asyncio.Queue()
    subscribers.add(q)
    
    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    msg = await asyncio.wait_for(q.get(), timeout=30.0)
                    yield f"data: {msg}\n\n"
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
                    
        except asyncio.CancelledError:
            pass
        finally:
            subscribers.discard(q)
    
    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no" 
        }
    )