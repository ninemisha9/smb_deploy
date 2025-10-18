FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    openssh-client \
    sshpass \
    curl \
    wget \
    vim \
    python3 \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY script.py .


CMD ["python3", "script.py"]