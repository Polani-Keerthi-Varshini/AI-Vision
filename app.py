from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
import cv2
import numpy as np
from datetime import datetime
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

class ObjectDetector:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        # Simulate object detection results
        self.possible_objects = [
            "person 2 meters ahead",
            "door on right",
            "stairs 3 meters ahead",
            "chair nearby",
            "table with objects"
        ]
        
    def detect_objects(self):
        ret, frame = self.camera.read()
        if not ret:
            return None, None
        # Simulate detection
        detected = np.random.choice(self.possible_objects)
        return frame, detected

    def release(self):
        self.camera.release()

detector = ObjectDetector()

def detection_thread():
    while True:
        frame, detected_objects = detector.detect_objects()
        if detected_objects:
            socketio.emit('detection', {'objects': detected_objects})
        time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_detection')
def start_detection():
    thread = threading.Thread(target=detection_thread)
    thread.daemon = True
    thread.start()
    return jsonify({"status": "started"})

@app.route('/emergency')
def emergency():
    # Simulate emergency contact
    return jsonify({
        "status": "Emergency contacts notified",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)