import click
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

LINUX_LOCAL_ARTIFACTS = TargetArtifacts( oh_my_zsh_install_sh = "install.sh",
                                         
                                         nvim_tarball = "nvim-linux64.tar.gz",

                                         ripgrep_tarball = "ripgrep-14.1.0-x86_64-unknown-linux-musl.tar.gz",
                                         xxd_c = "xxd.c",
                                         xxd_makefile = "Makefile",

                                         ryan_vscode_theme_vsix = "ryan-vscode-theme-2.0.0.vsix",

                                         pkg_config_tarball = "pkg-config-0.29.2.tar.gz",
                                         libevent_tarball = "libevent-2.1.12-stable.tar.gz",
                                         ncurses_tarball = "ncurses-6.3.tar.gz",
                                         tmux_tarball = "tmux-3.4.tar.gz",

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

MACOS_LOCAL_ARTIFACTS = TargetArtifacts( oh_my_zsh_install_sh = "install.sh",
                                        
                                         nvim_tarball = "nvim-macos.tar.gz",

                                         ripgrep_tarball = "ripgrep-14.1.0-aarch64-apple-darwin.tar.gz",
                                         xxd_c = "xxd.c",
                                         xxd_makefile = "Makefile",

                                         ryan_vscode_theme_vsix = "ryan-vscode-theme-2.0.0.vsix",

                                         pkg_config_tarball = "pkg-config-0.29.2.tar.gz",
                                         libevent_tarball = "libevent-2.1.12-stable.tar.gz",
                                         ncurses_tarball = "ncurses-6.3.tar.gz",
                                         tmux_tarball = "tmux-3.4.tar.gz",

                                         platform_artifacts = {
                                             "utf8proc": "utf8proc-2.9.0.tar.gz"
                                         } )

@click.command()
@click.option("--os-type", type=click.Choice(["linux", "macos"]), required=True)
def __generate_artifacts_tarball(os_type):
    import os
    from dataclasses import fields

    from app_paths import LocalPaths
    from artifacts import RemoteArtifact
    from shell_wrapper import LocalShell

    paths = LocalPaths()
    shell = LocalShell()
    
    if os_type == "linux":
        target_artifacts = TargetArtifacts.from_target_urls(LINUX_DOWNLOADABLE_ARTIFACTS, RemoteArtifact)
    else:
        target_artifacts = TargetArtifacts.from_target_urls(MACOS_DOWNLOADABLE_ARTIFACTS, RemoteArtifact)

    # Create the artifacts bundle directory
    bundle_dir = os.path.join(paths.BUILD_DIR, f"artifacts_bundle-{os_type}")
    os.makedirs(bundle_dir, exist_ok=True)

    def download_artifact(artifact: RemoteArtifact):
        print(f"Downloading {artifact.url} -> {bundle_dir}/{artifact.filename}")
        shell.install(artifact.url, bundle_dir)


    for field in fields(target_artifacts):
        fieldname = field.name
        field_obj = getattr(target_artifacts, fieldname)

        if isinstance(field_obj, dict):
            for _, artifact in field_obj.items():
                download_artifact(artifact)

        else:
            download_artifact(field_obj)

    # Create the tarball
    tarball_filename = os.path.join(paths.BUILD_DIR, f"artifacts_bundle-{os_type}.tar.gz")
    shell.run(f"tar -cvzf {tarball_filename} -C {bundle_dir} .")

    print(f"Artifacts tarball created: {tarball_filename}")


if __name__ == "__main__":
    __generate_artifacts_tarball()
