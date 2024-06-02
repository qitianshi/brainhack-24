FROM python:3.8-alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Install any additional dependencies
RUN apk add --no-cache gcc musl-dev

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# pip gives a warning if you install packages as root
# set this flag to just ignore the warning
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /workspace

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# copy the rest of the files into the container
COPY src .

# start model service
CMD uvicorn api_service:app --port 5002 --host 0.0.0.0
