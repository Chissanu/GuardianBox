import cv2

for i in range(10):
    cap = cv2.VideoCapture(i)
    if not cap.isOpened():
        print(f"Camera {i} not available")
    else:
        print(f"Camera {i} available")
        cap.release()
