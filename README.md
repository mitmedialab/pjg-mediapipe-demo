# pjg-mediapipe-demo
Demo of media pipe python integration with Django

## Cloud Setup


### Account Setup
- STEP: Install [gcloud](https://cloud.google.com/sdk/docs/install) 
- STEP: `gcloud auth login` choose the appropriate GCP account
- STEP: `gcloud config set project a-counting-sign-language`
- STEP: Ensure you have IAM permissions to view Cloud Run, Compute Engine, Cloud Build and Artifact Repository in the appropriate GCP account


### Artifact Repository
- STEP: Enable Docker auth to GCP 
  - `gcloud auth configure-docker us-central1-docker.pkg.dev`
- NOTES: How to create a repo (already done)
- `gcloud artifacts repositories create REPO_NAME --repository-format=docker \
    --location=us-central1 --description="DESCRTIPTION"`
- NOTES: List repositories
  - `gcloud artifacts repositories list`
  - Or navigate to [Console](https://console.cloud.google.com/artifacts?authuser=1&project=a-counting-sign-language)


### Cloud Run
- NOTES: [Console](https://console.cloud.google.com/run?authuser=1&project=a-counting-sign-language)
- NOTES: [How service was configures](https://cloud.google.com/run/docs/configuring/containers)
- NOTES: [Setting environmental variables](https://cloud.google.com/run/docs/configuring/environment-variables) based 
on [sample](./env-sample)
- NOTES: [Quick Build](https://cloud.google.com/cloud-build/docs/quickstart-build)
- NOTES: [Quick Start Deploy](https://cloud.google.com/cloud-build/docs/quickstart-deploy)
- NOTES: [Automating Deploys](https://cloud.google.com/cloud-build/docs/deploying-builds/deploy-cloud-run) 


## Local Setup


### Env
- STEP: Setup your env file based on the [sample](./env-sample)


### Docker / Local


#### Preferred Approach (Must Do Cloud Setup Above)
- STEP: `docker pull us-central1-docker.pkg.dev/a-counting-sign-language/mediapipe/mediapipe`
- STEP: `docker pull us-central1-docker.pkg.dev/a-counting-sign-language/pjg-mediapipe-demo/pjg-mediapipe-demo`
- STEP: Building Demo Server Container
  - `docker-compose up`


#### Alternate 1: Pre-release Tarball (likely Outdated)
- STEP: Download the latest [tar.gz release](https://github.com/mitmedialab/pjg-mediapipe-demo/releases/tag/0.0.1) 
  - [Alternate link](https://drive.google.com/file/d/1Yjvdu08ujZdwVsBcYRSFhoyO75m90bVq/view?usp=sharing)
  - should be 3.32 GB unzipped
  - Unzip the file, should be 3.32 gb
- STEP: load the tar as a docker image with `docker load -i pjg-mediapipe-demo_mediapipe_web.v0.0.1.tar`
- STEP: Run the image which should be tagged as `pjg-mediapipe-demo_mediapipe_web:latest` and image sha `782f523505a4`
  - `docker run -p 8080:8080 --env-file .env 782f523505a4 python3 serve.py`
- NOTES: 
  - Release was generated with `docker save 'pjg-mediapipe-demo_mediapipe_web' > pjg-mediapipe-demo_mediapipe_web.v0.0.1.tar` and gzipped


#### Alternate 2: Local Build
- Build Mediapipe Container Locally
  - STEP: Taken from https://google.github.io/mediapipe/getting_started/install.html
  - STEP: In a sibling folder, `git clone git@github.com:mitmedialab/mediapipe.git`
    - `docker build --tag=mediapipe .`
    - add second tag `docker tag mediapipe us-central1-docker.pkg.dev/a-counting-sign-language/mediapipe/mediapipe`
      - Based on the following [instructions](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
  - STEP: Quick Test (optional)
    - `docker run -it --name mediapipe mediapipe:latest`
    - `root@bca08b91ff63:/mediapipe# GLOG_logtostderr=1 bazel run --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/hello_world:hello_world`
- Building Demo Server Container
  - STEP: `docker-compose up`
- How images are pushed manually
  - NOTES: `docker push us-central1-docker.pkg.dev/a-counting-sign-language/mediapipe/mediapipe`
  - NOTES: `docker pull us-central1-docker.pkg.dev/a-counting-sign-language/mediapipe/mediapipe`


## Testing - local
- STEP: `curl -d '{"archive_id": "126f8d71-3116-43b0-8cd5-d7c73cdf8185"}' -H 'Content-Type: application/json' localhost:8080/hand`
- Run time is 5-7min output is expected [here](https://s3.console.aws.amazon.com/s3/buckets/a-counting-sign-language-dev?region=us-east-1&prefix=46914194/126f8d71-3116-43b0-8cd5-d7c73cdf8185/&showversions=false)


### Test Data
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_fist
- https://a-counting-sign-staging.herokuapp.com/transcribe/test/test_other_heuristics
- https://a-counting-sign-language.s3.amazonaws.com/demos/main_demos_mp4/fist_only/12.mp4
- https://a-counting-sign-language.s3.amazonaws.com/demos/main_demos_mp4/fist_only/fist_only_demo_10_16_20.mp4
- https://a-counting-sign-language.s3.amazonaws.com/46914194/126f8d71-3116-43b0-8cd5-d7c73cdf8185/archive.mp4 


## Deployment
- STEP: `gcloud builds submit`

### Testing - cloud
- STEP: `curl -d '{"archive_id": "126f8d71-3116-43b0-8cd5-d7c73cdf8185"}' -H 'Content-Type: application/json' https://pjg-mediapipe-demo-czcfo4ghca-uc.a.run.app/hand` 

## Development
- ADD files in Dockerfile with COPY command
- Remove old containers with `docker rm [CONTAINER]` 
- Remove images containers with `docker rmi [IMAGE]` 
- Run `docker-compose build` to build docker with the file changes 
- Run `docker-compose up` to start docker with the file changes 
- Run in new terminal `docker docker exec -it [CONTAINER ID] /bin/bash`
- Run `ls` to see new files
- Run curl command or run script or whatever needs to occur appropriately 
