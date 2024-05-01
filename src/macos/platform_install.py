import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform
from common.paths import DOTFILES_COMMON_DIR, HOME

class MacOS(Platform):
    def install_nvim(self):
        cmd = """
        curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-macos.tar.gz

        xattr -c ./nvim-macos.tar.gz
        tar -xzf nvim-macos.tar.gz
        """

        self.exec_bash(cmd)

    def install_vscode_conf(self):
        cmd = f"""
        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/settings.json    {HOME}/Library/Application\ Support/Code/User/settings.json
        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/keybindings.json {HOME}/Library/Application\ Support/Code/User/keybindings.json
        """

        self.exec_bash(cmd)

    def platform_specific_install(self):
        pass