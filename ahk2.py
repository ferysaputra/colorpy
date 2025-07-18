import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3

# Nonaktifkan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Konfigurasi server dan akun
nx_host = "https://192.168.0.4:7001"
username = "admin"
password = "Invision123"  # pastikan tidak salah!

# Payload JSON event
payload = {
    "timestamp": 0,
    "name": "ESP32 Gate Opened",
    "source": "ESP32",
    "caption": "Gate Triggered",
    "description": "Barrier gate dibuka oleh ESP32"
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

