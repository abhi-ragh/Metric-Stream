from datetime import datetime
import sqlite3 as sql
import psutil
import time

prev_bytes_recv = psutil.net_io_counters().bytes_recv
prev_bytes_sent = psutil.net_io_counters().bytes_sent

while True:
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    curr_bytes_recv = psutil.net_io_counters().bytes_recv
    curr_bytes_send = psutil.net_io_counters().bytes_sent
    print("!!!!!!!!!!!!!!!!!!!!!!!!")
    print("CPU: ",cpu_usage)
    print("Memory: ",mem_usage.percent)
    print("Disk: ", disk_usage.percent)
    print("Bytes Sent: ",round((curr_bytes_send-prev_bytes_sent)/1024,2))
    print("Bytes Received: ",round((curr_bytes_recv-prev_bytes_recv)/1024,2))
    prev_bytes_recv = curr_bytes_recv
    prev_bytes_sent = curr_bytes_send
    time.sleep(1)