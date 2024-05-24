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

### Tag container for push

```bash
docker tag dingdongs-asr asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-asr:latest
```

```bash
docker tag dingdongs-nlp asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-nlp:latest
```

```bash
docker tag dingdongs-vlm asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-vlm:latest
```

### Push

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-asr:latest
```

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-nlp:latest
```

```bash
docker push asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-vlm:latest
```

### Submit

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-asr' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-asr:latest --container-health-route /health --container-predict-route /stt --container-ports 5001 --version-aliases default
```

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-nlp' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-nlp:latest --container-health-route /health --container-predict-route /extract --container-ports 5002 --version-aliases default
```

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-vlm' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-vlm:latest --container-health-route /health --container-predict-route /identify --container-ports 5004 --version-aliases default
```

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
