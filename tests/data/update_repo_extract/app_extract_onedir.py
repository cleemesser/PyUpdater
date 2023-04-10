# ------------------------------------------------------------------------------
# Copyright (c) 2015-2020 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------
from __future__ import print_function
import os
import sys

from pyupdater.client import Client
from dsdev_utils.paths import get_mac_dot_app_dir

import client_config

APPNAME = "Acme"
VERSION = "4.1"


def cb(status):
    out = ""
    percent = status.get("percent_complete")
    time = status.get("time")
    if percent is not None:
        out += f"{percent}%"
    if time is not None:
        out += f" - {time}"
    if not out:
        out = "Nothing yet..."
    sys.stdout.write(f"\r{out}")
    sys.stdout.flush()


def main():
    print(VERSION)
    data_dir = None
    config = client_config.ClientConfig()
    if getattr(config, "USE_CUSTOM_DIR", False):
        if sys.platform == "darwin" and os.path.dirname(sys.executable).endswith(
            "MacOS"
        ):
            data_dir = os.path.join(
                get_mac_dot_app_dir(os.path.dirname(sys.executable)), ".update"
            )
        else:
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(sys.executable)), ".update"
            )
    client = Client(config, refresh=True, progress_hooks=[cb], data_dir=data_dir)
    update = client.update_check(APPNAME, VERSION)
    if update is not None:
        success = update.download()
        print("")
        if success is True:
            print("Update download successful")
            print("Extracting & overwriting")
            update.extract_overwrite()
        else:
            print("Failed to download update")
    return VERSION


if __name__ == "__main__":
    main()
