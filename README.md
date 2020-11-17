# pjg-mediapipe-demo
Demo of media pipe python integration with Django

## Server Setup

### Docker / Local

#### Mediapipe Container
- Taken from https://google.github.io/mediapipe/getting_started/install.html
- In a sibling folder, `git clone git@github.com:mitmedialab/mediapipe.git`
- `docker build --tag=mediapipe .`
- Quick Test (optiona1)
  - `docker run -it --name mediapipe mediapipe:latest`
  - `root@bca08b91ff63:/mediapipe# GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`

#### Demo Server Container
- `docker-compose up`
- `curl -d '{"archive_id": "013bc8ff-f069-44d9-af77-d170acd1c9c6"}' -H 'Content-Type: application/json' localhost:8080/hand`

### Cloud Run
- ...

### Temporary GCP Server
- (Dwayne's Personal) `gcloud beta compute ssh --zone "us-east4-c" "mediapipe-server" --project "mystical-slate-241320"`
- Follow https://google.github.io/mediapipe/getting_started/install.html#installing-on-debian-and-ubuntu
  - and https://dev.classmethod.jp/articles/mediapipe-install-on-aws-ec2-with-gpu-english/
- `GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`


## Test Data
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_fist
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_other_heuristics
- https://a-counting-sign-language.s3.amazonaws.com/demos/main_demos_mp4/fist_only/12.mp4