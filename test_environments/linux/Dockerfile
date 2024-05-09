# Use the official Debian 11 image as the base
FROM debian:11

RUN apt update

RUN apt install -y  \
    git             \
    sudo            \
    python3         \
    python3-pip     \
    curl            \
    bison

# Clean up cache to reduce image size
RUN apt clean && rm -rf /var/lib/apt/lists/*

# Create a new user and add to sudo group
RUN useradd -m testuser
RUN adduser testuser sudo

# Set password for the user
RUN echo 'testuser:pass' | chpasswd

# Copy files
RUN mkdir /home/testuser/dotfiles2

COPY src /home/testuser/dotfiles2/src
COPY dotfiles /home/testuser/dotfiles2/dotfiles
COPY resources /home/testuser/dotfiles2/resources

COPY install.py                             \
     quick_install.sh                       \
     requirements.txt                       \
     test_environments/linux/ssh_server.sh  \
     /home/testuser/dotfiles2/

RUN chown -R testuser:testuser /home/testuser

# Set default shell of testuser to bash
RUN chsh -s /bin/bash testuser

USER testuser

EXPOSE 22

# Do nothing forever
CMD ["bash", "-c", "while true; do sleep 30; done;"]
