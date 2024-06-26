import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, TypeVar, Type

T = TypeVar('T')

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
    def __init__(self, file_dir: str, filename: str):
        self._path = os.path.join(os.path.abspath(file_dir), filename)

    @property
    def url(self) -> str:
        return f"file://{self._path}"


@dataclass
class TargetArtifacts(Generic[T]):
    # oh-my-zsh
    oh_my_zsh_install_sh: T

    # nvim
    nvim_tarball: T

    # nvim conf dependencies
    ripgrep_tarball: T
    xxd_c: T
    xxd_makefile: T

    # My personal vscode theme
    ryan_vscode_theme_vsix: T

    # tmux and dependencies
    pkg_config_tarball: T
    libevent_tarball: T
    ncurses_tarball: T
    tmux_tarball: T

    # platform specific
    platform_artifacts: Dict[str, T]


    @classmethod
    def from_target_urls(cls, target_urls: "TargetArtifacts[str]", artifact_class: Type[Artifact]) -> "TargetArtifacts[Artifact]":
        return cls(
            oh_my_zsh_install_sh = artifact_class(target_urls.oh_my_zsh_install_sh),

            nvim_tarball = artifact_class(target_urls.nvim_tarball),

            ripgrep_tarball = artifact_class(target_urls.ripgrep_tarball),
            xxd_c = artifact_class(target_urls.xxd_c),
            xxd_makefile = artifact_class(target_urls.xxd_makefile),

            ryan_vscode_theme_vsix = artifact_class(target_urls.ryan_vscode_theme_vsix),

            pkg_config_tarball = artifact_class(target_urls.pkg_config_tarball),
            libevent_tarball = artifact_class(target_urls.libevent_tarball),
            ncurses_tarball = artifact_class(target_urls.ncurses_tarball),
            tmux_tarball = artifact_class(target_urls.tmux_tarball),

            platform_artifacts = {k: artifact_class(v) for k, v in target_urls.platform_artifacts.items()}
        )
