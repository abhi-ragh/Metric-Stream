import os 
import json
import requests

CONFIG_FILE = "config.json"
print("Registering the Agent")
with open(CONFIG_FILE, "w") as f:
    agent_name = input("Enter a Name for the Agent: ")
    response = requests.post("http://127.0.0.1:8000/register", params={"name":agent_name})
    print(response)
    data = response.json()
    print("Token: ", data["token"])
    print("Agent_ID: ", data["agent_id"])
    json.dump({"api_token": data["token"], "agent_id": data["agent_id"]}, f)