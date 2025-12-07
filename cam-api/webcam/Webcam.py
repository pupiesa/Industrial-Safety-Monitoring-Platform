import cv2
from threading import Thread
from multiprocessing import Process, Queue

class Webcam:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]
        self.current_frame = cv2.resize(self.current_frame,(720,480), interpolation=cv2.INTER_NEAREST)

    def _update_frame(self):
        self.current_frame = self.video_capture.read()[1]

    def _resize(self):
        self.current_frame = cv2.resize(self.current_frame,(720,480), interpolation=cv2.INTER_NEAREST)

    def resizeThread(self):
        p2 = Process(target=self._resize, args=())
        p2.start()

    def readThread(self):
        p1 = Process(target=self._update_frame, args=())
        p1.start()

    def get_frame(self):
        return self.current_frame
