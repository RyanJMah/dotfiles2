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
# stderr > /dev/null
docker buildx create --use --name mybuilder --driver docker-container --buildkitd-flags '--allow-insecure-entitlement security.insecure' > /dev/null 2>&1
docker buildx inspect --bootstrap > /dev/null 2>&1
set -e

# Build the Docker image
docker buildx build                         \
    -f test_environments/linux/Dockerfile   \
    --platform linux/amd64                  \
    --load                                  \
    -t $IMAGE_NAME .

# Clean up any existing containers
clean_container


docker run                  \
    -d                      \
    --platform linux/amd64  \
    --name $CONTAINER_NAME  \
    -p 2222:22              \
    $IMAGE_NAME


STARTING_DIR=/home/testuser/dotfiles2

if [[ $WITH_SSH -eq 1 ]]; then
    docker exec -it $CONTAINER_NAME bash -c "sudo ~/ssh_server.sh"

    # If with ssh, want to test the remote scripts, so remove the local dotfiles2 directory
    docker exec -it $CONTAINER_NAME bash -c "rm -rf ~/dotfiles2"

    STARTING_DIR=/home/testuser
fi

# Attach to the container's shell, start in the home directory
set +e
docker exec -it $CONTAINER_NAME bash -c "cd ${STARTING_DIR} && bash"
set -e
