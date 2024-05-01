import os
import sys

from paths import SRC_DIR
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


    if prompt_user("Install custom aliases?"):
        platform.install_aliases()


    if prompt_user("Install Neovim?"):
        platform.install_nvim()


    if prompt_user("Install Neovim configuration?"):
        platform.install_nvim_conf()


    if prompt_user("Install VSCode configuration?"):
        platform.install_vscode_conf()


    if prompt_user("Install VSCode extensions?"):
        platform.install_vscode_extensions()


    if prompt_user("Run platform specific installation?"):
        platform.platform_specific_install()
