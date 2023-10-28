import cv2
import time

class CamModule:

  def __init__(self, port) -> None:
    self.cap = cv2.VideoCapture(port)
    self.last_frame = None
    self.font = cv2.FONT_HERSHEY_SIMPLEX
    self.prev_frame_time = 0
    self.new_frame_time = 0

  def capture(self):
    ret, frame = self.cap.read()
    
    if not ret:
        print("Erro ao capturar o frame.")
        return

    self.new_frame_time = time.time() 
    fps = 1/(self.new_frame_time-self.prev_frame_time) 
    self.prev_frame_time = self.new_frame_time 
  
    fps = int(fps) 
    cv2.putText(frame, str(fps), (7, 70), self.font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
    self.last_frame = frame

  def run(self):
     print('captura iniciada')
     while True:
        self.capture()