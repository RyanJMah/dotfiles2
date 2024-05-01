import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)

DOTFILES_DIR        = os.path.join(SRC_DIR, "dotfiles")
DOTFILES_COMMON_DIR = os.path.join(DOTFILES_DIR, "common")
DOTFILES_LINUX_DIR  = os.path.join(DOTFILES_DIR, "linux")
DOTFILES_MACOS_DIR  = os.path.join(DOTFILES_DIR, "macos")