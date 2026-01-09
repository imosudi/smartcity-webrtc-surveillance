# app.py

import socket
import os, time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
import logging
import ssl

from os.path import join, dirname

certfile = join(dirname(__file__), 'certs/cert.pem') #"/certs/cert.pem")
keyfile = join(dirname(__file__), 'certs/key.pem')

# Configure logging to suppress SSL errors
logging.getLogger('gevent').setLevel(logging.ERROR)
logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

# Only show warnings and above for werkzeug
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our_weak_secret_key'

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="gevent",
    logger=False,  # Disable SocketIO logger
    engineio_logger=False  # Disable Engine.IO logger
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

@socketio.on_error_default
def default_error_handler(e):
    """Handle SocketIO errors silently"""
    pass

if __name__ == "__main__":
    # Suppress SSL handshake errors
    import warnings
    warnings.filterwarnings('ignore', message='.*SSL.*')
    
    # Create SSL context with better error handling
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    ssl_context.load_cert_chain(
        certfile=certfile,
        keyfile=keyfile
    )
    
    # Optional: Set to not require client certificates
    #ssl_context.check_hostname = False
    #ssl_context.verify_mode = ssl.CERT_NONE

    # Get all network interfaces
    hostname = socket.gethostname()
    local_ips = []
    
    try:
        # Get all IP addresses associated with the hostname
        addr_info = socket.getaddrinfo(hostname, None)
        for info in addr_info:
            ip = info[4][0]
            if ':' not in ip:  # Filter out IPv6 for cleaner output
                if ip not in local_ips and ip != '127.0.0.1':
                    local_ips.append(ip)
    except:
        pass
    
    # Also get the primary local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        primary_ip = s.getsockname()[0]
        s.close()
        if primary_ip not in local_ips:
            local_ips.insert(0, primary_ip)
    except:
        pass
        
    print("=" * 50)
    print("🚀 WebRTC Surveillance Server Starting...")
    print("=" * 50)
    print(f"🖥️  Hostname: {hostname}")
    print(f"📍 Listening: 0.0.0.0:5000")
    print("")
    print("🌐 Access URLs:")
    print(f"   • https://localhost:5000")
    for ip in local_ips:
        print(f"   • https://{ip}:5000")
    print("")
    print("🔒 SSL: Enabled")
    print("🔄 WebSocket: Ready")
    print("=" * 50)
    
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        certfile=certfile,
        keyfile=keyfile,
        debug=False,
        #ssl_context=ssl_context,
        #debug=True,  
        use_reloader=True  
    )