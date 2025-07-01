import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3

# Nonaktifkan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Konfigurasi server dan akun
nx_host = "https://192.168.1.66:7001"
username = "admin"
password = "vvtk3454"  # pastikan tidak salah!

# Payload JSON event
payload = {
    "caption": "Trigger dari Python",
    "description": "Tes kirim event ke Nx Witness",
    "eventType": "customPluginEvent",
    "sourceId": "python-script",
    "metadata": ""
}

# Kirim request
try:
    response = requests.post(
        f"{nx_host}/api/createEvent",
        auth=HTTPBasicAuth(username, password),
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        verify=False
    )
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
