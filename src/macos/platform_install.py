import os
import sys
from typing import Dict

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform

class MacOS(Platform):
    def install_nvim(self):
        cmd = f"""
        curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-macos.tar.gz

        xattr -c ./nvim-macos.tar.gz
        tar -xzf nvim-macos.tar.gz

        mkdir -p {self.paths.HOME}/.local
        mv nvim-macos {self.paths.HOME}/.local/nvim
        """

        self.exec_bash(cmd)

    def get_code_conf_dir(self) -> str:
        return f"{self.paths.HOME}/Library/Application\\ Support/Code/User"

    def get_code_cmd(self) -> str:
        return r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code"

    def get_ripgrep_download_url(self) -> str:
        return "https://github.com/BurntSushi/ripgrep/releases/download/14.1.0/ripgrep-14.1.0-aarch64-apple-darwin.tar.gz"

    def platform_tmux_configure_flags(self) -> Dict[str, str]:
        return {
            "tmux": "--enable-utf8proc"
        }
    
    def platform_specific_install(self):
        pass

    def install_aliases(self):
        super().install_aliases()

        cmd = f"""
        ln -sf {self.paths.DOTFILES_MACOS_DIR}/.platform_custom_aliases.sh {self.paths.HOME}/.platform_custom_aliases.sh
        """
        self.exec_bash(cmd)
