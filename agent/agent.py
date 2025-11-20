from datetime import datetime
import psutil
import time
import requests

date = datetime.today().strftime("%d-%m-%Y")

prev_bytes_recv = psutil.net_io_counters().bytes_recv
prev_bytes_sent = psutil.net_io_counters().bytes_sent

while True:
    cpu_usage = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    curr_bytes_recv = psutil.net_io_counters().bytes_recv
    curr_bytes_send = psutil.net_io_counters().bytes_sent
    
    bytes_send = (curr_bytes_send-prev_bytes_sent)/1024
    bytes_recv = (curr_bytes_recv-prev_bytes_recv)/1024
    
    prev_bytes_recv = curr_bytes_recv
    prev_bytes_sent = curr_bytes_send
    
    payload = {
        "date": date, 
        "cpu_usage": cpu_usage, 
        "mem_usage": mem_usage, 
        "disk_usage": disk_usage,
        "bytes_recv": bytes_recv,
        "bytes_send": bytes_send
    }

    response = requests.post('http://127.0.0.1:8000/metrics',json=payload)
    print(response)

    time.sleep(1)