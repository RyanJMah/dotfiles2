import os
import subprocess
from abc import ABC, abstractmethod

from paths import DOTFILES_COMMON_DIR, HOME

class Platform(ABC):
    ##############################################################################
    @abstractmethod
    def install_nvim(self):
        pass

    @abstractmethod
    def install_tmux(self):
        pass

    @abstractmethod
    def platform_specific_install(self):
        pass

    @abstractmethod
    def get_code_cmd(self) -> str:
        pass

    @abstractmethod
    def get_code_conf_dir(self) -> str:
        pass
    ##############################################################################


    ##############################################################################
    def exec_bash(self, cmd_str):
        cmd = cmd_str.strip()
        try:
            subprocess.run(cmd, shell=True, text=True, check=True)
        
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e}")
    ##############################################################################


    ##############################################################################
    def install_oh_my_zsh_conf(self):
        cmd = f"""
        sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
        source {HOME}/.zshrc
        """
        self.exec_bash(cmd)
    

    def install_minimal_shell_conf(self):
        cmd = f"""
        ln -sf {DOTFILES_COMMON_DIR}/minimal_shell_conf/.zshrc  {HOME}/.zshrc
        ln -sf {DOTFILES_COMMON_DIR}/minimal_shell_conf/.bashrc {HOME}/.bashrc
        ln -sf {DOTFILES_COMMON_DIR}/minimal_shell_conf/.tcshrc {HOME}/.tcshrc

        ln -sf {DOTFILES_COMMON_DIR}/minimal_shell_conf/.git-prompt.sh {HOME}/.git-prompt.sh
        """
        self.exec_bash(cmd)


    def install_aliases(self):
        cmd = f"""
        ln -sf {DOTFILES_COMMON_DIR}/.custom_aliases.sh {HOME}/.custom_aliases.sh
        """

        self.exec_bash(cmd)


    def install_nvim_conf(self):
        cmd = f"""
        mkdir -p {HOME}/.config/nvim
        
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/.vimrc   {HOME}/.vimrc
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/init.vim {HOME}/.config/nvim/init.vim

        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/.terminal-vimrc.vim {HOME}/.terminal-vimrc.vim
        ln -sf {DOTFILES_COMMON_DIR}/nvim_conf/.vscode-vimrc.vim   {HOME}/.vscode-vimrc.vim
        """

        self.exec_bash(cmd)

    def install_vscode_conf(self):
        vscode_dir = self.get_code_conf_dir()

        cmd = f"""
        mkdir -p {vscode_dir}

        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/settings.json    {vscode_dir}/settings.json
        ln -sf {DOTFILES_COMMON_DIR}/vscode_conf/keybindings.json {vscode_dir}/keybindings.json
        """

        self.exec_bash(cmd)

    def install_vscode_extensions(self):
        extensions_txt = os.path.join(DOTFILES_COMMON_DIR, "vscode_extensions.txt")

        # code = r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code"
        code = self.get_code_cmd()

        with open(extensions_txt, "r") as f:
            extensions = f.read().splitlines()

        for ext in extensions:
            cmd = f"{code} --install-extension {ext}"
            self.exec_bash(cmd)

        # Install my own custom theme
        cmd = f"""
        curl -LO https://github.com/RyanJMah/Ryan-VSCode-Theme/releases/download/2.0.0/ryan-vscode-theme-2.0.0.vsix

        {code} --install-extension ryan-vscode-theme-2.0.0.vsix
        rm ryan-vscode-theme-2.0.0.vsix
        """
        self.exec_bash(cmd)
    ##############################################################################
