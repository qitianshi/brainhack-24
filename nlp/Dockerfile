FROM python:3.8-alpine

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
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# copy the rest of the files into the container
COPY src .

# start model service
CMD uvicorn api_service:app --port 5002 --host 0.0.0.0
