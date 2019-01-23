# -*- coding: utf-8 -*-
"""version file."""
__version__ = '1.3.2'

import os
import sys
import time
import subprocess as sp
import webbrowser
import shutil


def check_requirements():
    """Errors and quits if tshark is not installed.

    On Windows, tshark may not be recognized by cmd even if Wireshark is
    installed. On Windows, this function will add the Wireshark folder to path
    so `tshark` can be called.

    Changing os.environ will only affect the cmd shell this program is using
    (tested). Not using setx here as that could be potentially destructive.

    Raises FileNotFonudError:
        If wireshark/tshark is not found, raise an error as they are required.
    """
    if sys.platform == 'win32':
        os.environ["PATH"] += os.pathsep + os.pathsep.join(
            ["C:\\Program Files\\Wireshark"])
    is_tshark_on_path = shutil.which('tshark')
    if not is_tshark_on_path:
        print("\nERROR: Requirement tshark from Wireshark not found!",
              "\n       Please install Wireshark or add tshark to your PATH.",
              "\n\nOpening Wireshark download page...")
        time.sleep(2)
        webbrowser.open('https://www.wireshark.org/download.html')
        raise FileNotFoundError


def get_wireshark_version():
    """Get the wireshark version in the form of '1.2.3'"""
    command_list = 'wireshark -v'.split()
    sp_pipe = sp.Popen(command_list, stdout=sp.PIPE, stderr=sp.PIPE)
    wireshark_v = sp_pipe.communicate()[0].decode('utf-8')
    return wireshark_v.split(' ')[1]  # Version is 2nd word
