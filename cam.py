import cv2
import time

class CamModule:

  def __init__(self, port) -> None:
    self.cap = cv2.VideoCapture(port)
    self.last_frame = None


  def capture(self):
    ret, frame = self.cap.read()
    
    if not ret:
        print("Erro ao capturar o frame.")
        return

    self.last_frame = frame

  def run(self):
     print('captura iniciada')
     while True:
        self.capture()