#!/usr/bin/env bash

set -e

# Name of the image
IMAGE_NAME="debian11-test-env"
CONTAINER_NAME="debian11-test-env-container"

function clean_container()
{
    set +e

    echo "Cleaning up container..."

    docker stop $CONTAINER_NAME > /dev/null 2>&1
    docker rm $CONTAINER_NAME   > /dev/null 2>&1

    set -e
}

clean_container

# Build the Docker image
docker build -t $IMAGE_NAME .

# Run the container in detached mode and remove it on exit
docker run -d --name $CONTAINER_NAME $IMAGE_NAME

# Wait a bit to ensure the container is fully up and running
sleep 2

# Attach to the container's shell, start in the home directory
docker exec -it $CONTAINER_NAME bash -c "cd ~ && bash"

clean_container
