# Smart City WebRTC Surveillance 🎥

<p align="center">
  <img src="docs/svgviewer-output.svg" width="600"/>
</p>

A decentralised IoT surveillance gateway using WebRTC for ultra-low-latency, secure, browser-native live video preview in smart city environments. The system combines peer-to-peer media delivery with a lightweight Flask–Socket.IO signalling plane and edge-based intelligence.

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)

## ✨ Features

- **🚀 Ultra-Low Latency**: WebRTC peer-to-peer streaming with <100ms latency
- **🔒 Secure by Design**: DTLS-SRTP encrypted media streams, HTTPS/WSS signalling
- **🌐 Browser-Native**: Zero plugin requirements, works in any modern browser
- **⚡ Edge Computing**: Lightweight signalling server for distributed deployments
- **🏙️ Smart City Ready**: Scalable architecture for multi-zone surveillance
- **📱 Real-Time**: Socket.IO for instant peer connection signalling

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Camera    │◄───────►│   Signaling  │◄───────►│  Dashboard  │
│  (Browser)  │  Socket │    Server    │  Socket │  (Browser)  │
│             │   .IO   │ Flask+SocketIO│   .IO  │             │
└─────────────┘         └──────────────┘         └─────────────┘
       │                                                  │
       └──────────────────────────────────────────────────┘
                    WebRTC P2P Media Stream
                      (DTLS-SRTP Encrypted)
```

## 📋 Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- SSL certificate (self-signed or CA-issued)
- Webcam or IP camera (for streaming)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/imosudi/smartcity-webrtc-surveillance.git
cd smartcity-webrtc-surveillance
```

### 2. Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Or on some systems
python -m venv venv
```

### 3. Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure SSL Certificates

WebRTC requires HTTPS for security. Generate a self-signed certificate for testing:

```bash
# Generate self-signed certificate (valid for 365 days)
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=localhost"
```

**Important**: Update the certificate paths in `app.py`:

```python
certfile="/path/to/your/cert.pem",
keyfile="/path/to/your/key.pem",
```
Default:
```python
certfile = join(dirname(__file__), 'certs/cert.pem')
keyfile = join(dirname(__file__), 'certs/key.pem')
```
### 6. Run the Application

```bash
python app.py
```

You should see output like:

```
==================================================
🚀 WebRTC Surveillance Server Starting...
==================================================
🖥️  Hostname: your-hostname
📍 Listening: 0.0.0.0:5000

🌐 Access URLs:
   • https://localhost:5000
   • https://192.168.1.100:5000

🔒 SSL: Enabled
🔄 WebSocket: Ready
==================================================
```

### 7. Access the Dashboard

Open your browser and navigate to one of the URLs shown above:

```
https://localhost:5000
```

**Note**: You may see a security warning for self-signed certificates. Click "Advanced" and proceed to continue.

## 📱 Usage

### Camera Stream (Publisher)

1. Open the dashboard in one browser window/device
2. Select "Camera" mode
3. Choose your surveillance zone
4. Click "Start Streaming"
5. Allow camera permissions when prompted

### Monitor View (Subscriber)

1. Open the dashboard in another browser window/device
2. Select "Monitor" mode
3. Choose the same zone as the camera
4. The live feed will appear automatically

## 🔧 Configuration

### Port Configuration

Edit `app.py` to change the default port:

```python
socketio.run(
    app,
    host="0.0.0.0",
    port=5000,  # Change this
    ssl_context=ssl_context,
    debug=False
)
```

### CORS Settings

Modify allowed origins in `app.py`:

```python
socketio = SocketIO(
    app,
    cors_allowed_origins="*",  # Change for production
    async_mode="gevent"
)
```

### Zone Management

Zones are defined client-side. Update the dashboard template to add custom surveillance zones.

## 🗂️ Project Structure

```
smartcity-webrtc-surveillance/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── cert.pem              # SSL certificate (you generate)
├── key.pem               # SSL private key (you generate)
├── templates/
│   └── dashboard.html    # WebRTC dashboard interface
├── static/               # Static assets (CSS, JS, images)
└── README.md             # This file
```

## 🛠️ Dependencies

- **Flask**: Web framework
- **Flask-SocketIO**: WebSocket communication
- **gevent**: Async networking library
- **gevent-websocket**: WebSocket support for gevent

See `requirements.txt` for complete dependency list.

## 🔒 Security Considerations

### Production Deployment

1. **Use Valid SSL Certificates**: Replace self-signed certificates with CA-issued ones (Let's Encrypt, etc.)

2. **Restrict CORS**: Change `cors_allowed_origins="*"` to specific domains

3. **Add Authentication**: Implement user authentication before accessing streams

4. **Firewall Rules**: Only expose necessary ports

5. **Update Dependencies**: Regularly update packages for security patches

```bash
pip install --upgrade -r requirements.txt
```

## 🐛 Troubleshooting

### SSL Certificate Errors

```bash
# Browser shows "Your connection is not private"
# Solution: Accept the self-signed certificate or use a valid CA certificate
```

### Camera Not Accessible

```bash
# Error: "Permission denied" or "Camera not found"
# Solution: 
# 1. Ensure HTTPS is enabled (WebRTC requires it)
# 2. Grant camera permissions in browser settings
# 3. Check if another app is using the camera
```

### Connection Issues

```bash
# Cannot connect to server
# Solution:
# 1. Check firewall rules
# 2. Verify the server is running
# 3. Ensure you're using HTTPS, not HTTP
# 4. Check the correct IP address/port
```

### Port Already in Use

```bash
# Error: "Address already in use"
# Solution: Change the port in app.py or kill the process using port 5000
lsof -ti:5000 | xargs kill -9  # Linux/macOS
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Project Link: [https://github.com/imosudi/smartcity-webrtc-surveillance](https://github.com/imosudi/smartcity-webrtc-surveillance)

## 🙏 Acknowledgments

- WebRTC API for real-time communication
- Flask and Socket.IO communities
- Smart city IoT research initiatives

---

**⚠️ Disclaimer**: This software is provided for educational and research purposes. Ensure compliance with local surveillance and privacy laws when deploying in production environments.