# Fall detector


### Prerequisites

* pip
  ```sh
  pip install -r requirements.txt
  ```

### Fast API

* pyhton
  ```sh
  python fall_detector/fall_detector/api/fast.py
  ```

### Docker

* docker
  ```sh
  docker build -f "DockerFile" -t $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$GCP_ARTIFACT/$IMAGE_NAME:$IMAGE_TAG .
  ```
* launch locally
  ```sh
  docker-compose -up
  ```

* GCP
  ```sh
  gcloud run services replace gcloud.yaml
  ```
