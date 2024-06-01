# Use the official Debian 11 image as the base
FROM debian:11

RUN apt update

RUN apt install -y  \
    zsh             \
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

# Set default shell of testuser to bash
RUN chsh -s /bin/bash testuser

# Copy files
RUN mkdir /home/testuser/dotfiles2

COPY requirements.txt /home/testuser/dotfiles2/requirements.txt
RUN pip3 install -r /home/testuser/dotfiles2/requirements.txt

COPY src /home/testuser/dotfiles2/src
COPY dotfiles /home/testuser/dotfiles2/dotfiles
COPY resources /home/testuser/dotfiles2/resources
COPY build /home/testuser/dotfiles2/build

COPY test_environments/linux/ssh_server.sh /home/testuser/ssh_server.sh

COPY install.py                             \
     quick_install.sh                       \
     /home/testuser/dotfiles2/


RUN chown -R testuser:testuser /home/testuser
USER testuser

EXPOSE 22

# Do nothing forever
CMD ["bash", "-c", "while true; do sleep 30; done;"]
