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
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-nlp' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-nlp:latest --container-health-route /health --container-predict-route /stt --container-ports 5001 --version-aliases default
```

```bash
gcloud ai models upload --region asia-southeast1 --display-name 'dingdongs-vlm' --container-image-uri asia-southeast1-docker.pkg.dev/dsta-angelhack/repository-dingdongs/dingdongs-vlm:latest --container-health-route /health --container-predict-route /stt --container-ports 5001 --version-aliases default
```
