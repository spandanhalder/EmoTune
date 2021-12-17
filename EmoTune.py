from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label   
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from deepface import DeepFace
import cv2
import os
import random

def draw_face_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


class KivyCamera(Image):

    # Global to call on click events easily
    play = 0
    stop = 0
    sound = ""
    textout = ""
    isPlaying = False

    def __init__(self, capture, fps, layout, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        # Button
        self.play = Button(text = "Play!", size_hint=(.1, .1))
        self.stop = Button(text = "Stop", size_hint=(.1, .1))
        layout.add_widget(self.play)
        layout.add_widget(self.stop)
    

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.3, 4)
            for (x,y,w,h) in faces:
                # To draw a rectangle in a face
                draw_face_border(frame, (x, y), (x+w, y+h), (132, 0, 255), 2,15,10)
            cv2.putText(frame, self.textout.capitalize(), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,145,255), 2)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture
            self.play.fbind('on_press', self.triggerPlay, frame)
            self.stop.fbind('on_press', self.triggerStop)
            
    def triggerStop(self, bt):
        if self.isPlaying:
                self.sound.stop() 
        return exit

    def triggerPlay(self, frame, bt):
        try:
            obj = DeepFace.analyze(frame, actions = ['emotion'])
            emotion = obj["dominant_emotion"]
            self.textout = emotion
            if self.isPlaying:
                self.sound.stop() 
            path = 'assets' + '/' + emotion + '/'
            self.sound = SoundLoader.load(path + str(random.randint(1, len(os.listdir(path)))) + '.mp3')
            if self.sound:
                self.sound.play()
                self.isPlaying = True

        except ValueError:
            self.textout = "Face Not Found..."

        except FileNotFoundError:
            self.textout = "Music File Does Not Exist..."

        return exit
        

class EmoTune(App):
    def build(self):
        # Icon
        self.icon = 'assets/logo/logo.png'
        # Layout 
        floatLayout = FloatLayout()
        horizontalLayout = BoxLayout(orientation='horizontal')
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=60, layout = horizontalLayout)
        # Add Layouts
        floatLayout.add_widget(horizontalLayout)
        floatLayout.add_widget(self.my_camera)
        return floatLayout


    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    EmoTune().run()
