#!/usr/bin/env bash

set -e

# Neovim doesn't do builds for arm64, but we probably don't need it
# anyways. However, I stil need to be able to test on my M2 Mac,
# so just sudo apt install neovim for now.

curl -LO https://github.com/neovim/neovim/releases/download/v0.9.5/nvim-linux64.tar.gz
tar -xzf nvim-linux64.tar.gz

rm nvim-linux64.tar.gz