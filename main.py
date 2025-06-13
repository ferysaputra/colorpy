import cv2
import numpy as np

# Open webcam
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
    cx = int(width / 2)
    cy = int(height / 2)

    pixel_center = hsv_frame[cy, cx]
    h, s, v = int(pixel_center[0]), int(pixel_center[1]), int(pixel_center[2])
    color = get_color_name(h, s, v)

    bgr_color = frame[cy, cx]
    b, g, r = int(bgr_color[0]), int(bgr_color[1]), int(bgr_color[2])

    cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
    cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
