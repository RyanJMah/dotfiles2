import os
import sys
from typing import Dict

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform

class MacOS(Platform):
    def get_nvim_download_url(self) -> str:
        return "https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-macos.tar.gz"

    def get_code_conf_dir(self) -> str:
        return f"{self.paths.HOME}/Library/Application\\ Support/Code/User"

    def get_code_cmd(self) -> str:
        return r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code"

    def get_ripgrep_download_url(self) -> str:
        return "https://github.com/BurntSushi/ripgrep/releases/download/14.1.0/ripgrep-14.1.0-aarch64-apple-darwin.tar.gz"

    def platform_tmux_configure_flags(self) -> Dict[str, str]:
        return {
            "libevent": "--enable-shared",
            "ncurses": "--with-shared",
            "tmux": "--enable-utf8proc"
        }

    def install_tmux(self):
        # Install utf8proc first
        cmd = f"""
        set -e
        curl -LO https://github.com/JuliaStrings/utf8proc/releases/download/v2.9.0/utf8proc-2.9.0.tar.gz
        tar -xzf utf8proc-*.tar.gz

        cd utf8proc-*

        make prefix={self.paths.HOME}/.local install

        cd ..
        rm -r utf8proc-*
        """
        self.exec_bash(cmd)

        super().install_tmux()
    
    def platform_specific_install(self):
        pass

    def install_aliases(self):
        super().install_aliases()

        cmd = f"""
        ln -sf {self.paths.DOTFILES_MACOS_DIR}/.platform_custom_aliases.sh {self.paths.HOME}/.platform_custom_aliases.sh
        """
        self.exec_bash(cmd)
