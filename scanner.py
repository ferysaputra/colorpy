import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ====== KONFIGURASI SERVER NX WITNESS ======
NX_SERVER = 'https://192.168.0.4:7001'  
USERNAME = 'admin'
PASSWORD = 'Invision123'
CAMERA_ID = '8bf3f8a8-dccd-21c8-3f76-a0f72fb4a6de'  

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
