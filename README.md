# pjg-mediapipe-demo
Demo of media pipe python integration with Django

## Local Setup

### Env
- Setup your env file based on the [sample](./env-sample)

### Docker / Local

#### Option 1: Pre-releases
- Download the latest [tar.gz release](https://github.com/mitmedialab/pjg-mediapipe-demo/releases/tag/0.0.1) 
  - [Alternate link](https://drive.google.com/file/d/1Yjvdu08ujZdwVsBcYRSFhoyO75m90bVq/view?usp=sharing)
  - should be 3.32 GB unzipped
  - Unzip the file, should be 3.32 gb
- load the tar as a docker image with `docker load -i pjg-mediapipe-demo_mediapipe_web.v0.0.1.tar`
- Run the image which should be tagged as `pjg-mediapipe-demo_mediapipe_web:latest` and image sha `782f523505a4`
  - `docker run -p 8080:8080 --env-file .env 782f523505a4 python3 serve.py`
- Optional
  - Release was generated with `docker save 'pjg-mediapipe-demo_mediapipe_web' > pjg-mediapipe-demo_mediapipe_web.v0.0.1.tar` and gzipped

#### Option 2a: Building Mediapipe Container
- Taken from https://google.github.io/mediapipe/getting_started/install.html
- In a sibling folder, `git clone git@github.com:mitmedialab/mediapipe.git`
- `docker build --tag=mediapipe .`
- Quick Test (optional)
  - `docker run -it --name mediapipe mediapipe:latest`
  - `root@bca08b91ff63:/mediapipe# GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`

#### Option 2b: Building Demo Server Container
- `docker-compose up`

## Testing (based on Option 1 or 2)
- `curl -d '{"archive_id": "126f8d71-3116-43b0-8cd5-d7c73cdf8185"}' -H 'Content-Type: application/json' localhost:8080/hand`
- Run time is 5-7min output is expected [here](https://s3.console.aws.amazon.com/s3/buckets/a-counting-sign-language-dev?region=us-east-1&prefix=46914194/126f8d71-3116-43b0-8cd5-d7c73cdf8185/&showversions=false)

## Cloud Setup

### Cloud
- Install [gcloud](https://cloud.google.com/sdk/docs/install) 
- `gcloud auth login` choose the appropriate GCP account
- `gcloud config set project a-counting-sign-language`
- Ensure you have IAM permissions to view Cloud Run, Compute Engine, and Artifact Repository in the appropriate GCP account

### Artifact Repository
- Enable Docker push
  - `gcloud auth configure-docker us-central1-docker.pkg.dev`
- How to create a repo (only needed once)
- `gcloud artifacts repositories create REPO_NAME --repository-format=docker \
    --location=us-central1 --description="DESCRTIPTION"`
- List repositories
  - `gcloud artifacts repositories list`
  - Or navigate to [Console](https://console.cloud.google.com/artifacts?authuser=1&project=a-counting-sign-language)
- Assuming there is a local image as per Option 2a (already done)
  - Based on the following [instructions](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
  - `docker tag mediapipe us-central1-docker.pkg.dev/a-counting-sign-language/mediapipe/mediapipe`
  - `docker push us-central1-docker.pkg.dev/a-counting-sign-language/mediapipe/mediapipe`

### Cloud Run
- [Console](https://console.cloud.google.com/run?authuser=1&project=a-counting-sign-language)


## Test Data
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_fist
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_other_heuristics
- https://a-counting-sign-language.s3.amazonaws.com/demos/main_demos_mp4/fist_only/12.mp4
- https://a-counting-sign-language.s3.amazonaws.com/demos/main_demos_mp4/fist_only/fist_only_demo_10_16_20.mp4
- https://a-counting-sign-language.s3.amazonaws.com/46914194/126f8d71-3116-43b0-8cd5-d7c73cdf8185/archive.mp4 
