import os
import sys
import platform

in_win = platform.system().lower() == "windows"
in_mac = platform.system().lower() == "darwin"

isEditor = os.path.exists(f".spec")