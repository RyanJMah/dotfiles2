import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

def prompt_user(msg: str) -> bool:
    while True:
        user_input = input(f"{msg} [Y/n]: ").strip().lower()

        if user_input in ["y", "n"]:
            return user_input == "y"


def install_all(os_type):
    if os_type == "linux":
        import linux.platform_install as platform
    
    elif os_type == "macos":
        import macos.platform_install as platform


    if prompt_user("Install Neovim?"):
        platform.install_neovim()


    platform.platform_specific_install()
