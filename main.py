import cv2
import numpy as np

#webcam video source
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#definisi warna dari nilai hsv
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

    # Koordinat 3 titik: kiri, tengah, kanan
    positions = [
        (int(width * 0.25), int(height / 2)),
        (int(width * 0.50), int(height / 2)),
        (int(width * 0.75), int(height / 2)),
    ]

    for i, (cx, cy) in enumerate(positions):
        hsv_pixel = hsv_frame[cy, cx]
        h, s, v = int(hsv_pixel[0]), int(hsv_pixel[1]), int(hsv_pixel[2])
        color_name = get_color_name(h, s, v)

        bgr_pixel = frame[cy, cx]
        b, g, r = int(bgr_pixel[0]), int(bgr_pixel[1]), int(bgr_pixel[2])

        # Gambar lingkaran dan label warna
        cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
        cv2.rectangle(frame, (cx - 100, 10), (cx + 100, 60), (255, 255, 255), -1)
        cv2.putText(frame, color_name, (cx - 90, 50), 0, 1.5, (b, g, r), 3)

    cv2.imshow("Multi Color Detection", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
