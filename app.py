from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="gevent"  # Use gevent instead of eventlet
)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@socketio.on("join")
def join(data):
    join_room(data["zone"])
    emit("peer-joined", room=data["zone"], include_self=False)

@socketio.on("offer")
def offer(data):
    emit("offer", data, room=data["zone"], include_self=False)

@socketio.on("answer")
def answer(data):
    emit("answer", data, room=data["zone"], include_self=False)

@socketio.on("ice-candidate")
def ice(data):
    emit("ice-candidate", data, room=data["zone"], include_self=False)

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        certfile="/home/mosud/cert.pem",
        keyfile="/home/mosud/key.pem",
        debug=True
    )