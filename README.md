# pjg-mediapipe-demo
Demo of media pipe python integration with Django

# Server Setup
- Follow https://google.github.io/mediapipe/getting_started/install.html#installing-on-debian-and-ubuntu
- `GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`

# Docker
- Taken from https://google.github.io/mediapipe/getting_started/install.html
- `docker build --tag=mediapipe .`
- `docker run -it --name mediapipe mediapipe:latest`
- `root@bca08b91ff63:/mediapipe# GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`
