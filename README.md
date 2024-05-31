# dingdongs
"Dingdongs" can be traced back to Old English and Middle Dutch. The term "ding" originates from the Old English "dingan," meaning to strike or hit, often used to describe the sound of a bell. The term "dong" comes from the Middle Dutch "donckus," which refers to the sound a duck makes when hitting the water at or above the von Plonck ducking velocity. Combining these elements, "Dingdongs" historically represents a harmonious and impactful sound, symbolizing our aim to make a resonant impact at BrainHack 2024.

## Docker cheatsheet

### Build

```bash
docker build -t dingdongs-asr .
```

```bash
docker build -t dingdongs-nlp .
```

```bash
docker build -t dingdongs-vlm .
```

```bash
docker build -t dingdongs-autonomy .
```

```bash
docker build -t dingdongs-main .
```

### Run

(run without `-d` to show debug info)

```bash
docker run -p 5001:5001 --gpus all -d dingdongs-asr
```

```bash
docker run -p 5002:5002 --gpus all -d dingdongs-nlp
```

```bash
docker run -p 5004:5004 --gpus all -d dingdongs-vlm⁠
```

```bash
docker run -p 5003:5003 dingdongs-autonomy
```

```bash
docker run -p 5005:5005 dingdongs-main
```

### View running containers

```bash
docker ps
```

### Stop a container

(but doesn't remove it)

```bash
docker kill CONTAINER-ID
```

### View all images

```bash
docker images
```

### Remove an image

```bash
docker rmi dingdongs-asr
```

```bash
docker rmi dingdongs-nlp
```

```bash
docker rmi dingdongs-vlm
```

```bash
docker rmi dingdongs-autonomy
```

```bash
docker rmi dingdongs-main
```

### Remove a container

(u shld kill it first)

```bash
docker rm CONTAINER_NAME 
```

### Remove all images and containers

```bash
# Stop all running containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Remove all volumes (optional)
docker volume rm $(docker volume ls -q)

# Remove all networks (optional)
docker network rm $(docker network ls -q)

# Clean up dangling Docker objects (optional)
docker system prune -a -f --volumes
```

### Tag images for push to artifact registry (Finals)

```bash
docker tag dingdongs-asr asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-asr:finals
```

```bash
docker tag dingdongs-asr asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-nlp:finals
```

```bash
docker tag dingdongs-asr asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-vlm:finals
```

```bash
docker tag dingdongs-asr asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-autonomy:finals
```

```bash
docker tag dingdongs-asr asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-main:finals
```

### Push images to artifact registry (Finals)

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-asr:finals
```

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-nlp:finals
```

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-vlm:finals
```

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-autonomy:finals
```

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-main:finals
```

### Submit

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-asr' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-asr:finals --container-health-route /health --container-predict-route /stt --container-ports 5001 --version-aliases default
```

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-nlp' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-nlp:finals --container-health-route /health --container-predict-route /extract --container-ports 5002 --version-aliases default
```

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-vlm' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-vlm:finals --container-health-route /health --container-predict-route /identify --container-ports 5004 --version-aliases default
```

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-vlm' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-autonomy:finals --container-health-route /health --container-predict-route /identify --container-ports 5003 --version-aliases default
```

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-vlm' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-main:finals --container-health-route /health --container-predict-route /identify --container-ports 5005 --version-aliases default
```

## Creating local simulator for finals

### Building the simulator

build the simulator + competition server from the top-level directory by running:

```bash
docker build -t competition .
```

### Running the simulator

You can run the simulator + competition server from the top-level directory by running:

```bash
docker run -p 8000:8000 competition
```

access `localhost:8000` from browser machine.

### Running containers with Docker Compose

```bash
# start all the services
docker compose up

# force a build of all services and start them afterwards
docker compose up --build

# take down all the services
docker compose down

# start a particular docker compose file by name (it defaults to `docker-compose.yml` if not indicated)
docker compose -f docker-compose-finals.yml up
```

### testing
Create an `.env` file based on the provided `.env.example` file, and update it accordingly:

- `COMPETITION_IP = "172.17.0.1"` on Linux, `"host.docker.internal"` otherwise
- `LOCAL_IP = "172.17.0.1"` on Linux, `"host.docker.internal"` otherwise
- `USE_ROBOT = "false"`

Then run `docker compose up`. This should start the competition server locally, as well as the rest of the services accordingly to connect to it.


## Tagging & releases

So that we can quickly rollback to an old code 

1. Submit your code first and get the scores
2. Commit everything you need (except any binary files or ginormous text files which should be ignored)
3. Tag the correct commit with the scores and the file structure (using `tree`). By default it tags the commit that `HEAD` points to, but you can `git log --oneline` and choose a different commit.

   ```bash
   git tag -a asr-v1.0 -m "Descriptive tag title
   Accuracy: 1.00000000
   Speed: 1.00000000
   Tree:
   .
   ├── Dockerfile
   ├── README.md
   ├── model
   │   ├── config.json
   │   ├── pytorch_model.bin
   │   └── tokenizer
   │       ├── merges.txt
   │       ├── special_tokens_map.json
   │       ├── tokenizer_config.json
   │       └── vocab.json
   ├── requirements.txt
   └── src
       ├── NLPManager.py
       └── api_service.py"
   ```
   
5. Push the tag to GitHub

   ```bash
   git push origin asr-v1.0
   ```
   
7. Create the release and upload
    1. Go to [Tags](https://github.com/qitianshi/brainhack-24/tags) and click the one you just created
    2. For the title and message just copy paste from your tag message lol
    3. Check the "Set as pre-release" checkbox
    4. Download the binary files from Vertex, and upload them here. The idea is that we should keep every single file, so we can quickly checkout a previous tag, and immediately build and submit 

### Versioning

* Follow semantic versioning (semver): major.minor.patch.
    * Major changes: Completely different methodology (e.g., switching from QA to NER for NLP).
    * Minor changes: Significant improvements (e.g., retrained model).
    * Patch changes: Small adjustments (e.g., minor code tweaks).
* Ensure the tag is on the commit that represents a complete, ready-to-submit state.
* Tags do not need to be sequential. You can tag earlier versions if you made an adjustment to a previous version.
* If this is the "baseline" submission (e.g. using a non-fine tuned model, using stupid methods) then we put as v0, otherwise the first major version should be v1
* The next minor version after v1.9 is v1.10 NOT v2.0 jkalshdfljkbsdfljkhsldfjh
