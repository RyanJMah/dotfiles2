import os
import sys
import subprocess
from typing import Dict

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform

class Linux(Platform):
    def get_code_cmd(self) -> str:
        return "/usr/bin/code"

    def get_code_conf_dir(self) -> str:
        return f"{self.paths.HOME}/.config/Code/User"

    def platform_tmux_configure_flags(self) -> Dict[str, str]:
        return {
            "libevent": "--enable-static",
            "ncurses":  "--enable-static",
            "tmux":     "--enable-static"
        }

    def platform_specific_install(self):
        pass

    def install_aliases(self):
        super().install_aliases()

        cmd = f"""
        ln -sf {self.paths.DOTFILES_LINUX_DIR}/.platform_custom_aliases.sh {self.paths.HOME}/.platform_custom_aliases.sh
        """
        self.exec_bash(cmd)
