import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp

class LiveCamera(Image):
    def __init__(self, **kwargs):
        super(LiveCamera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update at 30 FPS

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            # Draw rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # Display image from the texture
            self.texture = image_texture

class MyApp(MDApp):
    def build(self):
        self.title = 'Live Camera Face Detector'
        return LiveCamera()

if __name__ == '__main__':
    MyApp().run()
