import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform
from common.paths import HOME, DOTFILES_COMMON_DIR, DOTFILES_MACOS_DIR

class MacOS(Platform):
    def install_nvim(self):
        cmd = """
        curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-macos.tar.gz

        xattr -c ./nvim-macos.tar.gz
        tar -xzf nvim-macos.tar.gz
        """

        self.exec_bash(cmd)

    def install_vscode_conf(self):
        vscode_dir = f"{HOME}/Library/Application Support/Code/User"

        cmd = f"""
        mkdir -p {vscode_dir}

        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/settings.json    {vscode_dir}/settings.json
        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/keybindings.json {vscode_dir}/keybindings.json
        """

        self.exec_bash(cmd)

    def install_vscode_extensions(self):
        super().install_vscode_extensions()
    
        macos_extensions_dir = os.path.join(DOTFILES_MACOS_DIR, "vscode_extensions")

        for f in os.listdir(macos_extensions_dir):
            if f.endswith(".vsix"):
                cmd = f"code --install-extension {os.path.join(macos_extensions_dir, f)}"

                self.exec_bash(cmd)


    def platform_specific_install(self):
        pass