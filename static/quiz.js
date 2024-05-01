function flipVideo(video) {
    video.style.transform = 'scaleX(-1)';  // Flip horizontally
}

async function setupCamera() {
    const video = document.getElementById('video');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });
        video.srcObject = stream;

        flipVideo(video);

        return new Promise((resolve) => {
            video.onloadedmetadata = () => {
                video.play();
                resolve(video);
            };
        });
    } catch (error) {
        console.error('Error accessing the webcam:', error);
        alert('Error accessing the webcam: ' + error.message);
    }
}

async function loadPoseNet() {
    try {
        const net = await posenet.load();
        return net;
    } catch (error) {
        console.error('Error loading PoseNet:', error);
        alert('Error loading PoseNet: ' + error.message);
    }
}

async function init() {
    const video = await setupCamera();
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    if (video) {
        const net = await loadPoseNet();
        if (net) {
            detectPose(video, net, canvas, ctx);
        }
    }
}

function detectPose(video, net, canvas, ctx) {
    const poseDetectionFrame = async () => {
        const pose = await net.estimateSinglePose(video, {
            flipHorizontal: false
        });

        drawCanvas(video, canvas, ctx, pose);
        requestAnimationFrame(poseDetectionFrame);
    }
    poseDetectionFrame();
}

function drawCanvas(video, canvas, ctx, pose) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.save();
    ctx.scale(-1, 1);
    ctx.translate(-canvas.width, 0);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    drawKeypoints(pose.keypoints, ctx, 0.5);
    drawSkeleton(pose.keypoints, ctx, 0.5);
    ctx.restore();
}

function drawKeypoints(keypoints, ctx, minConfidence) {
    keypoints.forEach(keypoint => {
        if (keypoint.score > minConfidence) {
            const { y, x } = keypoint.position;
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = 'aqua';
            ctx.fill();
        }
    });
}

function drawSkeleton(keypoints, ctx, minConfidence) {
    const connectedParts = [
        ['leftHip', 'leftKnee'], ['leftKnee', 'leftAnkle'],
        ['rightHip', 'rightKnee'], ['rightKnee', 'rightAnkle'],
        ['leftHip', 'rightHip'], ['leftShoulder', 'rightShoulder'],
        ['leftElbow', 'leftWrist'], ['rightElbow', 'rightWrist']
    ];
    connectedParts.forEach(([start, end]) => {
        const partA = keypoints.find(k => k.part === start);
        const partB = keypoints.find(k => k.part === end);
        if (partA && partB && partA.score > minConfidence && partB.score > minConfidence) {
            ctx.beginPath();
            ctx.moveTo(partA.position.x, partA.position.y);
            ctx.lineTo(partB.position.x, partB.position.y);
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
    });
}

let countdown = 7;
const timerElement = document.getElementById('timer');

function updateTimer() {
    timerElement.textContent = countdown;

    if (countdown === 0) {

        const lastFrame = captureLastFrame(video, canvas);  // Capture the last frame
        sendImageFrameToBackend(lastFrame);

        document.getElementById('nextPoseForm').submit();  // Move to the next pose
    } else {
        countdown -= 1;
        setTimeout(updateTimer, 1000);  // Call updateTimer again after 1 second
    }
}

function captureLastFrame(video, canvas) {
    const tempCanvas = document.createElement('canvas');  // Create a temporary canvas
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;

    const tempCtx = tempCanvas.getContext('2d');  // Get context for the temporary canvas
    tempCtx.drawImage(video, 0, 0, canvas.width, canvas.height);  // Draw the current video frame

    tempCtx.save();  // Save the current state
    tempCtx.scale(-1, 1);  // Apply a negative scale to flip horizontally
    tempCtx.translate(-canvas.width, 0);  // Adjust position due to flip
    tempCtx.drawImage(video, 0, 0, canvas.width, canvas.height);  // Draw the video frame
    tempCtx.restore();

    return tempCanvas.toDataURL();  // Convert to data URL
}

function sendImageFrameToBackend(imageDataURL) {
    const xhr = new XMLHttpRequest();  // Create an XMLHttpRequest instance

    xhr.open('POST', '/save_image_frame', true);  // Open a POST request to '/save_image_frame'
    xhr.setRequestHeader('Content-Type', 'application/json');  // Set content type to JSON

    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log('Image frame sent successfully:', xhr.responseText);  // Success response
        } else {
            console.error('Error sending image frame:', xhr.responseText);  // Error response
        }
    };

    xhr.onerror = function () {
        console.error('Network error while sending image frame');  // Network error handling
    };

    xhr.send(JSON.stringify({ imageData: imageDataURL }));  // Send image data URL
}


document.addEventListener('DOMContentLoaded', () => {
    init();  // Start the camera and PoseNet
    setTimeout(updateTimer, 1000);  // Start the timer 1 second after page load
});

