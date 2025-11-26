from fastapi import APIRouter
import sqlite3 as sql
from db.schema import connect_db

router = APIRouter()

@router.post("/metrics")
def write_metrics(date, cpu_usage, mem_usage, disk_usage, net_recv, net_send):
    conn = connect_db(date)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO metrics VALUES (?,?,?,?,?)",(cpu_usage,mem_usage,disk_usage,net_send,net_recv) 
        )
    conn.commit()
    conn.close()
    return {
        "Status":"Success"
    }

@router.get("/metrics")
def read_metrics(date):
    conn = connect_db(date)
    cursor = conn.cursor()
    tasks = cursor.execute("SELECT * FROM metrics").fetchall()
    conn.commit()
    conn.close()
    return tasks
