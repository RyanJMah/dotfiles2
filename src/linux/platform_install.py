import os
import subprocess

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def install_nvim():
    nvim_install_script = os.path.join(THIS_DIR, "install_nvim.sh")

    subprocess.run(["bash", nvim_install_script], check=True)


def platform_specific_install():
    pass
