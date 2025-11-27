from fastapi import APIRouter
import sqlite3 as sql
from db.schema import connect_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Metrics(BaseModel):
    id: str
    cpu_usage: float
    mem_usage: float
    disk_usage: float
    bytes_recv: float
    bytes_send: float


@router.post("/metrics")
def write_metrics(payload: Metrics):
    ts = datetime.utcnow().isoformat()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metrics (ts, cpu, mem, disk, bytes_recv, bytes_send) VALUES (?,?,?,?,?,?)",(ts,payload.cpu_usage,payload.mem_usage,payload.disk_usage,payload.bytes_send,payload.bytes_recv) 
        )
    conn.commit()
    conn.close()
    return {
        "Status":"Success"
    }

@router.get("/metrics")
def read_metrics():
    conn = connect_db()
    cursor = conn.cursor()
    tasks = cursor.execute("SELECT * FROM metrics").fetchall()
    conn.commit()
    conn.close()
    return tasks
