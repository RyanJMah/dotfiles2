import os
import sys
from tempfile import TemporaryDirectory

from app_paths import SRC_DIR
from app_paths import LocalPaths, RemotePaths
sys.path.append(SRC_DIR)

from dependencies import (
    check_dependencies,
    LOCAL_DEPENDENCIES,
    REMOTE_DEPENDENCIES
)
from shell_wrapper import LocalShell, RemoteShell

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


def install_all(os_type, remote, user, password, priv_key, port):
    if remote is not None:
        shell = RemoteShell(remote, user, port, password, priv_key)
        paths = RemotePaths(user)

        ok = True

        print("checking remote dependencies...")
        ok &= check_dependencies(shell, REMOTE_DEPENDENCIES["remote"])

        print("checking local dependencies...")
        ok &= check_dependencies(shell.local_shell, REMOTE_DEPENDENCIES["local"])

        if not ok:
            input("WARNING: Some dependencies are missing, press enter to continue...")

        # Push repo to remote
        this_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir  = os.path.dirname(this_dir)
        repo_dir = os.path.dirname(src_dir)

        with TemporaryDirectory() as tmp_dir:
            # compress
            cmd = f"""
            cd {repo_dir}

            tar -czvf {tmp_dir}/dotfiles2.tar.gz .
            """
            shell.local_shell.run(cmd)

            # push
            shell.put(f"{tmp_dir}/dotfiles2.tar.gz", paths.HOME)

            # remove local
            os.remove(f"{tmp_dir}/dotfiles2.tar.gz")

        # extract
        cmd = f"""
        mkdir -p dotfiles2
        tar -xzvf dotfiles2.tar.gz -C dotfiles2

        rm dotfiles2.tar.gz

        cd dotfiles2 && ls -l
        """
        shell.run(cmd)

        print("dotfiles2 repo successfully pushed to remote machine...")

    else:
        shell = LocalShell()
        paths = LocalPaths()

        if not check_dependencies(shell, LOCAL_DEPENDENCIES):
            input("WARNING: Some dependencies are missing, press enter to continue...")


    if os_type == "macos":
        platform = MacOS(shell, paths)
    else:
        platform = Linux(shell, paths)


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


    if prompt_user("Install Tmux?"):
        platform.install_tmux()


    if prompt_user("Install Tmux configuration?"):
        platform.install_tmux_conf()


    if prompt_user("Install VSCode configuration?"):
        platform.install_vscode_conf()


    if prompt_user("Install VSCode extensions?"):
        platform.install_vscode_extensions()


    if prompt_user("Install misc. configurations?"):
        platform.install_misc()


    if prompt_user("Run platform specific installation?"):
        platform.platform_specific_install()
