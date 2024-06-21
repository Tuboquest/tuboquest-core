#!/usr/bin/python3

import os
import threading

import dotenv
from datetime import timedelta, datetime, timezone
import jwt
from flask import Flask, request, jsonify, session
from functools import wraps
from stepper import rotate_motor

dotenv.load_dotenv()
secret = os.getenv('secret')
algorithm = os.getenv('algorithm')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')


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


@app.route('/api/test')
@token_required
def test():
    return jsonify({'message': "🤖 - hello"})


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
