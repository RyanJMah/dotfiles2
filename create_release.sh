#!/usr/bin/env bash

THIS_DIR=$(dirname "$0")

# source .venv if it exists
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

pip3 install git-archive-all


mkdir -p $THIS_DIR/releases

# create tarball of git repo
git-archive-all -v --force-submodules $THIS_DIR/releases/dotfiles2.tar.gz

# create artifacts tarball
python3 $THIS_DIR/src/common/artifact_urls.py --os-type linux --out-dir $THIS_DIR/releases
python3 $THIS_DIR/src/common/artifact_urls.py --os-type macos --out-dir $THIS_DIR/releases
