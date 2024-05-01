import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from linux.platform_install import Linux
from macos.platform_install import MacOS

def prompt_user(msg: str) -> bool:
    while True:
        user_input = input(f"{msg} [Y/n]: ").strip().lower()

        if user_input in ["y", "n"]:
            return user_input == "y"


def install_all(os_type):
    if os_type == "linux":
        platform = Linux()
    
    elif os_type == "macos":
        platform = MacOS()


    if prompt_user("Install Neovim?"):
        platform.install_nvim()


    platform.platform_specific_install()
