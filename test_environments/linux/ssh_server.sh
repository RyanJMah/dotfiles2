# Install SSH server
sudo apt update
sudo apt install -y openssh-server

# Setup SSH server
sudo mkdir -p /var/run/sshd

# Configure SSH daemon to allow password login for "testuser"
# Ensure that password authentication is enabled
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

sudo service ssh start
