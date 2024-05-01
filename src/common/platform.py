import os
import subprocess
from abc import ABC, abstractmethod

from paths import DOTFILES_COMMON_DIR

class Platform(ABC):
    def exec_bash(self, cmd_str):
        for cmd in cmd_str.split("\n"):
            subprocess.run(cmd, shell=True, text=True)

    @abstractmethod
    def install_nvim(self):
        pass

    def install_nvim_conf(self):
        home = os.path.expanduser("~")

        cmd = f"""
        mkdir -p {home}/.config/nvim
        
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/.vimrc   {home}/.vimrc
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/init.vim {home}/.config/nvim/init.vim

        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/terminal-vimrc.vim {home}/terminal-vimrc.vim
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/vscode-vimrc.vim   {home}/vscode-vimrc.vim
        """

        self.exec_bash(cmd)

    @abstractmethod
    def platform_specific_install(self):
        pass
