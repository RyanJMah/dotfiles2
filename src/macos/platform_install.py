import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform

class MacOS(Platform):
    def install_nvim(self):
        cmd = """
        curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-macos.tar.gz

        xattr -c ./nvim-macos.tar.gz
        tar -xzf nvim-macos.tar.gz
        """

        self.exec_bash(cmd)

    def platform_specific_install(self):
        pass