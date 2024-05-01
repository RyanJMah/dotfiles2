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

if [[ $1 == "clean" ]]; then
    clean_container
    exit 0
fi

cd ../../

# Build the Docker image
docker buildx build                         \
    -f test_environments/linux/Dockerfile   \
    --platform linux/amd64                  \
    --load                                  \
    -t $IMAGE_NAME .

# Clean up any existing containers
clean_container

# Run the container in detached mode and remove it on exit
docker run                  \
    -d                      \
    --platform linux/amd64  \
    --name $CONTAINER_NAME  \
    $IMAGE_NAME

# Attach to the container's shell, start in the home directory
set +e
docker exec -it $CONTAINER_NAME bash -c "cd ~/dotfiles2 && bash"
set -e
