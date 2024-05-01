import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.dirname(THIS_DIR)
sys.path.append(SRC_DIR)

from common.platform import Platform

class MacOS(Platform):
    def install_nvim():
        pass

    def platform_specific_install(self):
        pass