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

def prompt_user_choice(msg: str, choices: list) -> str:
    while True:
        user_input = input(f"{msg} {choices}: ").strip().lower()

        if user_input in choices:
            return user_input

        print(f"Invalid choice: {user_input}")


def install_all(os_type):
    if os_type == "linux":
        platform = Linux()
    
    elif os_type == "macos":
        platform = MacOS()

    if prompt_user("Install shell configuration?"):
        platform.install_aliases()

        shell_choice = prompt_user_choice("Choose shell", ["oh-my-zsh", "minimal"])

        if shell_choice == "oh-my-zsh":
            platform.install_oh_my_zsh_conf()
        
        elif shell_choice == "minimal":
            platform.install_minimal_shell_conf()


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
