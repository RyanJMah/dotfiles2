# Use the official Debian 11 image as the base
FROM debian:11

# Update the package list
RUN apt update

# Install Git
RUN apt install -y git

# Clean up cache to reduce image size
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Do nothing forever
CMD ["bash", "-c", "while true; do sleep 30; done;"]
