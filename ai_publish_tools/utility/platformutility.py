import os
import sys
import traceback

from .logutility import LogUtility
from constant import isEditor, in_win, in_mac

cur_platform = "Windows" if in_win else "Mac"

if in_win:
    import win32api
    import win32file


def trans_unity_cmd_path(unity_path):
    if in_mac:
        return os.path.join(unity_path, "Contents/MacOS/Unity")
    return unity_path


def get_unity_folder_path(unity_path):
    if in_mac:
        return os.path.dirname(unity_path.replace("/Contents/MacOS/Unity", ""))
    elif in_win:
        return os.path.dirname(unity_path)


def open_local_folder(folder):
    try:
        if in_win:
            os.startfile(folder)
        elif in_mac:
            os.system("open '{}'".format(folder))
    except:
        LogUtility().error(traceback.format_exc())


def ui_file_path(filename):
    if in_win or isEditor:
        return f"view/ui/{filename}.ui"
    elif in_mac:
        return os.path.join(os.path.dirname(sys.argv[0]), f"view/ui/{filename}.ui")


def open_process_with_param(cmd, param, startFolder):
    try:
        if in_win:
            win32api.ShellExecute(0, 'open', cmd, param, startFolder, 1)
        else:
            if param is not None and param != "":
                cmd += f" --args {param}"
            LogUtility().info("open process cmd: " + cmd)
            os.system("open " + cmd)
    except:
        LogUtility().error(traceback.format_exc())

