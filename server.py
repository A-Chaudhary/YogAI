from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

sequences = ["Warrior", "Core Strengthener"]

data = {
    "0" : {
        "id": "0",
        "name": "Downward Dog Pose",
        "sequence": "",
        "difficulty": "1",
        "benefits": "Activates shoulders, arms, and wrists for improved strength. Stretches hamstrings, calves, and foot arches, enhancing flexibility.",
        "mistakes": "Avoid overarching the back to prevent spine compression. Keep shoulders away from ears to reduce neck and shoulder tension.",
        "tips": "Spread fingers and evenly press through palms and fingertips for balanced support. Aim for an inverted V-shape by lifting hips upwards, enhancing the pose’s effectiveness.",
        "video": "EC7RGJ975iM",
        "icon": "https://cdn4.iconfinder.com/data/icons/yoga-pose-outline/64/yoga-pose-meditation-suriya-namaskar-downward-dog-512.png"
    },
    "1" : {
        "id": "1",
        "name": "Lizard Pose",
        "sequence": "",
        "difficulty": "2",
        "benefits": "Ideal for those who sit frequently, offering a deep stretch to alleviate tightness. Targets and fortifies inner thigh muscles, enhancing leg strength.",
        "mistakes": "Ensure the knee doesn’t collapse inward to avoid knee stress. Maintain level hips to prevent lower back and hip strain",
        "tips": "Activate your core to support the spine and enhance balance. Utilize blocks for hand or forearm support for easier reach.",
        "video": "jXk5dquBT6w",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-poses-1-2/256/Lizard-Pose-yoga-512.png"
    },
    "2" : {
        "id": "2",
        "name": "Mountain Pose",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Mountain Pose helps in aligning the spine, shoulders, and hips, which improves overall posture. Practicing Tadasana increases body awareness, helping you identify misalignments and correct them.",
        "mistakes": "Letting the arches of the feet collapse instead of engaging them can lead to instability and improper alignment. Hyperextending or locking the knees can strain the joints. Instead, keep a micro-bend in the knees to maintain stability.",
        "tips": "Pay close attention to the alignment of your feet, ankles, knees, hips, shoulders, and head. Imagine yourself being pulled upward by a string from the crown of your head. Activate the muscles of the legs by lifting the kneecaps and engaging the quadriceps. Draw the belly button gently toward the spine to engage the core muscles.",
        "video": "Kv4C8CV8HjM",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-essentials/48/Paul-25-256.png"
    },
    "3" : {
        "id": "3",
        "name": "Warrior I",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Warrior I strengthens the legs, particularly the quadriceps, hamstrings, and calves, helping to improve overall lower body strength. Practicing this pose challenges your balance, which helps to improve coordination and stability.",
        "mistakes": "Allowing the front knee to collapse inward can strain the knee joint. Ensure that the knee is stacked directly over the ankle. Placing the back foot at an awkward angle or not grounding it properly can lead to instability. The back foot should be turned out at a 45-degree angle and firmly rooted into the ground.",
        "tips": "Pay attention to the alignment of the feet, knees, hips, and shoulders. Maintain a strong foundation with proper alignment to maximize the benefits of the pose. Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and lift the kneecaps to support the stability of the pose.",
        "video": "NytDpa2r34g",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-poses-2/48/Paul-06-256.png"
    },
    "4" : {
        "id": "4",
        "name": "Humble Warrior Pose",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Humble Warrior provides a deep stretch to the shoulders, chest, and upper back, helping to release tension in these areas. The pose stretches the hip flexors, groin, and quadriceps, promoting flexibility and mobility in the hips.elping to improve overall lower body strength. Practicing this pose challenges your balance, which helps to improve coordination and stability.",
        "mistakes": "Allowing the chest to collapse toward the thigh instead of maintaining an open chest can compromise the integrity of the pose and limit the stretch. Rounding the upper back instead of keeping it flat can strain the spine. Aim to keep the spine long and neutral.",
        "tips": "Pay attention to the alignment of the feet, knees, hips, and shoulders. Keep the front knee stacked directly over the ankle and the hips squared toward the front of the mat. Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and glutes to support the stability of the pose.",
        "video": "LwCWbc1y9sQ",
        "icon": "https://static.thenounproject.com/png/1303208-200.png"
    },
    "5" : {
        "id": "5",
        "name": "Warrior II",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Warrior II strengthens the legs, including the quadriceps, hamstrings, and calves, which promotes stability and balance. The pose opens up the hips, stretching the groin and hip flexors, which can alleviate tightness and improve flexibility.",
        "mistakes": "Allowing the front knee to collapse inward (toward the midline of the body) can strain the knee joint. Ensure the knee is stacked directly over the ankle. Incorrect placement of the back foot, such as pointing it too far forward or inward, can compromise stability and alignment. Aim to keep the back foot parallel to the short edge of the mat.",
        "tips": "Ensure the front heel is aligned with the arch of the back foot. This alignment helps maintain stability and supports proper hip positioning. Activate the core muscles by drawing the navel gently toward the spine. This action provides support to the lower back and helps maintain stability in the pose.",
        "video": "Mn6RSIRCV3w",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-essentials/48/Paul-07-512.png"
    },
    "6" : {
        "id": "6",
        "name": "Reverse Warrior",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Reverse Warrior stretches the side body, including the intercostal muscles, obliques, and latissimus dorsi, promoting increased flexibility and range of motion. The pose opens up the hips and groin, providing relief from tightness and improving hip mobility.",
        "mistakes": "Allowing the chest to collapse toward the thigh instead of maintaining an open chest can limit the stretch and compromise alignment. Excessively arching the lower back can strain the lumbar spine. Engage the core muscles and lengthen the tailbone toward the ground to maintain a neutral spine.",
        "tips": "Pay attention to the alignment of the feet, knees, hips, shoulders, and arms. Maintain a strong foundation with proper alignment to maximize the benefits of the pose. Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and inner thighs to support the stability of the pose.",
        "video": "xpKG_OrBWLI",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-poses-2-2/256/Reverse-Warrior-Pose-yoga-256.png"
    },
    "7" : {
        "id": "7",
        "name": "Warrior III",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Warrior III strengthens the muscles of the standing leg, including the quadriceps, hamstrings, and calves, as well as the core muscles, including the abdominals and lower back. Holding the pose challenges your balance and stability, helping to improve proprioception (awareness of body position in space) and coordination.",
        "mistakes": "Allowing the chest to collapse toward the ground can disrupt the alignment of the spine and compromise balance. Aim to keep the chest lifted and the spine long. Excessively arching the lower back can strain the lumbar spine. Engage the core muscles and lengthen the tailbone toward the extended heel to maintain a neutral spine.",
        "tips": "Place your hands on blocks or a chair for added support if you're working on building strength and stability in the pose. Activate the muscles of the core by drawing the navel gently toward the spine. This action helps stabilize the torso and maintain balance.",
        "video": "uEc5hrgIYx4",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-essentials/48/Paul-09-256.png"
    },
    "8" : {
        "id": "8",
        "name": "Plank Pose",
        "sequence": "Core Strengthener",
        "difficulty": "2",
        "benefits": "Plank pose primarily targets the muscles of the core, including the rectus abdominis, transverse abdominis, obliques, and lower back muscles. It helps strengthen these muscles, leading to improved stability and posture. While the core muscles are the primary focus, plank pose also engages muscles throughout the entire body, including the shoulders, arms, chest, and legs, promoting overall strength and endurance.",
        "mistakes": "Allowing the hips to sag toward the ground can put strain on the lower back and reduce the effectiveness of the pose. Keep the body in a straight line from head to heels by engaging the core muscles. Lifting the hips too high can create tension in the shoulders and limit engagement of the core muscles. Aim to maintain a neutral spine and avoid overarching or rounding the back.",
        "tips": "Focus on actively engaging the muscles of the core throughout the entire pose. Imagine drawing the navel toward the spine to create stability and support for the entire body. Pay attention to the alignment of the body, keeping the shoulders stacked over the wrists and the heels reaching back behind you. Avoid any sagging or lifting in the hips.",
        "video": "u6ZelKyUM6g",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-poses-2-2/256/Low-Plank-Pose-yoga-256.png"
    },
    "9" : {
        "id": "9",
        "name": "Boat Pose",
        "sequence": "Core Strengthener",
        "difficulty": "2",
        "benefits": "Boat Pose primarily targets the muscles of the abdomen, including the rectus abdominis, transverse abdominis, and obliques, helping to strengthen and tone the core. Holding Boat Pose requires balance and stability, which engages the muscles of the core, hips, and lower back, promoting overall stability and coordination.",
        "mistakes": "Allowing the spine to round or hunch forward can strain the lower back and reduce the effectiveness of the pose. Aim to keep the spine long and straight, with the chest lifted. Allowing the chest to collapse toward the thighs can disengage the core muscles and compromise balance. Keep the chest open and broad, lifting the sternum toward the ceiling.",
        "tips": "Focus on actively engaging the muscles of the core throughout the entire pose. Imagine drawing the navel toward the spine to create stability and support for the entire body. Pay attention to the alignment of the spine, keeping it long and straight from the tailbone to the crown of the head. Avoid rounding or overarching the back.",
        "video": "QVEINjrYUPU",
        "icon": "https://cdn1.iconfinder.com/data/icons/yoga-poses-1-2/256/Half-Boat-Pose-yoga-256.png"
    },
    "10" : {
        "id": "10",
        "name": "Forearm Plank Pose",
        "sequence": "Core Strengthener",
        "difficulty": "2",
        "benefits": "Forearm Plank primarily targets the muscles of the core, including the rectus abdominis, transverse abdominis, and obliques, helping to strengthen and tone the entire midsection. Holding Forearm Plank engages the muscles of the shoulders, arms, and upper back, helping to build strength and stability in the upper body.",
        "mistakes": "Allowing the hips to sag toward the ground can put strain on the lower back and reduce the effectiveness of the pose. Keep the body in a straight line from head to heels by engaging the core muscles. Lifting the hips too high can create tension in the shoulders and limit engagement of the core muscles. Aim to maintain a neutral spine and avoid overarching or rounding the back.",
        "tips": "Focus on actively engaging the muscles of the core throughout the entire pose. Imagine drawing the navel toward the spine to create stability and support for the entire body. Pay attention to the alignment of the body, keeping the shoulders stacked directly over the elbows and the heels reaching back behind you. Avoid any sagging or lifting in the hips.",
        "video": "3QZlgJ40LfU",
        "icon": "https://cdn4.iconfinder.com/data/icons/yoga-pose-outline/64/forearm-plank-yoga-pose-meditation-256.png"
    },
}

yoga_sequences = {
    'Sequence 1': ['Mountain', 'Downward Dog', 'Warrior I', 'Tree', 'Child'],
    'Sequence 2': ['Cobra', 'Plank', 'Seated Forward Bend', 'Triangle', 'Camel']
}

# Detailed keypoints for each pose
pose_keypoints = {
    'Mountain': {
        'leftHip': {'x': 0.5, 'y': 0.6}, 'rightHip': {'x': 0.5, 'y': 0.6},
        'leftKnee': {'x': 0.5, 'y': 0.75}, 'rightKnee': {'x': 0.5, 'y': 0.75},
        'leftAnkle': {'x': 0.5, 'y': 0.9}, 'rightAnkle': {'x': 0.5, 'y': 0.9}
    },
    'Downward Dog': {
        'leftHip': {'x': 0.4, 'y': 0.4}, 'rightHip': {'x': 0.6, 'y': 0.4},
        'leftKnee': {'x': 0.4, 'y': 0.65}, 'rightKnee': {'x': 0.6, 'y': 0.65},
        'leftAnkle': {'x': 0.35, 'y': 0.9}, 'rightAnkle': {'x': 0.65, 'y': 0.9}
    },
    'Warrior I': {
        'leftHip': {'x': 0.4, 'y': 0.55}, 'rightHip': {'x': 0.55, 'y': 0.55},
        'leftKnee': {'x': 0.3, 'y': 0.8}, 'rightKnee': {'x': 0.55, 'y': 0.8},
        'leftAnkle': {'x': 0.25, 'y': 0.95}, 'rightAnkle': {'x': 0.55, 'y': 0.95}
    },
    'Tree': {
        'leftHip': {'x': 0.5, 'y': 0.55}, 'rightHip': {'x': 0.55, 'y': 0.55},
        'leftKnee': {'x': 0.6, 'y': 0.6}, 'rightKnee': {'x': 0.55, 'y': 0.75},
        'leftAnkle': {'x': 0.5, 'y': 0.7}, 'rightAnkle': {'x': 0.55, 'y': 0.95}
    },
    'Child': {
        'leftHip': {'x': 0.5, 'y': 0.7}, 'rightHip': {'x': 0.5, 'y': 0.7},
        'leftKnee': {'x': 0.5, 'y': 0.85}, 'rightKnee': {'x': 0.5, 'y': 0.85},
        'leftAnkle': {'x': 0.5, 'y': 0.95}, 'rightAnkle': {'x': 0.5, 'y': 0.95}
    },
    'Cobra': {
        'leftHip': {'x': 0.5, 'y': 0.7}, 'rightHip': {'x': 0.5, 'y': 0.7},
        'leftKnee': {'x': 0.5, 'y': 0.85}, 'rightKnee': {'x': 0.5, 'y': 0.85},
        'leftAnkle': {'x': 0.45, 'y': 0.95}, 'rightAnkle': {'x': 0.55, 'y': 0.95}
    },
    'Plank': {
        'leftHip': {'x': 0.5, 'y': 0.5}, 'rightHip': {'x': 0.5, 'y': 0.5},
        'leftKnee': {'x': 0.5, 'y': 0.75}, 'rightKnee': {'x': 0.5, 'y': 0.75},
        'leftAnkle': {'x': 0.5, 'y': 0.95}, 'rightAnkle': {'x': 0.5, 'y': 0.95}
    },
    'Seated Forward Bend': {
        'leftHip': {'x': 0.5, 'y': 0.5}, 'rightHip': {'x': 0.5, 'y': 0.5},
        'leftKnee': {'x': 0.5, 'y': 0.6}, 'rightKnee': {'x': 0.5, 'y': 0.6},
        'leftAnkle': {'x': 0.5, 'y': 0.75}, 'rightAnkle': {'x': 0.5, 'y': 0.75}
    },
    'Triangle': {
        'leftHip': {'x': 0.4, 'y': 0.55}, 'rightHip': {'x': 0.6, 'y': 0.55},
        'leftKnee': {'x': 0.4, 'y': 0.8}, 'rightKnee': {'x': 0.6, 'y': 0.8},
        'leftAnkle': {'x': 0.4, 'y': 0.95}, 'rightAnkle': {'x': 0.6, 'y': 0.95}
    },
    'Camel': {
        'leftHip': {'x': 0.5, 'y': 0.55}, 'rightHip': {'x': 0.5, 'y': 0.55},
        'leftKnee': {'x': 0.5, 'y': 0.8}, 'rightKnee': {'x': 0.5, 'y': 0.8},
        'leftAnkle': {'x': 0.45, 'y': 0.95}, 'rightAnkle': {'x': 0.55, 'y': 0.95}
    }
}

quiz_score = 0
num_poses = 11

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
        return redirect(url_for('index'))
    pose_name = session['sequence'][session['current_pose_index']]
    keypoints = pose_keypoints[pose_name]
    return render_template('pose.html', pose_name=pose_name, keypoints=keypoints)

@app.route('/next_pose', methods=['POST'])
def next_pose():
    score = float(request.form.get('score'))
    if 'scores' not in session:
        session['scores'] = []
    session['scores'].append(score)
    session['current_pose_index'] += 1
    if session['current_pose_index'] >= len(session['sequence']):
        return redirect(url_for('results'))
    return redirect(url_for('pose'))

@app.route('/results')
def results():
    global quiz_score
    if 'scores' not in session:
        quiz_score = 0
    else:
        quiz_score = round(sum(session['scores']) / len(session['scores']), 2)

    from random import random

    scores = session['scores']


    return render_template('results.html', overall_score=quiz_score, scores=scores)

if __name__ == '__main__':
    app.run(debug = True)
