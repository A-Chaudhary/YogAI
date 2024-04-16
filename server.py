from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

data = {
    "0" : {
        "id": "0",
        "name": "Downward Dog Pose",
        "benefits": "Upper Body Strength: Activates shoulders, arms, and wrists for improved strength. Boosts Flexibility: Stretches hamstrings, calves, and foot arches, enhancing flexibility.",
        "mistakes": "Spinal Alignment: Avoid overarching the back to prevent spine compression. Shoulder Position: Keep shoulders away from ears to reduce neck and shoulder tension.",
        "tips": "Hand Placement: Spread fingers and evenly press through palms and fingertips for balanced support. Hip Elevation: Aim for an inverted V-shape by lifting hips upwards, enhancing the pose’s effectiveness.",
        "video": "Cil7tOPh4qM"
    }
}

@app.route('/learn/<id>')
def view(id = None):
    global data

    pose = data[id]
    return render_template('view.html', pose=pose)

if __name__ == '__main__':
    app.run(debug = True)
