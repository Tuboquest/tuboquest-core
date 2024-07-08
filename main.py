#!/usr/bin/python3

import io
import logging
import os
import time

import dotenv
import threading
from threading import Condition
from datetime import timedelta, datetime, timezone
import jwt
from flask import Flask, Response, request, jsonify, render_template_string, session
from functools import wraps
from stepper import rotate_motor

# ================================================================================================
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

# ================================================================================================

dotenv.load_dotenv()
secret = os.getenv('secret')
algorithm = os.getenv('algorithm')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


# ================================================================================================
output = StreamingOutput()
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720)}))
picam2.start_recording(JpegEncoder(), FileOutput(output))


# ================================================================================================

def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': '⚠️ Token is missing!'}), 401
        try:
            session['token'] = token.split(" ")[1]
            print(session)
            token = token.split(" ")[1]  # Typically "Bearer <token>"
            jwt.decode(token, secret, algorithms=[algorithm])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '⚠️ Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '⛔️ Invalid token!'}), 401
        return f(*args, **kwargs)

    return wrap


@app.route('/api/get_token')
def get_token():
    # TEST TOKEN
    payload = {
        'user_id': 'tuboquest-test',
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(payload, secret, algorithm)
    return jsonify({"message": token})


def gen_stream():
    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            yield (b'--FRAME\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except GeneratorExit:
        logging.info("Stream connection closed")
    finally:
        picam2.stop_recording()
        logging.info("Camera recording stopped")


@app.route('/api/test')
@token_required
def test():
    return jsonify({'message': "🤖 - hello"})


@app.route('/api/video')
@token_required
def video_page():
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tuboquest sentinel</title>
        <style>
            body, html {
                height: 100%;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #000;
                overflow: hidden
            }
            .videoStream {
                width: 100%;
                max-width: 800px;
                height: auto;
                border: 5px solid #fff;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }
        </style>
    </head>
    <body>
        <img class="videoStream" src="/api/stream.mjpg" alt="Streaming unavailable"/>
    </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/api/stream.mjpg')
def stream_video():
    token = session.get('token')

    if not token:
        return jsonify({'message': '⚠️ Token is missing!'}), 401
    try:
        jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': '⚠️ Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': '⛔️ Invalid token!'}), 401

    return Response(gen_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=FRAME')


@app.route('/api/rotate', methods=['POST'])
@token_required
def rotate():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided - Required: angle, date'}), 400

    angle = data.get('angle')
    date = data.get('date')

    if angle is None:
        return jsonify({'message': "Angle is missing"}), 400
    if date is None:
        return jsonify({'message': "Date is missing"}), 400

    try:
        angle = float(angle)
    except ValueError:
        return jsonify({'message': 'Invalid angle value'}), 400

    # Ensure the motor rotation runs in a separate thread to avoid blocking the Flask server
    motor_thread = threading.Thread(target=rotate_motor, args=(angle,))
    motor_thread.start()

    print(f"Should rotate disc by {angle} degrees - {date}")
    return jsonify({'message': 'Success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
    picam2.stop_recording()
