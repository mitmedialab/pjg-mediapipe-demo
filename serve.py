import subprocess
from flask import Flask, request
app = Flask(__name__)

#https://google.github.io/mediapipe/solutions/hands.html#desktop
cpu_bash_command = "GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hand_tracking:hand_tracking_cpu"
gpu_bash_command = "GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hand_tracking:hand_tracking_gpu"


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/hand')
def hand():
    video = request.files['file']
    if video.filename != '':
        video.save(video.filename)

    cmd = cpu_bash_command + f'--input_video_path="{video.filename}" --output_video_path="out-{video.filename}"'
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
    print(f'error: {error}')

if __name__ == '__main__':
    app.run(host='0.0.0.0')