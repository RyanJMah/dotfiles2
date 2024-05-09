import os
from abc import ABC, abstractmethod

THIS_DIR      = os.path.dirname(os.path.abspath(__file__))
SRC_DIR       = os.path.dirname(THIS_DIR)
ROOT_DIR      = os.path.dirname(SRC_DIR)
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")

class Paths(ABC):
    @property
    @abstractmethod
    def HOME(self):
        pass

    @property
    @abstractmethod
    def ROOT_DIR(self):
        pass

    def __init__(self):

        self.SRC_DIR             = os.path.join(self.ROOT_DIR, "src")
        self.DOTFILES_DIR        = os.path.join(self.ROOT_DIR, "dotfiles")
        self.DOTFILES_COMMON_DIR = os.path.join(self.DOTFILES_DIR, "common")
        self.DOTFILES_LINUX_DIR  = os.path.join(self.DOTFILES_DIR, "linux")
        self.DOTFILES_MACOS_DIR  = os.path.join(self.DOTFILES_DIR, "macos")

class LocalPaths(Paths):
    @property
    def HOME(self):
        return os.path.expanduser("~")

    @property
    def ROOT_DIR(self):
        return ROOT_DIR


class RemotePaths(Paths):
    """
    In the remote case, we will scp dotfiles2 to $HOME on the remote machine. 
    """
    def __init__(self, user):
        self.user = user

        super().__init__()

    @property
    def HOME(self):
        return f"/home/{self.user}"

    @property
    def ROOT_DIR(self):
        return f"{self.HOME}/dotfiles2"
