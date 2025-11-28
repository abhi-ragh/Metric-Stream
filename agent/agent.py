from datetime import datetime
import psutil
import time
import requests
import os
import json

CONFIG_FILE = "config.json"

prev_bytes_recv = psutil.net_io_counters().bytes_recv
prev_bytes_sent = psutil.net_io_counters().bytes_sent

while True:
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            token = config["api_token"]
            agent_id = config["agent_id"]
            #response = requests.post('http://127.0.0.1:8000/verify',params={"api_token":token,"agent_id": agent_id})
            #if response == 0: 
            #    break

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
                "id": agent_id,
                "token": token,
                "cpu_usage": cpu_usage, 
                "mem_usage": mem_usage, 
                "disk_usage": disk_usage,
                "bytes_recv": bytes_recv,
                "bytes_send": bytes_send
            }
            response = requests.post('http://127.0.0.1:8000/metrics',json=payload)
            print(response.json())
            time.sleep(1)

        
    except FileNotFoundError:
        with open(CONFIG_FILE, "w") as f:
            print("Agent not registered")

