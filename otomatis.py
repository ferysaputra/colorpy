# tambah simpan otomatis hasil warna ke csv
import cv2
import numpy as np
import time
import csv
from datetime import datetime

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

box_position = [640, 360]  # tengah layar
box_size = 20
saved_colors = []

# Untuk mendeteksi perubahan warna
hue_history = []
history_duration = 3  # dalam detik
last_save_time = 0
significant_diff = 15  # ambang batas perubahan H yang signifikan

# File CSV untuk menyimpan warna
date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file_path = f"saved_colors_{date_str}.csv"
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Color", "H", "S", "V", "Timestamp"])


def get_color_name(h, s, v):
    if s < 50 and v > 200:
        return "WHITE"
    elif v < 50:
        return "BLACK"
    elif s < 50:
        return "GRAY"
    if 0 <= h < 10 or 170 <= h <= 180:
        return "RED"
    elif 10 <= h < 25:
        return "ORANGE"
    elif 25 <= h < 35:
        return "YELLOW"
    elif 35 <= h < 85:
        return "GREEN"
    elif 85 <= h < 125:
        return "BLUE"
    elif 125 <= h < 160:
        return "VIOLET"
    elif 160 <= h < 170:
        return "PINK"
    else:
        return "UNDEFINED"


def save_color(color_name, h, s, v):
    timestamp = datetime.now().strftime("%H:%M:%S %A %d-%m-%Y")
    saved_colors.append((color_name, h, s, v, timestamp))
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([color_name, h, s, v, timestamp])


def mouse_move(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        box_position[0] = x
        box_position[1] = y

cv2.namedWindow("Color Detection")
cv2.setMouseCallback("Color Detection", mouse_move)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cx, cy = box_position
    offset = box_size // 2
    x1, y1 = max(cx - offset, 0), max(cy - offset, 0)
    x2, y2 = min(cx + offset, frame.shape[1]), min(cy + offset, frame.shape[0])

    roi = hsv_frame[y1:y2, x1:x2]
    h_mean = int(np.mean(roi[:, :, 0]))
    s_mean = int(np.mean(roi[:, :, 1]))
    v_mean = int(np.mean(roi[:, :, 2]))
    color_name = get_color_name(h_mean, s_mean, v_mean)

    # Tambahkan hue ke riwayat dengan timestamp
    current_time = time.time()
    hue_history.append((current_time, h_mean))
    hue_history = [(t, h) for (t, h) in hue_history if current_time - t <= history_duration]

    if hue_history:
        h_values = [h for (_, h) in hue_history]
        h_min, h_max = min(h_values), max(h_values)
        if abs(h_mean - h_min) > significant_diff or abs(h_mean - h_max) > significant_diff:
            if current_time - last_save_time > 1:
                save_color(color_name, h_mean, s_mean, v_mean)
                last_save_time = current_time
                hue_history = []

    # Gambar kotak dan label warna
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.rectangle(frame, (10, 10), (410, 60), (255, 255, 255), -1)
    cv2.putText(frame, f"{color_name} HSV({h_mean},{s_mean},{v_mean})", (15, 45), 0, 1.2, (0, 0, 0), 2)

    # Tampilkan daftar warna tersimpan
    for i, (name, h, s, v, timestamp) in enumerate(saved_colors[-10:]):
        cv2.putText(frame, f"{name} HSV({h},{s},{v}) {timestamp}", (15, 80 + i * 30), 0, 0.6, (0, 0, 0), 1)

    cv2.imshow("Color Detection", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break
    elif key == ord('s'):
        save_color(color_name, h_mean, s_mean, v_mean)

cap.release()
cv2.destroyAllWindows()