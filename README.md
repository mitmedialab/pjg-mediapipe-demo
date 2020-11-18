# pjg-mediapipe-demo
Demo of media pipe python integration with Django

## Server Setup

### Env
- Setup your env file based on the [sample](./env-sample)

### Docker / Local

#### Pre-releases
- Release was generated with `docker save 'pjg-mediapipe-demo_mediapipe_web' > pjg-mediapipe-demo_mediapipe_web.v0.0.1.tar` 
  - and gzipped
- Download the latest [tar.gz release](https://github.com/mitmedialab/pjg-mediapipe-demo/releases/tag/0.0.1)
- Unzip the file
- load the tar as a docker image with `docker load pjg-mediapipe-demo_mediapipe_web.v0.0.1.tar`
- Run the image which should be tagged as `pjg-mediapipe-demo_mediapipe_web:latest` and image sha `782f523505a4`
  - `docker run -p 8080:8080 --env-file .env 782f523505a4 python3 serve.py`

#### Building Mediapipe Container
- Taken from https://google.github.io/mediapipe/getting_started/install.html
- In a sibling folder, `git clone git@github.com:mitmedialab/mediapipe.git`
- `docker build --tag=mediapipe .`
- Quick Test (optiona1)
  - `docker run -it --name mediapipe mediapipe:latest`
  - `root@bca08b91ff63:/mediapipe# GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`

#### Building Demo Server Container
- `docker-compose up`
- `curl -d '{"archive_id": "126f8d71-3116-43b0-8cd5-d7c73cdf8185"}' -H 'Content-Type: application/json' localhost:8080/hand`
- Run time is 5-7min output is expected [here](https://s3.console.aws.amazon.com/s3/buckets/a-counting-sign-language-dev?region=us-east-1&prefix=46914194/126f8d71-3116-43b0-8cd5-d7c73cdf8185/&showversions=false)

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