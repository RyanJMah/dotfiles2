#!/usr/bin/env bash

set -e

# Name of the image
IMAGE_NAME="debian11-test-env"
CONTAINER_NAME="debian11-test-env-container"

BUILDX_NAME="${IMAGE_NAME}-builder"

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
    docker buildx rm $BUILDX_NAME

    exit 0
fi

# Check if the --with-ssh flag was provided
WITH_SSH=0

for arg in "$@"; do
    if [[ "$arg" == "--with-ssh" ]]; then
        WITH_SSH=1
        break
    fi
done


cd ../../

set +e
docker buildx create --use --name mybuilder --driver docker-container --buildkitd-flags '--allow-insecure-entitlement security.insecure'
docker buildx inspect --bootstrap
set -e

# Build the Docker image
docker buildx build                         \
    -f test_environments/linux/Dockerfile   \
    --platform linux/amd64                  \
    --load                                  \
    -t $IMAGE_NAME .

# Clean up any existing containers
clean_container

# Extend the Docker image with SSH if requested
if [[ $WITH_SSH -eq 1 ]]; then

SSH_IMG_NAME="${IMAGE_NAME}-with-ssh"

sudo docker buildx build                         \
    -f test_environments/linux/withSSH.Dockerfile   \
    --build-arg TEST_ENV_BASE_IMG=$IMAGE_NAME       \
    --pull=false                               \
    --platform linux/amd64                  \
    --load                                  \
    -t $IMAGE_NAME .

# docker buildx build                                 \
#     --build-arg TEST_ENV_BASE_IMG=$IMAGE_NAME       \
#     -f test_environments/linux/withSSH.Dockerfile   \
#     --platform linux/amd64                          \
#     --load                                          \
#     -t $SSH_IMAGE_NAME .

# Use the SSH image
CONTAINER_NAME="${CONTAINER_NAME}-with-ssh"
IMAGE_NAME=$SSH_IMG_NAME

# Clean up any existing containers
clean_container

fi


docker run                  \
    -d                      \
    --platform linux/amd64  \
    --name $CONTAINER_NAME  \
    $IMAGE_NAME

# Attach to the container's shell, start in the home directory
set +e
docker exec -it $CONTAINER_NAME bash -c "cd ~/dotfiles2 && bash"
set -e
