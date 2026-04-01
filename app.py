from flask import Flask, render_template
from flask_socketio import SocketIO
from random_number import generate_number
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")

# Start background task PROPERLY
def send_numbers():
    while True:
        num = generate_number()
        print("Sending:", num)   # DEBUG
        socketio.emit('new_number', {'number': num})
        socketio.sleep(1)   # IMPORTANT (not time.sleep)

@socketio.on('connect')
def start_sending():
    print("Client connected")
    socketio.start_background_task(send_numbers)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5003)