# My Dotfiles

Second iteration of my dotfiles, designed to be more minimal, lightweight, and have
as little dependencies as possible.

For the original iteration of my dotfiles, see [here](https://github.com/RyanJMah/dotfiles).

Some interesting features/choices include:

* Doesn't require `sudo apt install` or `brew install` or equivalents (given that the
  **minimal** dependencies are already installed)

* `nvim` config doesn't use a plugin manage (e.g., plug), all plugins are managed as submodules within this repository.
    * The installation scripts symlink the submodules to the appropriate directories
    * A big advantage of this approach is that all plugin commits are pinned, meaning no more bricking your
      setup by doing `:PlugUpdate`, or anything like that

* `tmux` config doesn't require `tpm`

# Cloning and Troubleshooting

* **YOU MUST CLONE WITH `--recursive` for the repo to work**

```
git clone --recursive https://github.com/RyanJMah/dotfiles2
```

* You will probably have to do `:TSUninstall all` the first time you
  launch `nvim`, if you're doing the remote setup


## Dependencies

* `python3`
* `pip3`
* `curl`
* `tar`
* `make`
* A C compiler

`tmux` doesn't have stand-alone pre-built binaries like `nvim` does, so the install scripts
have to build it from source.

As such, if you want the tmux installation you will need some more dependencies - notably,
the following:

* `bison`


The installation scripts have some dependencies as well, install them via pip.

```bash
pip3 install -r requirements.txt
```

### MacOS

All dependencies should be able to be installed by `xcode-select --install`.

## Installation

Locally, you can just do this.

```shell
./quick-install.sh
```

### Remote Servers

The Linux configuration supports installing on remote servers, even if they
do not have internet access due to firewalls or what not (which is quite common
for large companies).

This works by doing all necessary installs from internet locally, then sftp-ing
the files up. This method of installation can be invoked like so:

```bash
# see --help for more options
python3 install.py --os linux --remote localhost --user testuser --password pass --port 2222
```

## Test Environments

To test the installation scripts, test environments are provided. They
provide a "fresh" install of the target OS to run the scripts on.

### Linux

A docker container running Debian 11 is provided.

```bash
cd test_environments/linux

./spinup_container.sh
```

### MacOS

A computer legally running MacOS is required. Apple's own virutalization
framework in swift is used to spin-up a VM running a fresh install of MacOS.

**NOTE:**
* To clone this repo in the VM, you will need to `xcode-select --install` first

```bash
cd test_environments/macos

make
make run

# Delete the current VM (to start fresh)
make clean
```
