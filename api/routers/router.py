from fastapi import APIRouter
import sqlite3 as sql
from db.schema import connect_db
from pydantic import BaseModel

router = APIRouter()

class Metrics(BaseModel):
    date: str
    cpu_usage: float
    mem_usage: float
    disk_usage: float
    bytes_recv: float
    bytes_send: float

@router.post("/metrics")
def write_metrics(payload: Metrics):
    conn = connect_db(payload.date)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metrics VALUES (?,?,?,?,?)",(payload.cpu_usage, payload.mem_usage, payload.disk_usage, payload.bytes_recv, payload.bytes_send)
        )
    conn.commit()
    conn.close()
    return {
        "Status":"Success"
    }

@router.get("/metrics")
def read_metrics(date: str):
    conn = connect_db(date)
    cursor = conn.cursor()
    tasks = cursor.execute("SELECT * FROM metrics").fetchall()
    conn.commit()
    conn.close()
    return tasks
