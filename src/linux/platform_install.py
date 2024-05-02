import os
import sys
import subprocess

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform
from common.paths import HOME, DOTFILES_LINUX_DIR

class Linux(Platform):
    def install_nvim(self):
        cmd = """
        curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-linux64.tar.gz
        tar -xzf nvim-linux64.tar.gz

        rm nvim-linux64.tar.gz

        mkdir -p {HOME}/.local
        mv nvim-linux64 {HOME}/.local/nvim
        """

        self.exec_bash(cmd)

    def install_aliases(self):
        super().install_aliases()

        cmd = """
        ln -sf {DOTFILES_LINUX_DIR}/platform_custom_aliases.sh {HOME}/platform_custom_aliases.sh
        """
        self.exec_bash(cmd)

    def platform_specific_install(self):
        print("running platform specific install for linux...")
