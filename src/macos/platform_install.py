import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform
from common.paths import HOME, DOTFILES_COMMON_DIR, DOTFILES_MACOS_DIR

class MacOS(Platform):
    def install_nvim(self):
        cmd = f"""
        curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-macos.tar.gz

        xattr -c ./nvim-macos.tar.gz
        tar -xzf nvim-macos.tar.gz

        mkdir -p {HOME}/.local
        mv nvim-macos {HOME}/.local/nvim
        """

        self.exec_bash(cmd)

    def install_aliases(self):
        super().install_aliases()

        cmd = """
        ln -sf {DOTFILES_MACOS_DIR}/platform_custom_aliases.sh {HOME}/platform_custom_aliases.sh
        """
        self.exec_bash(cmd)

    def get_code_conf_dir(self) -> str:
        return f"{HOME}/Library/Application\\ Support/Code/User"

    def get_code_cmd(self) -> str:
        return r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code"

    def platform_specific_install(self):
        pass