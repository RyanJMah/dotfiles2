from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

class Artifact(ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @property
    def filename(self) -> str:
        return self.url.split("/")[-1]


class RemoteArtifact(Artifact):
    def __init__(self, url: str):
        self._url = url

    @property
    def url(self) -> str:
        return self._url

class LocalArtifact(Artifact):
    def __init__(self, path: str):
        self._path = path

    @property
    def url(self) -> str:
        return f"file://{self._path}"

@dataclass
class TargetArtifacts:
    # oh-my-zsh
    oh_my_zsh_install_sh: Artifact

    # nvim
    nvim_tarball: Artifact

    # nvim conf dependencies
    ripgrep_tarball: Artifact
    xxd_c: Artifact
    xxd_makefile: Artifact

    # My personal vscode theme
    ryan_vscode_theme_vsix: Artifact

    # tmux and dependencies
    pkg_config_tarball: Artifact
    libevent_tarball: Artifact
    ncurses_tarball: Artifact
    tmux_tarball: Artifact

    # platform specific
    platform_artifacts: Dict[str, Artifact]
