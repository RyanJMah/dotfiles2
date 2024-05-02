# My Dotfiles

Second iteration of my dotfiles, designed to be more minimal, lightweight, and have
as little dependencies as possible. For example, no longer requires sudo apt install
or brew install.

For the original iteration of my dotfiles, see [here](https://github.com/RyanJMah/dotfiles).

## Dependencies

* `python3`
* `pip3`
* `curl`

The installation scripts have some dependencies as well, install them via pip.

```bash
pip3 install -r requirements.txt
```

## Installation

```shell
./quick-install.sh
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

./spinup_vm.sh
```

Once a VM is provisioned, it's disk will be persistent even when it's shut off.
To create a fresh VM instance, simply remove the VM bundle.

```bash
rm -rf VM.bundle
```
