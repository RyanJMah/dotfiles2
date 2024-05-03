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

    def get_code_conf_dir(self) -> str:
        return f"{HOME}/Library/Application\\ Support/Code/User"

    def get_code_cmd(self) -> str:
        return r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code"

    def install_tmux(self):
        install_dir = os.path.join(HOME, ".local")

        cmd = f"""
        set -e

        mkdir -p {install_dir}

        # install libevent

        curl -LO https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz

        tar -zxf libevent-*.tar.gz
        rm libevent-2.1.12-stable.tar.gz

        cd libevent-*/

        ./configure --prefix={install_dir} --enable-shared
        make && make install

        cd ..

        # install ncurses
        curl -LO https://ftp.gnu.org/gnu/ncurses/ncurses-6.3.tar.gz

        tar -zxf ncurses-*.tar.gz
        rm ncurses-6.3.tar.gz

        cd ncurses-*/
        ./configure --prefix={install_dir} --with-shared --with-termlib --enable-pc-files --with-pkg-config-libdir={install_dir}/lib/pkgconfig
        make && make install

        cd ..

        # install tmux
        curl -LO https://github.com/tmux/tmux/releases/download/3.4/tmux-3.4.tar.gz

        tar -zxf tmux-*.tar.gz
        rm tmux-3.4.tar.gz

        cd tmux-*/
        PKG_CONFIG_PATH={install_dir}/lib/pkgconfig ./configure --prefix={install_dir} --enable-utf8proc
        make && make install
        """
        self.exec_bash(cmd)



    def platform_specific_install(self):
        pass

    def install_aliases(self):
        super().install_aliases()

        cmd = f"""
        ln -sf {DOTFILES_MACOS_DIR}/.platform_custom_aliases.sh {HOME}/.platform_custom_aliases.sh
        """
        self.exec_bash(cmd)
