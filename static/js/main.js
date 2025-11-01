let stream = null;
let cameraActive = false;

function startCamera() {
    const video = document.getElementById("camera");
    const startBtn = document.getElementById("start-camera-btn");
    const captureBtn = document.getElementById("capture-btn");
    const stopBtn = document.getElementById("stop-camera-btn");

    navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
        .then(function(mediaStream) {
            stream = mediaStream;
            video.srcObject = stream;
            cameraActive = true;

            startBtn.style.display = "none";
            captureBtn.style.display = "inline-block";
            stopBtn.style.display = "inline-block";
        })
        .catch(function(error) {
            alert("Erro ao acessar câmera: " + error.message);
        });
}

function stopCamera() {
    const video = document.getElementById("camera");
    const startBtn = document.getElementById("start-camera-btn");
    const captureBtn = document.getElementById("capture-btn");
    const stopBtn = document.getElementById("stop-camera-btn");

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }

    video.srcObject = null;
    cameraActive = false;

    startBtn.style.display = "inline-block";
    captureBtn.style.display = "none";
    stopBtn.style.display = "none";

    document.getElementById("recognition-status").style.display = "none";
}

function captureAndRecognize() {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL("image/jpeg");

    // Enviar para o servidor
    const statusDiv = document.getElementById("recognition-status");
    const statusMsg = document.getElementById("status-message");

    statusDiv.style.display = "block";
    statusMsg.textContent = "⏳ Processando...";
    statusMsg.style.color = "#2d7a3e";

    fetch(reconhecerRostoUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            statusMsg.textContent = "✓ Rosto reconhecido! Redirecionando...";
            statusMsg.style.color = "#3c3";
            setTimeout(() => {
                window.location.href = "/dashboard/";
            }, 2000);
        } else {
            statusMsg.textContent = "✗ " + data.message;
            statusMsg.style.color = "#c33";
        }
    })
    .catch(error => {
        statusMsg.textContent = "✗ Erro: " + error.message;
        statusMsg.style.color = "#c33";
    });
} 