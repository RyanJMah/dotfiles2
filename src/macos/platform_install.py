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

    def install_vscode_conf(self):
        vscode_dir = f"{HOME}/Library/Application\\ Support/Code/User"

        cmd = f"""
        mkdir -p {vscode_dir}

        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/settings.json    {vscode_dir}/settings.json
        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/keybindings.json {vscode_dir}/keybindings.json
        """

        self.exec_bash(cmd)

    def install_vscode_extensions(self):
        extensions_txt = os.path.join(DOTFILES_COMMON_DIR, "vscode_extensions.txt")

        code = r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code"

        with open(extensions_txt, "r") as f:
            extensions = f.read().splitlines()

        for ext in extensions:
            cmd = f"{code} --install-extension {ext}"
            self.exec_bash(cmd)


    def platform_specific_install(self):
        pass