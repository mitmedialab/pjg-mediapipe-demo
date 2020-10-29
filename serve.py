import subprocess
from flask import Flask, request
app = Flask(__name__)

# https://google.github.io/mediapipe/solutions/hands.html#desktop
hello_world_build_command = "GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world"
cpu_build_bash_command = "GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hand_tracking:hand_tracking_cpu"
gpu_build_bash_command = "GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hand_tracking:hand_tracking_gpu"
# https://google.github.io/mediapipe/getting_started/building_examples.html#option-1-running-on-cpu
cpu_run_command = "GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_cpu --calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_desktop_live.pbtxt"

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/hand')
def hand():
    video = request.files['file']
    if video.filename != '':
        video.save(video.filename)

    cmd = cpu_run_command + f'--input_video_path="{video.filename}" --output_video_path="out-{video.filename}"'
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
    print(f'error: {error}')
    # Write file to s3
    # Delete both files or stream them

if __name__ == '__main__':
    app.run(host='0.0.0.0')