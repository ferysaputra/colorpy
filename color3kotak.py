import cv2
import numpy as np
#tambah
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    positions = [
        (int(width * 0.25), int(height / 2)),
        (int(width * 0.50), int(height / 2)),
        (int(width * 0.75), int(height / 2)),
    ]

    for cx, cy in positions:
        # Ambil area 20x20 piksel di sekitar titik
        offset = 25
        x1, y1 = cx - offset, cy - offset
        x2, y2 = cx + offset, cy + offset

        roi = hsv_frame[y1:y2, x1:x2]

        # Hitung rata-rata H, S, V
        h_mean = int(np.mean(roi[:, :, 0]))
        s_mean = int(np.mean(roi[:, :, 1]))
        v_mean = int(np.mean(roi[:, :, 2]))

        color_name = get_color_name(h_mean, s_mean, v_mean)

        # Gambar kotak area dan info warna
        cv2.rectangle(frame, (x1, y1), (x2, y2), (25, 25, 25), 2)
        cv2.rectangle(frame, (cx - 100, 10), (cx + 100, 60), (255, 255, 255), -1)
        cv2.putText(frame, color_name, (cx - 90, 50), 0, 1.5, (0, 0, 0), 3)

    cv2.imshow("Color Area Detection (20x20)", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
