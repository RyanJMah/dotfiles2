import os
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, Optional
from tempfile import TemporaryDirectory

from app_paths import Paths, RESOURCES_DIR
from shell_wrapper import Shell

class Platform(ABC):
    def __init__(self, shell: Shell, paths: Paths):
        self.shell = shell
        self.paths = paths

        os.makedirs(self.paths.BUILD_DIR, exist_ok=True)

    def exec_bash(self, cmd_str):
        self.shell.run(cmd_str)

    def install_url(self, *args, **kwargs):
        self.shell.install(*args, **kwargs)

    ##############################################################################
    @abstractmethod
    def get_nvim_download_url(self) -> str:
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

    # Can override
    def platform_tmux_configure_flags(self) -> Dict[str, str]:
        return {}
    ##############################################################################


    ##############################################################################
    def install_oh_my_zsh_conf(self):
        ok = self.shell.check_dependency("zsh")
        if not ok:
            print("ERROR: zsh is not installed, skipping...")
            return


        if not os.path.exists(f"{self.paths.HOME}/.oh-my-zsh"):
            self.install_url("https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh", self.paths.BUILD_DIR)

            cmd = f"""
            cd {self.paths.BUILD_DIR}
            
            sh install.sh --unattended
            rm install.sh

            mkdir -p {self.paths.HOME}/.oh-my-zsh/custom/plugins
            """
            self.exec_bash(cmd)

            # Install plugins
            self.shell.symlink_dir_files(f"{self.paths.DOTFILES_COMMON_DIR}/oh_my_zsh_conf/plugins", f"{self.paths.HOME}/.oh-my-zsh/custom/plugins")

        cmd = f"""
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/oh_my_zsh_conf/.zshrc {self.paths.HOME}/.zshrc

        cp {self.paths.DOTFILES_COMMON_DIR}/oh_my_zsh_conf/*.zsh-theme {self.paths.HOME}/.oh-my-zsh/themes
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


    def install_nvim(self):
        self.install_url( self.get_nvim_download_url(), self.paths.BUILD_DIR )

        cmd = f"""
        cd {self.paths.BUILD_DIR}

        tar -xzf nvim-*.tar.gz

        rm nvim-*.tar.gz

        mkdir -p {self.paths.HOME}/.local/nvim

        if [ -d {self.paths.HOME}/.local/nvim ];
        then
            rm -r {self.paths.HOME}/.local/nvim
        fi

        mv nvim-* {self.paths.HOME}/.local/nvim
        """
        self.exec_bash(cmd)


    def install_nvim_conf(self):
        # The plugins are installed in this repo as submodules, symlink them
        plugins_dir           = f"{self.paths.HOME}/.local/share/nvim/site/pack/vendor/start"
        submodule_plugins_dir = f"{self.paths.DOTFILES_COMMON_DIR}/nvim_conf/plugins"

        cmd = f"""
        set -e

        mkdir -p {self.paths.HOME}/.config/nvim

        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/.vimrc   {self.paths.HOME}/.vimrc
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/init.vim {self.paths.HOME}/.config/nvim/init.vim

        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/.terminal-vimrc.vim {self.paths.HOME}/.terminal-vimrc.vim
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/nvim_conf/.vscode-vimrc.vim   {self.paths.HOME}/.vscode-vimrc.vim

        mkdir -p {plugins_dir}
        """
        self.exec_bash(cmd)

        # Install plugins
        self.shell.symlink_dir_files(submodule_plugins_dir, plugins_dir)


        # Install plugin dependencies
        self.install_url( self.get_ripgrep_download_url(), self.paths.BUILD_DIR )

        xxd_dir = os.path.join(self.paths.BUILD_DIR, "xxd")
        self.install_url( "https://raw.githubusercontent.com/vim/vim/master/src/xxd/xxd.c",    xxd_dir )
        self.install_url( "https://raw.githubusercontent.com/vim/vim/master/src/xxd/Makefile", xxd_dir )

        cmd = f"""
        set -e

        cd {self.paths.BUILD_DIR}

        # ripgrep
        tar -zxf ripgrep-*.tar.gz
        rm ripgrep-*.tar.gz

        if [ -d {self.paths.HOME}/.local/ripgrep ];
        then
            rm -r {self.paths.HOME}/.local/ripgrep
        fi

        mv ripgrep-*/ {self.paths.HOME}/.local/ripgrep

        mkdir -p {self.paths.HOME}/.local/bin
        ln -sf {self.paths.HOME}/.local/ripgrep/rg {self.paths.HOME}/.local/bin/rg


        # xxd (build from source)
        cd {xxd_dir}
        make
        mv xxd {self.paths.HOME}/.local/bin
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
        extensions_txt = os.path.join(RESOURCES_DIR, "vscode_extensions.txt")

        code = self.get_code_cmd()

        with open(extensions_txt, "r") as f:
            extensions = f.read().splitlines()

        for ext in extensions:
            cmd = f"{code} --install-extension {ext}"
            self.exec_bash(cmd)

        # Install my own custom theme
        self.install_url(
            "https://github.com/RyanJMah/Ryan-VSCode-Theme/releases/download/2.0.0/ryan-vscode-theme-2.0.0.vsix",
            self.paths.BUILD_DIR
        )

        cmd = f"""
        {code} --install-extension ryan-vscode-theme-2.0.0.vsix
        rm ryan-vscode-theme-2.0.0.vsix
        """
        self.exec_bash(cmd)



    def install_tmux(self):
        install_dir = os.path.join(self.paths.HOME, ".local")

        configure_flags = self.platform_tmux_configure_flags()

        libevent_flags = configure_flags.get("libevent", "")
        ncurses_flags  = configure_flags.get("ncurses", "")
        tmux_flags     = configure_flags.get("tmux", "")

        self.install_url(
            "https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz",
            self.paths.BUILD_DIR
        )
        self.install_url(
            "https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz",
            self.paths.BUILD_DIR
        )
        self.install_url(
            "https://ftp.gnu.org/gnu/ncurses/ncurses-6.3.tar.gz",
            self.paths.BUILD_DIR
        )
        self.install_url(
            "https://github.com/tmux/tmux/releases/download/3.4/tmux-3.4.tar.gz",
            self.paths.BUILD_DIR
        )

        cmd = f"""
        set -e

        cd {self.paths.BUILD_DIR}

        INSTALL_DIR={install_dir}
        mkdir -p $INSTALL_DIR

        # Install pkg-config
        tar -zxf pkg-config-*.tar.gz

        cd pkg-config-*/
        CFLAGS=-Wno-int-conversion ./configure --prefix=$INSTALL_DIR --with-internal-glib
        make -j && make install

        cd ..

        PKG_CONFIG_BIN=$INSTALL_DIR/bin/pkg-config

        # install libevent
        tar -zxf libevent-*.tar.gz

        cd libevent-*/

        ./configure --prefix=$INSTALL_DIR --disable-openssl {libevent_flags}
        make -j && make install

        cd ..

        # install ncurses
        tar -zxf ncurses-*.tar.gz

        cd ncurses-*/
        ./configure --prefix=$INSTALL_DIR --with-termlib --enable-pc-files --with-pkg-config=$PKG_CONFIG_BIN --with-pkg-config-libdir=$INSTALL_DIR/lib/pkgconfig {ncurses_flags}
        make -j && make install

        cd ..

        # install tmux
        tar -zxf tmux-*.tar.gz

        cd tmux-*/
        PKG_CONFIG_PATH=$INSTALL_DIR/lib/pkgconfig PKG_CONFIG=$PKG_CONFIG_BIN ./configure --prefix=$INSTALL_DIR {tmux_flags}
        make -j && make install

        cd ..

        rm -r libevent-* ncurses-* tmux-* pkg-config-*
        """
        self.exec_bash(cmd)


    def install_tmux_conf(self):
        cmd = f"""
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/tmux_conf/.tmux.conf {self.paths.HOME}/.tmux.conf
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/tmux_conf/.tmux_theme.sh {self.paths.HOME}/.tmux_theme.sh
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/tmux_conf/.tmux_sensible.sh {self.paths.HOME}/.tmux_sensible.sh
        """
        self.exec_bash(cmd)

    def install_misc(self):
        cmd = f"""
        ln -sf {self.paths.DOTFILES_COMMON_DIR}/scripts/fuck-windows {self.paths.HOME}/.local/bin
        """
        self.exec_bash(cmd)
    ##############################################################################
