# Use the official Debian 11 image as the base
FROM debian:11

RUN apt update

RUN apt install -y  \
    git             \
    sudo

# Clean up cache to reduce image size
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Create a new user and add to sudo group
RUN useradd -m testuser
RUN usermod -aG sudo testuser

USER testuser


# Do nothing forever
CMD ["bash", "-c", "while true; do sleep 30; done;"]
