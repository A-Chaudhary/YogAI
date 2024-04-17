async function setupCamera() {
    const video = document.getElementById('video');
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });
        video.srcObject = stream;
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
