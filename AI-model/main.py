from ultralytics import YOLO
import cv2
import math

# cam = "http://100.94.83.16:8000/"
cam = "contract.mp4"
model = YOLO("yolo_custom.pt")
yolo_class = ["helmet","gloves","vest","boots","goggles","none","Person","no_helmet","no_goggle","no_gloves","no_boots"]
color_map = [(0, 255, 255),(255, 0, 0),(0, 165, 255),(0, 0, 0),(0, 255, 0),(255, 255, 255),(255, 255, 0),(0, 0, 255),(128, 0, 128),(203, 192, 255),(19, 69, 139)]

# try:
#     while True:
#         cap = cv2.VideoCapture(cam)
#         ret, frame = cap.read()
#         if not ret:
#             print("Failed to grab frame")
#             break

#         results = model(frame)

#         for result in results:
#             boxes = result.boxes
#             for box in boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 conf = math.ceil((box.conf[0] * 100)) / 100
#                 cls = int(box.cls[0])
#                 label = f"{yolo_class[cls]} {conf}"
#                 if conf >= 0.65:
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), color_map[cls], 2)
#                     cv2.putText(frame, f'ID:{label} Conf:{conf:.2f}', (x1, y1 - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[cls], 2)

#         cv2.imshow("YOLO Detection", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
    
# except KeyboardInterrupt:
#     print("Exiting program...")
#     cap.release()
#     cv2.destroyAllWindows()

cap = cv2.VideoCapture(cam)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    results = model(frame)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            label = f"{yolo_class[cls]} {conf}"
            if conf >= 0.3:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color_map[cls], 2)
                cv2.putText(frame, f'ID:{label} Conf:{conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[cls], 2)

    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()