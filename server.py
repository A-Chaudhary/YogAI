from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

data = {
    "0" : {
        "id": "0",
        "name": "Downward Dog Pose",
        "sequence": "",
        "difficulty": "1",
        "benefits": "Upper Body Strength: Activates shoulders, arms, and wrists for improved strength. Boosts Flexibility: Stretches hamstrings, calves, and foot arches, enhancing flexibility.",
        "mistakes": "Spinal Alignment: Avoid overarching the back to prevent spine compression. Shoulder Position: Keep shoulders away from ears to reduce neck and shoulder tension.",
        "tips": "Hand Placement: Spread fingers and evenly press through palms and fingertips for balanced support. Hip Elevation: Aim for an inverted V-shape by lifting hips upwards, enhancing the pose’s effectiveness.",
        "video": "Cil7tOPh4qM"
    },
    "1" : {
        "id": "1",
        "name": "Lizard Pose",
        "sequence": "",
        "difficulty": "2",
        "benefits": "Opens Hip Flexors: Ideal for those who sit frequently, offering a deep stretch to alleviate tightness. Strengthens Inner Thighs: Targets and fortifies inner thigh muscles, enhancing leg strength.",
        "mistakes": "Front Knee Alignment: Ensure the knee doesn’t collapse inward to avoid knee stress. Hip Position: Maintain level hips to prevent lower back and hip strain",
        "tips": "Core Engagement: Activate your core to support the spine and enhance balance. Prop Usage: Utilize blocks for hand or forearm support for easier reach.",
        "video": "Cil7tOPh4qM"
    },
    "2" : {
        "id": "2",
        "name": "Glizzard Poze",
        "sequence": "",
        "difficulty": "3",
        "benefits": "Opens Hip Flexors: Ideal for those who sit frequently, offering a deep stretch to alleviate tightness. Strengthens Inner Thighs: Targets and fortifies inner thigh muscles, enhancing leg strength.",
        "mistakes": "Front Knee Alignment: Ensure the knee doesn’t collapse inward to avoid knee stress. Hip Position: Maintain level hips to prevent lower back and hip strain",
        "tips": "Core Engagement: Activate your core to support the spine and enhance balance. Prop Usage: Utilize blocks for hand or forearm support for easier reach.",
        "video": "Cil7tOPh4qM"
    }
}
num_poses = 3

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/directory')
def directory():
    sort_by = request.args.get('sort_by')
    body_part = request.args.get('body_part')
    global data

    poses = [data[str(id)] for id in range(num_poses)]

    if sort_by == "name":
        sorted_poses = sorted(poses, key=lambda x: x["name"])
    elif sort_by == "difficulty":
        sorted_poses = sorted(poses, key=lambda x: x["difficulty"])
        print(sorted_poses)
    elif body_part is not None:
        for pose in poses:
            print(pose['benefits'])
        sorted_poses = [pose for pose in poses if body_part.lower() in pose['benefits'].lower()]
    else:
        sorted_poses = poses
    
    return render_template('directory.html', poses=sorted_poses)

@app.route('/learn/<id>')
def learn(id=None):

    pose = data[id]

    return render_template('learn.html', pose=pose)


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug = True)
