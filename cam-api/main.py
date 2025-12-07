from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from webcam import Webcam
import cv2
import time
webcam = Webcam.Webcam()
webcam.readThread()
webcam.resizeThread()
app = FastAPI()
def generate_frames():
    while True:
        webcam._update_frame()
        webcam._resize()
        image = webcam.get_frame()
        # Encode the frame as JPEG
        ret, buffer = cv2.imencode(".jpg", image)
        image = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')  
        
@app.get("/")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# while True:
    # startF = time.time()
    # webcam._update_frame()
    # webcam._resize()
    # image = webcam.get_frame()
    # print  (image.shape)
    # cv2.imshow("Frame", image)
    # endF = time.time()
    # print ("FPS: {:.2f}".format(1/(endF-startF)))
    # cv2.waitKey(1)
