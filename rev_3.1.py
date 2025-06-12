#Bisa digeser pakai mouse
#simpan hasil warna

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Variabel untuk posisi kotak
box_position = [640, 360]  # tengah layar
box_size = 20
saved_colors = []

# Fungsi untuk menentukan nama warna berdasarkan HSV
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

# Fungsi mouse callback untuk mengubah posisi kotak
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

    # Gambar kotak dan label warna
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.rectangle(frame, (10, 10), (310, 60), (255, 255, 255), -1)
    cv2.putText(frame, f"{color_name} HSV({h_mean},{s_mean},{v_mean})", (15, 45), 0, 1.2, (0, 0, 0), 2)

    # Tampilkan daftar warna tersimpan
    for i, (name, h, s, v) in enumerate(saved_colors):
        cv2.putText(frame, f"{name} HSV({h},{s},{v})", (15, 80 + i * 30), 0, 0.8, (0, 0, 0), 1)

    cv2.imshow("Color Detection", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break
    elif key == ord('s'):
        saved_colors.append((color_name, h_mean, s_mean, v_mean))

cap.release()
cv2.destroyAllWindows()
