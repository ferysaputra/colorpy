import requests
import time
import urllib3
import json
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ====== KONFIGURASI SERVER NX WITNESS ======

config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

NX_SERVER = config["nx_server_ip"]
USERNAME = config["username"]
PASSWORD = config["password"]
CAMERA_ID = config["camera_id"] 

# ====== DATA EVENT YANG DIKIRIM ======
SOURCE = 'Barcode Scanner Sim'
CAPTION = 'Scan Detected'
DESCRIPTION_PREFIX = 'Barcode: '

# ====== FUNGSI UNTUK MENGIRIM EVENT ======
def send_event(barcode_data):
    timestamp = int(time.time() * 1000)  # waktu dalam milidetik
    url = f'{NX_SERVER}/api/createEvent'
    auth = (USERNAME, PASSWORD)

    payload = {
        'timestamp': timestamp,
        'source': SOURCE,
        'caption': CAPTION,
        'description': DESCRIPTION_PREFIX + barcode_data,
        'cameraRefs': CAMERA_ID
    }

    try:
        response = requests.post(url, data=payload, auth=auth, verify=False)
        if response.status_code == 200:
            print(f"[✓] Event berhasil dikirim: {barcode_data}")
        else:
            print(f"[!] Gagal kirim event. Status: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print("[!] Error saat kirim:", e)

# ====== SIMULASI INPUT BARCODE DARI KEYBOARD ======
print("Simulasi Barcode Scanner (tekan Ctrl+C untuk keluar)")
while True:
    barcode = input("Scan Barcode: ").strip()
    if barcode:
        send_event(barcode)
