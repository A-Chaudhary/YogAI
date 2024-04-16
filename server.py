from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
app = Flask(__name__)

sequences = ["Warrior", "Core Strengthener"]

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
        "name": "Mountain Pose",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Posture Improvement: Mountain Pose helps in aligning the spine, shoulders, and hips, which improves overall posture. Awareness of Alignment: Practicing Tadasana increases body awareness, helping you identify misalignments and correct them.",
        "mistakes": "Collapsed Arches: Letting the arches of the feet collapse instead of engaging them can lead to instability and improper alignment.Locked Knees: Hyperextending or locking the knees can strain the joints. Instead, keep a micro-bend in the knees to maintain stability.",
        "tips": "Focus on Alignment: Pay close attention to the alignment of your feet, ankles, knees, hips, shoulders, and head. Imagine yourself being pulled upward by a string from the crown of your head. Engage Muscles: Activate the muscles of the legs by lifting the kneecaps and engaging the quadriceps. Draw the belly button gently toward the spine to engage the core muscles.",
        "video": "Cil7tOPh4qM"
    },
    "3" : {
        "id": "3",
        "name": "Warrior I",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Strengthens Lower Body: Warrior I strengthens the legs, particularly the quadriceps, hamstrings, and calves, helping to improve overall lower body strength. Improves Balance: Practicing this pose challenges your balance, which helps to improve coordination and stability.",
        "mistakes": "Front Knee Alignment: Allowing the front knee to collapse inward can strain the knee joint. Ensure that the knee is stacked directly over the ankle.Back Foot Position: Placing the back foot at an awkward angle or not grounding it properly can lead to instability. The back foot should be turned out at a 45-degree angle and firmly rooted into the ground.",
        "tips": "Focus on Alignment: Pay attention to the alignment of the feet, knees, hips, and shoulders. Maintain a strong foundation with proper alignment to maximize the benefits of the pose. Engage Muscles: Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and lift the kneecaps to support the stability of the pose.",
        "video": "Cil7tOPh4qM"
    },
    "4" : {
        "id": "4",
        "name": "Humble Warrior Pose",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Deep Shoulder and Chest Stretch: Humble Warrior provides a deep stretch to the shoulders, chest, and upper back, helping to release tension in these areas. Hip Opener: The pose stretches the hip flexors, groin, and quadriceps, promoting flexibility and mobility in the hips.elping to improve overall lower body strength. Improves Balance: Practicing this pose challenges your balance, which helps to improve coordination and stability.",
        "mistakes": "Collapsed Chest: Allowing the chest to collapse toward the thigh instead of maintaining an open chest can compromise the integrity of the pose and limit the stretch. Round Back: Rounding the upper back instead of keeping it flat can strain the spine. Aim to keep the spine long and neutral.",
        "tips": "Focus on Alignment: Pay attention to the alignment of the feet, knees, hips, and shoulders. Keep the front knee stacked directly over the ankle and the hips squared toward the front of the mat. Engage Muscles: Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and glutes to support the stability of the pose.",
        "video": "Cil7tOPh4qM"
    },
    "5" : {
        "id": "5",
        "name": "Warrior II",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Strengthens Legs: Warrior II strengthens the legs, including the quadriceps, hamstrings, and calves, which promotes stability and balance. Opens Hips: The pose opens up the hips, stretching the groin and hip flexors, which can alleviate tightness and improve flexibility.",
        "mistakes": "Front Knee Alignment: Allowing the front knee to collapse inward (toward the midline of the body) can strain the knee joint. Ensure the knee is stacked directly over the ankle. Back Foot Position: Incorrect placement of the back foot, such as pointing it too far forward or inward, can compromise stability and alignment. Aim to keep the back foot parallel to the short edge of the mat.",
        "tips": "Align Feet Properly: Ensure the front heel is aligned with the arch of the back foot. This alignment helps maintain stability and supports proper hip positioning. Engage Core Muscles: Activate the core muscles by drawing the navel gently toward the spine. This action provides support to the lower back and helps maintain stability in the pose.",
        "video": "Cil7tOPh4qM"
    },
    "6" : {
        "id": "6",
        "name": "Reverse Warrior",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Side Body Stretch: Reverse Warrior stretches the side body, including the intercostal muscles, obliques, and latissimus dorsi, promoting increased flexibility and range of motion. Hip Opener: The pose opens up the hips and groin, providing relief from tightness and improving hip mobility.",
        "mistakes": "Collapsed Chest: Allowing the chest to collapse toward the thigh instead of maintaining an open chest can limit the stretch and compromise alignment. Overarching Lower Back: Excessively arching the lower back can strain the lumbar spine. Engage the core muscles and lengthen the tailbone toward the ground to maintain a neutral spine.",
        "tips": "Focus on Alignment: Pay attention to the alignment of the feet, knees, hips, shoulders, and arms. Maintain a strong foundation with proper alignment to maximize the benefits of the pose. Engage Muscles: Activate the muscles of the legs by pressing firmly into the ground with both feet. Engage the quadriceps and inner thighs to support the stability of the pose.",
        "video": "Cil7tOPh4qM"
    },
    "7" : {
        "id": "7",
        "name": "Warrior III",
        "sequence": "Warrior",
        "difficulty": "3",
        "benefits": "Strengthens Legs and Core: Warrior III strengthens the muscles of the standing leg, including the quadriceps, hamstrings, and calves, as well as the core muscles, including the abdominals and lower back. Improves Balance and Stability: Holding the pose challenges your balance and stability, helping to improve proprioception (awareness of body position in space) and coordination.",
        "mistakes": "Collapsed Chest: Allowing the chest to collapse toward the ground can disrupt the alignment of the spine and compromise balance. Aim to keep the chest lifted and the spine long. Overarching Lower Back: Excessively arching the lower back can strain the lumbar spine. Engage the core muscles and lengthen the tailbone toward the extended heel to maintain a neutral spine.",
        "tips": "Use Props for Support: Place your hands on blocks or a chair for added support if you're working on building strength and stability in the pose. Engage Core Muscles: Activate the muscles of the core by drawing the navel gently toward the spine. This action helps stabilize the torso and maintain balance.",
        "video": "Cil7tOPh4qM"
    },
    "8" : {
        "id": "8",
        "name": "Plank Pose",
        "sequence": "Core Strengthener",
        "difficulty": "2",
        "benefits": "Core Strength: Plank pose primarily targets the muscles of the core, including the rectus abdominis, transverse abdominis, obliques, and lower back muscles. It helps strengthen these muscles, leading to improved stability and posture.Total Body Engagement: While the core muscles are the primary focus, plank pose also engages muscles throughout the entire body, including the shoulders, arms, chest, and legs, promoting overall strength and endurance.",
        "mistakes": "Sagging Hips: Allowing the hips to sag toward the ground can put strain on the lower back and reduce the effectiveness of the pose. Keep the body in a straight line from head to heels by engaging the core muscles. Lifting Hips Too High: Lifting the hips too high can create tension in the shoulders and limit engagement of the core muscles. Aim to maintain a neutral spine and avoid overarching or rounding the back.",
        "tips": "Engage the Core: Focus on actively engaging the muscles of the core throughout the entire pose. Imagine drawing the navel toward the spine to create stability and support for the entire body. Maintain Proper Alignment: Pay attention to the alignment of the body, keeping the shoulders stacked over the wrists and the heels reaching back behind you. Avoid any sagging or lifting in the hips.",
        "video": "Cil7tOPh4qM"
    },
    "9" : {
        "id": "9",
        "name": "Boat Pose",
        "sequence": "Core Strengthener",
        "difficulty": "2",
        "benefits": "Core Strength: Boat Pose primarily targets the muscles of the abdomen, including the rectus abdominis, transverse abdominis, and obliques, helping to strengthen and tone the core. Improves Balance and Stability: Holding Boat Pose requires balance and stability, which engages the muscles of the core, hips, and lower back, promoting overall stability and coordination.",
        "mistakes": "Rounded Back: Allowing the spine to round or hunch forward can strain the lower back and reduce the effectiveness of the pose. Aim to keep the spine long and straight, with the chest lifted. Collapsed Chest: Allowing the chest to collapse toward the thighs can disengage the core muscles and compromise balance. Keep the chest open and broad, lifting the sternum toward the ceiling.",
        "tips": "Engage Core Muscles: Focus on actively engaging the muscles of the core throughout the entire pose. Imagine drawing the navel toward the spine to create stability and support for the entire body. Maintain Proper Alignment: Pay attention to the alignment of the spine, keeping it long and straight from the tailbone to the crown of the head. Avoid rounding or overarching the back.",
        "video": "Cil7tOPh4qM"
    },
    "10" : {
        "id": "10",
        "name": "Forearm Plank Pose",
        "sequence": "Core Strengthener",
        "difficulty": "2",
        "benefits": "Core Strength: Forearm Plank primarily targets the muscles of the core, including the rectus abdominis, transverse abdominis, and obliques, helping to strengthen and tone the entire midsection. Shoulder and Arm Strength: Holding Forearm Plank engages the muscles of the shoulders, arms, and upper back, helping to build strength and stability in the upper body.",
        "mistakes": "Sagging Hips: Allowing the hips to sag toward the ground can put strain on the lower back and reduce the effectiveness of the pose. Keep the body in a straight line from head to heels by engaging the core muscles. Lifting Hips Too High: Lifting the hips too high can create tension in the shoulders and limit engagement of the core muscles. Aim to maintain a neutral spine and avoid overarching or rounding the back.",
        "tips": "Engage the Core: Focus on actively engaging the muscles of the core throughout the entire pose. Imagine drawing the navel toward the spine to create stability and support for the entire body. Maintain Proper Alignment: Pay attention to the alignment of the body, keeping the shoulders stacked directly over the elbows and the heels reaching back behind you. Avoid any sagging or lifting in the hips.",
        "video": "Cil7tOPh4qM"
    },
}


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
    elif body_part is not None:
        for pose in poses:
            print(pose['benefits'])
        sorted_poses = [pose for pose in poses if body_part.lower() in pose['benefits'].lower()]
    else:
        sorted_poses = poses
    
    return render_template('directory.html', poses=sorted_poses, sequences=sequences)

@app.route('/learn/<id>')
def learn(id=None):

    pose = data[id]

    return render_template('learn.html', pose=pose)


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug = True)
