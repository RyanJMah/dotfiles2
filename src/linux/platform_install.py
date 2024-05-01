import os
import sys
import subprocess

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform

class Linux(Platform):
    def install_nvim(self):
        cmd = """
        set -e

        # Neovim doesn't do builds for arm64, but we probably don't need it
        # anyways. However, I stil need to be able to test on my M2 Mac,
        # so just sudo apt install neovim for now.

        curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-linux64.tar.gz
        tar -xzf nvim-linux64.tar.gz

        rm nvim-linux64.tar.gz

        mkdir -p ~/.local
        mv nvim-linux64 ~/.local
        """

        self.exec_bash(cmd)


    def platform_specific_install(self):
        print("running platform specific install for linux...")
