import os
import subprocess
from abc import ABC, abstractmethod

from paths import DOTFILES_COMMON_DIR, HOME

class Platform(ABC):
    def exec_bash(self, cmd_str):
        for cmd in cmd_str.split("\n"):
            try:
                subprocess.run(cmd, shell=True, text=True, check=True)
            
            except subprocess.CalledProcessError as e:
                print(f"ERROR: {cmd}: {e}")

    def install_aliases(self):
        cmd = f"""
        ln -sf {DOTFILES_COMMON_DIR}/.custom_aliases {HOME}/.custom_aliases
        """

        self.exec_bash(cmd)

    @abstractmethod
    def install_nvim(self):
        pass

    def install_nvim_conf(self):
        cmd = f"""
        mkdir -p {HOME}/.config/nvim
        
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/.vimrc   {HOME}/.vimrc
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/init.vim {HOME}/.config/nvim/init.vim

        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/terminal-vimrc.vim {HOME}/terminal-vimrc.vim
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/vscode-vimrc.vim   {HOME}/vscode-vimrc.vim
        """

        self.exec_bash(cmd)

    @abstractmethod
    def install_vscode_conf(self):
        pass

    @abstractmethod
    def install_vscode_extensions(self):
        pass

    @abstractmethod
    def platform_specific_install(self):
        pass
