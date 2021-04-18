# Realtime Facial Expression Based Music Player

It is a music player based on facial expression which is captured in realtime through webcam.

![Preview](SCREENSHOTS/REBMP.gif)

## Features
-	This is complete GUI based application.
-	Created using Python and Deepface, Kivy, OpenCV libraries.
-	The webcam is accessed by OpenCV and face is captured through Haar Cascade Classifier.
-	Then facial expressions are compared with predefined models to get the emotion. Here lightweight library Deepface is used.
-	This GUI base is created by Kivy. After getting the emotion the correct music is played by Kivy.

## Dependencies
- OpenCV
- Kivy
- TensorFlow
- Deepface
