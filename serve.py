import subprocess
import os
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from flask import Flask, request, Response
app = Flask(__name__)
PORT = os.getenv("PORT", default=8080)

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
import botocore
import boto3
s3 = boto3.resource('s3')

os.environ["GLOG_logtostderr"]="1"
# https://google.github.io/mediapipe/solutions/hands.html#desktop
hello_world_build_command = "bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world"
cpu_build_bash_command = "bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hand_tracking:hand_tracking_cpu"
gpu_build_bash_command = "bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hand_tracking:hand_tracking_gpu"
# https://google.github.io/mediapipe/getting_started/building_examples.html#option-1-running-on-cpu
cpu_run_command = "bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_cpu --calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_desktop_live.pbtxt"


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/hand', methods=['POST'])
def hand():
    #video = request.files['file']
    # if video.filename != '':
    #     video.save(video.filename)

    try:
        data = request.get_json()
        logger.debug(data)
        if not 'archive_id' in data:
            logger.warn('Missing field: archive_id')
            return Response("Missing field: archive_id", status=400)
        archive_id = data['archive_id']
        source_object_key = f'46914194/{archive_id}/archive.mp4'
        processed_object_key = f'46914194/{archive_id}/processed.mp4'
        source_local_path = f'/media/{archive_id}-source.mp4'
        processed_local_path = f'/media/{archive_id}-processed.mp4'
        s3.Bucket(S3_BUCKET_NAME).download_file(source_object_key, source_local_path)
    except botocore.exceptions.ClientError as download_error:
        if download_error.response['Error']['Code'] == 'NoSuchKey':
            logger.warn('No object found in bucket - returning empty')
            return Response("S3 Path Does Not Exist", status=400)
        else:
           logger.error(f'{download_error.response["Error"]["Code"]}: {download_error.response["Error"]["Message"]}')
           return Response("Not Found", status=404)

    cmd = cpu_run_command + f' --input_video_path="{source_local_path}" --output_video_path="{processed_local_path}"'
    logger.info(cmd)
    #TODO: subprocess function is not working.Would prefer as its the recommended approach
    #process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    #output, process_error = process.communicate()
    #logger.info(output)
    os.popen(cmd).read()
    # if process_error:
    #     logger.error(f'error: {process_error}')
    #     return Response("Mediapipe Processing failed", status=500)

    try:
        s3.Bucket(S3_BUCKET_NAME).upload_file(processed_local_path, processed_object_key)
    # except boto3.S3UploadFailedError as upload_error:
    #     logger.error(f'error: {upload_error}')
    #     return Response("S3 Upload error", status=500)
    except botocore.exceptions.ClientError as generic_error:
        logger.error(f'{generic_error.response["Error"]["Code"]}: {generic_error.response["Error"]["Message"]}')
        return Response("Internal Server Error", status=500)

    try:
        os.remove(processed_local_path)
    except OSError as os_error:
        logger.error(f'Error: {os_error.filename} {os_error.strerror}')
        return Response("Internal Server Error", status=500)

    return Response("{'a':'b'}", status=201, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)