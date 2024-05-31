from artifacts import TargetArtifacts

__OH_MY_ZSH_INSTALL_SH = "https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh"

__NVIM_TARBALL_LINUX = "https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-linux64.tar.gz"
__NVIM_TARBALL_MACOS = "https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-macos.tar.gz"

__RIPGREP_TARBALL_LINUX = "https://github.com/BurntSushi/ripgrep/releases/download/14.1.0/ripgrep-14.1.0-x86_64-unknown-linux-musl.tar.gz"
__RIPGREP_TARBALL_MACOS = "https://github.com/BurntSushi/ripgrep/releases/download/14.1.0/ripgrep-14.1.0-aarch64-apple-darwin.tar.gz"

__XXD_C        = "https://raw.githubusercontent.com/vim/vim/master/src/xxd/xxd.c"
__XXD_MAKEFILE = "https://raw.githubusercontent.com/vim/vim/master/src/xxd/Makefile"

__RYAN_VSCODE_THEME_VSIX = "https://github.com/RyanJMah/Ryan-VSCode-Theme/releases/download/2.0.0/ryan-vscode-theme-2.0.0.vsix"

__PKG_CONFIG_TARBALL = "https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz"
__LIBEVENT_TARBALL   = "https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz"
__NCURSES_TARBALL    = "https://ftp.gnu.org/gnu/ncurses/ncurses-6.3.tar.gz"
__TMUX_TARBALL       = "https://github.com/tmux/tmux/releases/download/3.4/tmux-3.4.tar.gz"

# Needed for MacOS only
__UTF8PROC_TARBALL = "https://github.com/JuliaStrings/utf8proc/releases/download/v2.9.0/utf8proc-2.9.0.tar.gz"


LINUX_DOWNLOADABLE_ARTIFACTS = TargetArtifacts( oh_my_zsh_install_sh = __OH_MY_ZSH_INSTALL_SH,

                                                nvim_tarball = __NVIM_TARBALL_LINUX,
                                                ripgrep_tarball = __RIPGREP_TARBALL_LINUX,

                                                xxd_c = __XXD_C,
                                                xxd_makefile = __XXD_MAKEFILE,

                                                ryan_vscode_theme_vsix = __RYAN_VSCODE_THEME_VSIX,

                                                pkg_config_tarball = __PKG_CONFIG_TARBALL,
                                                libevent_tarball = __LIBEVENT_TARBALL,
                                                ncurses_tarball = __NCURSES_TARBALL,
                                                tmux_tarball = __TMUX_TARBALL,

                                                platform_artifacts = {} )

MACOS_DOWNLOADABLE_ARTIFACTS = TargetArtifacts( oh_my_zsh_install_sh = __OH_MY_ZSH_INSTALL_SH,

                                                nvim_tarball = __NVIM_TARBALL_MACOS,
                                                ripgrep_tarball = __RIPGREP_TARBALL_MACOS,

                                                xxd_c = __XXD_C,
                                                xxd_makefile = __XXD_MAKEFILE,

                                                ryan_vscode_theme_vsix = __RYAN_VSCODE_THEME_VSIX,

                                                pkg_config_tarball = __PKG_CONFIG_TARBALL,
                                                libevent_tarball = __LIBEVENT_TARBALL,
                                                ncurses_tarball = __NCURSES_TARBALL,
                                                tmux_tarball = __TMUX_TARBALL,

                                                platform_artifacts = {
                                                    "utf8proc": __UTF8PROC_TARBALL
                                                } )


