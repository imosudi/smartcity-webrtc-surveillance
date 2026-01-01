const socket = io();

let zone;
let role;
let localStream;
let pc;

const rtcConfig = {
    iceServers: [
        { urls: "stun:stun.l.google.com:19302" }
        // TURN goes here in production
    ]
};

const localVideo  = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");
const connectBtn  = document.getElementById("connectBtn");

/* ------------------------------
   User clicks Connect
--------------------------------*/
connectBtn.onclick = async () => {
    zone = document.getElementById("zone").value.trim();
    role = document.getElementById("role").value;

    if (!zone) {
        alert("Zone ID required");
        return;
    }

    socket.emit("join", { zone });

    if (role === "edge") {
        localStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        localVideo.srcObject = localStream;
    }
};

/* ------------------------------
   Peer initialisation
--------------------------------*/
function initPeer() {
    pc = new RTCPeerConnection(rtcConfig);

    if (role === "edge" && localStream) {
        localStream.getTracks().forEach(track => {
            pc.addTrack(track, localStream);
        });
    }

    pc.ontrack = event => {
        remoteVideo.srcObject = event.streams[0];
        remoteVideo.play().catch(() => {});
    };

    pc.onicecandidate = event => {
        if (event.candidate) {
            socket.emit("ice-candidate", {
                zone,
                candidate: event.candidate
            });
        }
    };

    pc.onconnectionstatechange = () => {
        console.log("Connection state:", pc.connectionState);
    };
}

/* ------------------------------
   Signalling logic (NO glare)
--------------------------------*/
socket.on("peer-joined", async () => {
    if (role !== "edge") return;

    initPeer();

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    socket.emit("offer", {
        zone,
        offer
    });
});

socket.on("offer", async data => {
    if (role !== "viewer") return;

    initPeer();

    await pc.setRemoteDescription(new RTCSessionDescription(data.offer));

    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);

    socket.emit("answer", {
        zone,
        answer
    });
});

socket.on("answer", async data => {
    if (!pc) return;
    await pc.setRemoteDescription(new RTCSessionDescription(data.answer));
});

socket.on("ice-candidate", async data => {
    if (!pc) return;
    try {
        await pc.addIceCandidate(new RTCIceCandidate(data.candidate));
    } catch (e) {
        console.warn("ICE error", e);
    }
});
