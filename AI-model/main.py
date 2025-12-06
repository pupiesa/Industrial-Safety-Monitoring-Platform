from ultralytics import YOLO
import cv2
import math
from kafka import KafkaProducer
import time
import json
import random
import base64

# cam = "http://100.94.83.16:8000/"
cam = "contract.mp4"
model = YOLO("yolo_custom.pt")
yolo_class = ["helmet","gloves","vest","boots","goggles","none","Person","no_helmet","no_goggle","no_gloves","no_boots"]
color_map = [(0, 255, 255),(255, 0, 0),(0, 165, 255),(0, 0, 0),(0, 255, 0), (255, 255, 255),(255, 255, 0),(0, 0, 255),(128, 0, 128),(203, 192, 255),(19, 69, 139)]
location = ["Site A", "Site B", "Site C", "Site D"]


cap = cv2.VideoCapture(cam)
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    person_detected = False
    results = model(frame)
    detections = {cls: 0 for cls in yolo_class}
    for result in results:
        boxes = result.boxes 
        for box in boxes:
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            label = yolo_class[cls]
            if label == "Person" and conf >= 0.6:
                person_detected = True

    if person_detected:        
        for result in results:
            boxes = result.boxes 
            for box in boxes: 
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                label = yolo_class[cls]
                if conf >= 0.2:
                    detections[label] += 1
                    detections["location"] = location[random.randint(0, 2)] # Random location for demo purposes
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color_map[cls], 2)
                    cv2.putText(frame, f'ID:{label} Conf:{conf:.2f}', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[cls], 2)
                    
    if person_detected == False:
        detections = {"message": "No person detected"}

    if person_detected:
        print("-------------------json data-------------------")
        detections["image"] = base64.b64encode(cv2.imencode('.jpg', frame)[1].tobytes()).decode('utf-8')  # Encode as base64 string
        json_data = json.dumps(detections)
        print(json_data)
        producer.send('safety_detections', value=json_data.encode('utf-8'))
        # time.sleep(10) # Send data every 10 seconds
        
    cv2.imshow("YOLO Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
