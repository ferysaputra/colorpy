import requests
import base64
import json
import urllib3

# Nonaktifkan warning SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Konfigurasi server Nx
nx_host = "https://192.168.1.3:7001"  # HTTPS karena error muncul di port 7001
username = "admin"
password = "vvtk3454"

# Buat Header Basic Auth
credentials = f"{username}:{password}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json"
}

# Payload event
payload = {
    "caption": "Trigger dari Python",
    "description": "Tes HTTP dari Python",
    "eventType": "customPluginEvent",
    "sourceId": "python-script",
    "metadata": ""
}

# Kirim request ke Nx
url = f"{nx_host}/api/createEvent"

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
