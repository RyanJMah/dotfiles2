import os
from abc import ABC, abstractmethod

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)

class Paths(ABC):
    @property
    @abstractmethod
    def ROOT_DIR(self):
        pass

    def __init__(self):
        self.HOME = "$HOME"

        self.SRC_DIR             = os.path.join(self.ROOT_DIR, "src")
        self.DOTFILES_DIR        = os.path.join(self.ROOT_DIR, "dotfiles")
        self.DOTFILES_COMMON_DIR = os.path.join(self.DOTFILES_DIR, "common")
        self.DOTFILES_LINUX_DIR  = os.path.join(self.DOTFILES_DIR, "linux")
        self.DOTFILES_MACOS_DIR  = os.path.join(self.DOTFILES_DIR, "macos")

class LocalPaths(Paths):
    @property
    def ROOT_DIR(self):
        return os.path.dirname( SRC_DIR )


class RemotePaths(Paths):
    """
    In the remote case, we will scp dotfiles2 to $HOME on the remote machine. 
    """

    @property
    def ROOT_DIR(self):
        return f"{self.HOME}/dotfiles2"
