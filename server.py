from flask import Flask
from flask import render_template
from flask import request, jsonify, session, redirect, url_for
import base64
import numpy as np
import cv2
import pose_estimation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

sequences = ["Warrior", "Core Strengthener"]

data = {
    "0" : {
        "id": "0",
        "name": "Downward Dog",
        "sequence": "",
        "difficulty": "1",
        "benefits": "Activates shoulders, arms, and wrists for improved strength. Stretches hamstrings, calves, and foot arches, enhancing flexibility.",
        "mistakes": "Avoid overarching the back to prevent spine compression. Keep shoulders away from ears to reduce neck and shoulder tension.",
        "tips": "Spread fingers and evenly press through palms and fingertips for balanced support. Aim for an inverted V-shape by lifting hips upwards, enhancing the pose’s effectiveness.",
        "video": "downward_dog.mp4",
        "icon": "https://cdn4.iconfinder.com/data/icons/yoga-pose-outline/64/yoga-pose-meditation-suriya-namaskar-downward-dog-512.png"
    },
    "1" : {
        "id": "1",
        "name": "Mountain",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Mountain Pose helps in aligning the spine, shoulders, and hips, which improves overall posture. Practicing Tadasana increases body awareness, helping you identify misalignments and correct them.",
        "mistakes": "Letting the arches of the feet collapse instead of engaging them can lead to instability and improper alignment. Hyperextending or locking the knees can strain the joints. Instead, keep a micro-bend in the knees to maintain stability.",
        "tips": "Pay close attention to the alignment of your feet, ankles, knees, hips, shoulders, and head. Imagine yourself being pulled upward by a string from the crown of your head. Activate the muscles of the legs by lifting the kneecaps and engaging the quadriceps. Draw the belly button gently toward the spine to engage the core muscles.",
        "video": "mountain_pose.mp4",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-essentials/48/Paul-25-256.png"
    },
    "2" : {
        "id": "2",
        "name": "Warrior I",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Warrior I strengthens the legs, particularly the quadriceps, hamstrings, and calves, helping to improve overall lower body strength. Practicing this pose challenges your balance, which helps to improve coordination and stability.",
        "mistakes": "Allowing the front knee to collapse inward can strain the knee joint. Ensure that the knee is stacked directly over the ankle. Placing the back foot at an awkward angle or not grounding it properly can lead to instability. The back foot should be turned out at a 45-degree angle and firmly rooted into the ground.",
        "tips": "Pay attention to the alignment of the feet, knees, hips, and shoulders. Maintain a strong foundation with proper alignment to maximize the benefits of the pose. Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and lift the kneecaps to support the stability of the pose.",
        "video": "warrior_1.mp4",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-poses-2/48/Paul-06-256.png"
    },
    "3" : {
        "id": "3",
        "name": "Humble Warrior",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Humble Warrior provides a deep stretch to the shoulders, chest, and upper back, helping to release tension in these areas. The pose stretches the hip flexors, groin, and quadriceps, promoting flexibility and mobility in the hips.elping to improve overall lower body strength. Practicing this pose challenges your balance, which helps to improve coordination and stability.",
        "mistakes": "Allowing the chest to collapse toward the thigh instead of maintaining an open chest can compromise the integrity of the pose and limit the stretch. Rounding the upper back instead of keeping it flat can strain the spine. Aim to keep the spine long and neutral.",
        "tips": "Pay attention to the alignment of the feet, knees, hips, and shoulders. Keep the front knee stacked directly over the ankle and the hips squared toward the front of the mat. Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and glutes to support the stability of the pose.",
        "video": "humble_warrior.mp4",
        "icon": "https://static.thenounproject.com/png/1303208-200.png"
    },
    "4" : {
        "id": "4",
        "name": "Warrior II",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Warrior II strengthens the legs, including the quadriceps, hamstrings, and calves, which promotes stability and balance. The pose opens up the hips, stretching the groin and hip flexors, which can alleviate tightness and improve flexibility.",
        "mistakes": "Allowing the front knee to collapse inward (toward the midline of the body) can strain the knee joint. Ensure the knee is stacked directly over the ankle. Incorrect placement of the back foot, such as pointing it too far forward or inward, can compromise stability and alignment. Aim to keep the back foot parallel to the short edge of the mat.",
        "tips": "Ensure the front heel is aligned with the arch of the back foot. This alignment helps maintain stability and supports proper hip positioning. Activate the core muscles by drawing the navel gently toward the spine. This action provides support to the lower back and helps maintain stability in the pose.",
        "video": "warrior_2.mp4",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-essentials/48/Paul-07-512.png"
    },
    "5" : {
        "id": "5",
        "name": "Reverse Warrior",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Reverse Warrior stretches the side body, including the intercostal muscles, obliques, and latissimus dorsi, promoting increased flexibility and range of motion. The pose opens up the hips and groin, providing relief from tightness and improving hip mobility.",
        "mistakes": "Allowing the chest to collapse toward the thigh instead of maintaining an open chest can limit the stretch and compromise alignment. Excessively arching the lower back can strain the lumbar spine. Engage the core muscles and lengthen the tailbone toward the ground to maintain a neutral spine.",
        "tips": "Pay attention to the alignment of the feet, knees, hips, shoulders, and arms. Maintain a strong foundation with proper alignment to maximize the benefits of the pose. Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and inner thighs to support the stability of the pose.",
        "video": "reverse_warrior.mp4",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-poses-2-2/256/Reverse-Warrior-Pose-yoga-256.png"
    },
    "6" : {
        "id": "6",
        "name": "Warrior III",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Warrior III strengthens the muscles of the standing leg, including the quadriceps, hamstrings, and calves, as well as the core muscles, including the abdominals and lower back. Holding the pose challenges your balance and stability, helping to improve proprioception (awareness of body position in space) and coordination.",
        "mistakes": "Allowing the chest to collapse toward the ground can disrupt the alignment of the spine and compromise balance. Aim to keep the chest lifted and the spine long. Excessively arching the lower back can strain the lumbar spine. Engage the core muscles and lengthen the tailbone toward the extended heel to maintain a neutral spine.",
        "tips": "Place your hands on blocks or a chair for added support if you're working on building strength and stability in the pose. Activate the muscles of the core by drawing the navel gently toward the spine. This action helps stabilize the torso and maintain balance.",
        "video": "warrior_3.mp4",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-essentials/48/Paul-09-256.png"
    },
}

yoga_sequences = {
    'Balance Flow Sequence': ['Chair', 'Cobra', 'Downward Dog', 'Tree', 'Warrior III'],
    'Warrior Sequence': ['Mountain', 'Warrior I', 'Humble Warrior', 'Warrior II', 'Reverse Warrior', 'Warrior III']
}

quiz_score = 0
num_poses = len(data.keys())
scores = []

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/directory')
def directory():
    sort_by = request.args.get('sort_by')
    body_part = request.args.get('body_part')
    global data
    global sequences

    poses = [data[str(id)] for id in range(num_poses)]
    sequences.sort()

    if sort_by == "name":
        sorted_poses = sorted(poses, key=lambda x: x["name"])
        sequences.sort()
    elif sort_by == "difficulty":
        sorted_poses = sorted(poses, key=lambda x: x["difficulty"])
        print(sorted_poses)
    elif sort_by == 'default':
        sorted_poses = poses
    elif body_part == 'all':
        sorted_poses = poses
    elif body_part is not None:
        for pose in poses:
            print(pose['benefits'])
        sorted_poses = [pose for pose in poses if body_part.lower() in pose['benefits'].lower()]
    else:
        sorted_poses = poses

    return render_template('directory.html', poses=sorted_poses, sequences=sequences)

@app.route('/learn/<id>')
def learn(id=None):
    global num_poses
    pose = data[id]

    return render_template('learn.html', pose=pose, num_poses = num_poses)


@app.route('/quiz')
def index():
    global scores
    scores = []
    return render_template('quiz.html', sequences=yoga_sequences)

@app.route('/start', methods=['POST'])
def start():
    sequence_name = request.form.get('sequence')
    session['sequence'] = yoga_sequences[sequence_name]
    session['current_pose_index'] = 0
    return redirect(url_for('pose'))

@app.route('/pose')
def pose():
    if 'sequence' not in session or session['current_pose_index'] >= len(session['sequence']):
        return redirect(url_for('quiz'))
    pose_name = session['sequence'][session['current_pose_index']]
    return render_template('pose.html', pose_name=pose_name, timer_duration=10)

@app.route('/save_image_frame', methods=['POST'])
def save_image_frame():
    image_data = request.json.get('imageData')
    img_bytes = base64.b64decode(image_data.split(",")[1])
    image_array = np.frombuffer(img_bytes, dtype=np.uint8) # Decode the base64 data
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    pose_dict = pose_estimation.run('movenet_thunder', None, 'classifier', 'labels.txt', image)
    pose_name = session['sequence'][session['current_pose_index']]
    if isinstance(pose_dict, dict):
        pose_score = pose_dict.get(pose_name)
        if pose_score is not None:
            scores.append(float(pose_score) * 100)
    else:
        scores.append(0)

    #with open("image.png", "wb") as image_file:
        #image_file.write(img_bytes)
    return jsonify({'status': 'success', 'image_frame_received': True}), 200

@app.route('/next_pose', methods=['POST'])
def next_pose():
    session['current_pose_index'] += 1
    if session['current_pose_index'] >= len(session['sequence']):
        return redirect(url_for('results'))
    return redirect(url_for('pose'))

@app.route('/results')
def results():
    global quiz_score
    quiz_score = round(sum(scores) / len(scores), 2)


    return render_template('results.html', overall_score=quiz_score, scores=scores)

if __name__ == '__main__':
    app.run(debug = True)
