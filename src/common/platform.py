import os
import subprocess
from abc import ABC, abstractmethod

from app_paths import Paths
from shell_wrapper import Shell

class Platform(ABC):
    def __init__(self, shell: Shell, paths: Paths):
        self.shell = shell
        self.paths = paths

    def exec_bash(self, cmd_str):
        self.shell.run(cmd_str)


    ##############################################################################
    @abstractmethod
    def install_nvim(self):
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

    @abstractmethod
    def get_ripgrep_download_url(self) -> str:
        pass
    ##############################################################################


    ##############################################################################
    def install_oh_my_zsh_conf(self):
        cmd = f"""
        sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
        source {self.paths.HOME}/.zshrc
        """
        self.exec_bash(cmd)
    

    def install_minimal_shell_conf(self):
        cmd = f"""
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/minimal_shell_conf/.zshrc  {self.paths.HOME}/.zshrc
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/minimal_shell_conf/.bashrc {self.paths.HOME}/.bashrc
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/minimal_shell_conf/.tcshrc {self.paths.HOME}/.tcshrc

        ln -sf {self.paths.DOTFILES_COMMON_DIR}/minimal_shell_conf/.git-prompt.sh {self.paths.HOME}/.git-prompt.sh
        """
        self.exec_bash(cmd)


    def install_aliases(self):
        cmd = f"""
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/.custom_aliases.sh {self.paths.HOME}/.custom_aliases.sh
        """

        self.exec_bash(cmd)


    def install_nvim_conf(self):
        plugin_dir = f"{self.paths.HOME}/.local/share/nvim/site/pack/vendor/start"

        cmd = f"""
        set -e

        mkdir -p {self.paths.HOME}/.config/nvim
        
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/.vimrc   {self.paths.HOME}/.vimrc
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/init.vim {self.paths.HOME}/.config/nvim/init.vim

        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/.terminal-vimrc.vim {self.paths.HOME}/.terminal-vimrc.vim
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/.vscode-vimrc.vim   {self.paths.HOME}/.vscode-vimrc.vim

        mkdir -p {plugin_dir}
        """
        self.exec_bash(cmd)

        # install plugins
        with open(os.path.join(self.paths.DOTFILES_COMMON_DIR, "nvim_conf", "plugins.txt"), "r") as f:
            plugins = f.read().strip().splitlines()

        for plugin in plugins:
            plugin_name = plugin.split("/")[-1]

            cmd = f"""
            git clone https://github.com/{plugin}.git tmp
            mv tmp {plugin_dir}/{plugin_name}
            """
            self.exec_bash(cmd)

        # Install plugin dependencies
        cmd = f"""
        set -e

        # ripgrep
        curl -LO {self.get_ripgrep_download_url()}
        tar -zxf ripgrep-*.tar.gz
        rm ripgrep-*.tar.gz

        mkdir -p {self.paths.HOME}/.local/bin/ripgrep
        mv ripgrep-* {self.paths.HOME}/.local/bin/ripgrep
        ln -sf {self.paths.HOME}/.local/bin/ripgrep/rg {self.paths.HOME}/.local/bin/rg

        # xxd (build from source)
        mkdir tmp
        cd tmp
        curl -LO https://raw.githubusercontent.com/vim/vim/master/src/xxd/Makefile
        curl -LO https://raw.githubusercontent.com/vim/vim/master/src/xxd/xxd.c
        make
        mv xxd {self.paths.HOME}/.local/bin

        cd ..
        rm -rf tmp
        """
        self.exec_bash(cmd)



    def install_vscode_conf(self):
        vscode_dir = self.get_code_conf_dir()

        cmd = f"""
        mkdir -p {vscode_dir}

        ln -sf {self.paths.DOTFILES_COMMON_DIR}/vscode_conf/settings.json    {vscode_dir}/settings.json
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/vscode_conf/keybindings.json {vscode_dir}/keybindings.json
        """

        self.exec_bash(cmd)

    def install_vscode_extensions(self):
        extensions_txt = os.path.join(self.paths.DOTFILES_COMMON_DIR, "vscode_extensions.txt")

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

    def install_tmux(self):
        install_dir = os.path.join(self.paths.HOME, ".local", "tmux")

        cmd = f"""
        set -e

        mkdir -p {install_dir}

        # install libevent

        curl -LO https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz

        tar -zxf libevent-*.tar.gz
        rm libevent-2.1.12-stable.tar.gz

        cd libevent-*/

        ./configure --prefix={install_dir} --enable-shared
        make -j && make install

        cd ..

        # install ncurses
        curl -LO https://ftp.gnu.org/gnu/ncurses/ncurses-6.3.tar.gz

        tar -zxf ncurses-*.tar.gz
        rm ncurses-6.3.tar.gz

        cd ncurses-*/
        ./configure --prefix={install_dir} --with-shared --with-termlib --enable-pc-files --with-pkg-config-libdir={install_dir}/lib/pkgconfig
        make -j && make install

        cd ..

        # install tmux
        curl -LO https://github.com/tmux/tmux/releases/download/3.4/tmux-3.4.tar.gz

        tar -zxf tmux-*.tar.gz
        rm tmux-3.4.tar.gz

        cd tmux-*/
        PKG_CONFIG_PATH={install_dir}/lib/pkgconfig ./configure --prefix={install_dir} --enable-utf8proc
        make -j && make install

        rm -rf libevent-* ncurses-* tmux-*
        """
        self.exec_bash(cmd)

        # Alias to set LD_LIBRARY_PATH before running tmux
        alias_script = f"""
        #!/usr/bin/env bash

        LD_LIBRARY_PATH={install_dir}/lib:${{LD_LIBRARY_PATH}} ${{HOME}}/.local/tmux/bin/tmux "$@"

        """

        cmd = f"""
        set -e

        mkdir -p {self.paths.HOME}/.local/bin
        cd {self.paths.HOME}/.local/bin

        touch tmux
        chmod +x tmux

        echo '{alias_script}' > tmux

        # Test the alias
        {self.paths.HOME}/.local/bin/tmux -V
        """
        self.exec_bash(cmd)



    ##############################################################################
