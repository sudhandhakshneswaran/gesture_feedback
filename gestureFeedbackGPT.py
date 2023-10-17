import cv2
import mediapipe as mp
from mediapipe.tasks import python
import threading 
import os
import numpy
import hashlib
import pyglet
import time
import datetime

count = 0

class GestureRecognizer:
    def __init__(self):
        self.win = None
        self.likes_win = None
        self.folder_path = 'feedback'
        self.likes = 0

    def main(self):
        count = 0
        num_hands = 1
        model_path = "gesture_recognizer.task"
        GestureRecognizer = mp.tasks.vision.GestureRecognizer
        GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        self.lock = threading.Lock()
        self.current_gestures = []
        options = GestureRecognizerOptions(
            base_options=python.BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands = num_hands,
            result_callback=self.__result_callback)
        recognizer = GestureRecognizer.create_from_options(options)

        timestamp = 0 
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=num_hands,
                min_detection_confidence=0.65,
                min_tracking_confidence=0.65)

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            np_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np_array)
                    recognizer.recognize_async(mp_image, timestamp)
                    timestamp = timestamp + 1 # should be monotonically increasing, because in LIVE_STREAM mode
                    
                self.put_gestures(frame)

            # cv2.imshow('MediaPipe Hands', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()

    def put_gestures(self, frame):
        self.lock.acquire()
        gestures = self.current_gestures
        y_pos = 50
        for hand_gesture_name in gestures:
            # show the prediction on the frame
            # cv2.putText(frame, hand_gesture_name, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 
            #                     1, (0,0,255), 2, cv2.LINE_AA)
            # y_pos += 50
            if(hand_gesture_name == "Thumb_Up"):
                self.save_my_img(count, frame)
                #self.play_gif()
                self.likes = len(os.listdir(self.folder_path))
                time.sleep(7)
        self.lock.release()

    def __result_callback(self, result, output_image, timestamp_ms):
        print(f'outputimage: {output_image}')
        self.lock.acquire() # solves potential concurrency issues
        self.current_gestures = []
        if result is not None and any(result.gestures):
            print("Recognized gestures:")
            for single_hand_gesture_data in result.gestures:
                gesture_name = single_hand_gesture_data[0].category_name
                print(gesture_name)
                self.current_gestures.append(gesture_name)
        self.lock.release()

    def save_my_img(self, frame_count, img):
        name = f'feedback/feedback{datetime.datetime.now().strftime("%m%d%H%M%S")}.jpg'
        cv2.imwrite(name, img)

    def play_gif(self):
        if self.win is None:
            ag_file = "success.gif"
            animation = pyglet.resource.animation(ag_file)
            sprite = pyglet.sprite.Sprite(animation)

            # create a window and set it to the image size
            self.win = pyglet.window.Window(width=sprite.width, height=sprite.height)

            # set window background color = r, g, b, alpha
            # each value goes from 0.0 to 1.0
            green = 0, 1, 0, 1
            pyglet.gl.glClearColor(*green)

            @self.win.event
            def on_draw():
                self.win.clear()
                sprite.draw()

            pyglet.clock.schedule_once(self.close_pyglet, 5)
            print(pyglet.app)
            pyglet.app.run()

    def display_likes_window(self):
        if self.likes_win is None:
            # create a window and set it to the image size
            self.likes_win = pyglet.window.Window(width=500, height=500)

            # set window background color = r, g, b, alpha
            # each value goes from 0.0 to 1.0
            green = 0, 1, 0, 1
            pyglet.gl.glClearColor(*green)

            @self.likes_win.event
            def on_draw():
                self.likes_win.clear()
                sprite.draw()

            pyglet.app.run()
            self.likes

    def close_pyglet(self, dt):
        print("closing window")
        if self.win:
            self.win.close()
            self.win = None

if __name__ == "__main__":
    rec = GestureRecognizer()
    rec.main()
