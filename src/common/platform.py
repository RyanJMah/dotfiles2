import subprocess
from abc import ABC, abstractmethod

class Platform(ABC):
    def exec_bash(self, cmd_str):
        for cmd in cmd_str.split("\n"):
            subprocess.run(cmd, shell=True, text=True)


    @abstractmethod
    def install_nvim(self):
        pass

    @abstractmethod
    def platform_specific_install(self):
        pass
