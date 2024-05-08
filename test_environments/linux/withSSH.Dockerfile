ARG TEST_ENV_BASE_IMG
FROM ${TEST_ENV_BASE_IMG}:latest

RUN apt update

# Install SSH server
RUN sudo apt update &&                      \
    sudo apt install -y openssh-server &&   \
    sudo apt clean &&                       \
    sudo rm -rf /var/lib/apt/lists/*

# Setup SSH server
RUN sudo mkdir /var/run/sshd

# Configure SSH daemon
RUN sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose the default SSH port
EXPOSE 22

# Start SSH service and keep container running
CMD ["/usr/sbin/sshd"]
