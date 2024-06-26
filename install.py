import os
import sys
import click
from typing import Tuple, Type
from tempfile import TemporaryDirectory

from src.common.shell_wrapper import LocalShell, RemoteShell, Shell
from src.common.app_paths import LocalPaths, RemotePaths, Paths
from src.common.artifacts import Artifact, RemoteArtifact, LocalArtifact, TargetArtifacts

from src.common.dependencies import (
    check_dependencies,
    LOCAL_DEPENDENCIES,
    REMOTE_DEPENDENCIES
)

from src.linux.linux_install import Linux
from src.macos.macos_install import MacOS

from src.common.artifact_urls import (
    LINUX_DOWNLOADABLE_ARTIFACTS,
    MACOS_DOWNLOADABLE_ARTIFACTS,
    LINUX_LOCAL_ARTIFACTS,
    MACOS_LOCAL_ARTIFACTS
)

REPO_DIR = os.path.dirname(os.path.abspath(__file__))


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


def init_remote(remote, user, password, priv_key, port) -> Tuple[Shell, Paths]:
    shell = RemoteShell(remote, user, port, password, priv_key)
    paths = RemotePaths(shell)

    ok = True

    print("checking remote dependencies...")
    ok &= check_dependencies(shell, REMOTE_DEPENDENCIES["remote"])

    print("checking local dependencies...")
    ok &= check_dependencies(shell.local_shell, REMOTE_DEPENDENCIES["local"])

    if not ok:
        input("WARNING: Some dependencies are missing, press enter to continue...")

    # Push repo to remote
    repo_dir = REPO_DIR

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

    return shell, paths


def init_local() -> Tuple[Shell, Paths]:
    shell = LocalShell()
    paths = LocalPaths()

    if not check_dependencies(shell, LOCAL_DEPENDENCIES):
        input("WARNING: Some dependencies are missing, press enter to continue...")

    return shell, paths


@click.command()
@click.option( "--os", "os_type", required=True, type=click.Choice(['linux', 'macos']), help="Operating system" )
@click.option( "--remote", default=None, type=str, help="Remote hostname or IP address" )
@click.option( "--user", default=None, type=str, help="Remote username" )
@click.option( "--password", default=None, type=str, help="Remote password" )
@click.option( "--priv-key", default=None, type=str, help="Remote ssh private key" )
@click.option( "--port", default=22, type=int, help="Remote port" )
@click.option( "--artifacts-tarball", default=None, type=str, help="Path to the artifacts tarball" )
def main(os_type, remote, user, password, priv_key, port, artifacts_tarball):
    # Validate arguments

    # Only linux and macos are supported
    assert( os_type in ["linux", "macos"] )

    # Cannot be both remote and artifacts-tarball
    assert( (remote is None) or (artifacts_tarball is None) )

    # If remote is specified, user must be specified
    assert( (remote is None) or (user is not None) )

    # Remote only supported on linux
    assert( (remote is None) or (os_type == "linux") )

    # Make sure tarball is .tar.gz
    assert( (artifacts_tarball is None) or (artifacts_tarball.endswith(".tar.gz")) )


    if remote is not None:
        shell, paths = init_remote(remote, user, password, priv_key, port)

    else:
        shell, paths = init_local()


    tarball_dir: str

    # Extract artifacts tarball
    if artifacts_tarball is not None:
        # get the name of the tarball without .tar.gz
        tarball_name = os.path.basename(artifacts_tarball).replace(".tar.gz", "")

        # Create the directory to extract the tarball
        tarball_dir = os.path.join(paths.BUILD_DIR, tarball_name)
        os.makedirs(tarball_dir, exist_ok=True)

        # Extract the tarball
        shell.run(f"tar -xvzf {artifacts_tarball} -C {paths.BUILD_DIR}/{tarball_name}")


    if os_type == "macos":
        if artifacts_tarball is None:
            # Downloadable artifacts
            target_artifacts = TargetArtifacts.from_target_urls(MACOS_DOWNLOADABLE_ARTIFACTS, RemoteArtifact)
        else:
            # Local artifacts
            target_artifacts = TargetArtifacts.from_target_urls( MACOS_LOCAL_ARTIFACTS,
                                                                 lambda filename: LocalArtifact(tarball_dir, filename) )

        platform = MacOS(shell, paths, target_artifacts)

    else:
        if artifacts_tarball is None:
            # Downloadable artifacts
            target_artifacts = TargetArtifacts.from_target_urls(LINUX_DOWNLOADABLE_ARTIFACTS, RemoteArtifact)
        else:
            # Local artifacts
            target_artifacts = TargetArtifacts.from_target_urls( LINUX_LOCAL_ARTIFACTS,
                                                                 lambda filename: LocalArtifact(tarball_dir, filename) )

        platform = Linux(shell, paths, target_artifacts)


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


if __name__ == '__main__':
    main()
