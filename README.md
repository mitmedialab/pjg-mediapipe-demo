# pjg-mediapipe-demo
Demo of media pipe python integration with Django

## Server Setup

### GCP 
- Temporary Server (Dwayne's Personal) `gcloud beta compute ssh --zone "us-east4-c" "mediapipe-server" --project "mystical-slate-241320"`
- Follow https://google.github.io/mediapipe/getting_started/install.html#installing-on-debian-and-ubuntu
  - and https://dev.classmethod.jp/articles/mediapipe-install-on-aws-ec2-with-gpu-english/
- `GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`

### Docker / Local
- Taken from https://google.github.io/mediapipe/getting_started/install.html
- `docker build --tag=mediapipe .`
- `docker run -it --name mediapipe mediapipe:latest`
- `root@bca08b91ff63:/mediapipe# GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`

## Test Data
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_fist
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_other_heuristics
- https://a-counting-sign-language.s3.amazonaws.com/demos/main_demos_mp4/fist_only/12.mp4