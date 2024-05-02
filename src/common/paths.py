import os

HOME = os.path.expanduser("~")

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)

DOTFILES_DIR        = os.path.join(ROOT_DIR, "dotfiles")
DOTFILES_COMMON_DIR = os.path.join(DOTFILES_DIR, "common")
DOTFILES_LINUX_DIR  = os.path.join(DOTFILES_DIR, "linux")
DOTFILES_MACOS_DIR  = os.path.join(DOTFILES_DIR, "macos")