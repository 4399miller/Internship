import os
import platform
import subprocess
import traceback

testMode = True

if not testMode:
    from .logutility import LogUtility
    from .platformutility import in_win, in_mac

else:
    cur_platform = platform.system().lower()
    in_win = cur_platform == "windows"
    in_mac = cur_platform == "darwin"

if in_win:
    import win32file


def is_file_using(file_path):
    if file_path is None:
        return False
    if in_win:
        if not os.access(file_path, os.F_OK):  # 是否存在
            return False
        try:
            vHandle = win32file.CreateFile(file_path, win32file.GENERIC_WRITE,
                                           0, None, win32file.OPEN_EXISTING,
                                           win32file.FILE_ATTRIBUTE_NORMAL, None)
            if int(vHandle) == win32file.INVALID_HANDLE_VALUE:
                win32file.CloseHandle(vHandle)
                return True
            else:
                win32file.CloseHandle(vHandle)
                return False
        except Exception as e:
            log_error(e)
            return True
    elif in_mac:
        try:
            result = subprocess.getoutput("lsof | grep " + file_path)
            log(result)
            lines = result.splitlines()
            for line in lines:
                content = line.split()
                if content[0] != "Finder":
                    return True
            return False
        except:
            log_error(traceback.format_exc())
            return False
    else:
        return False


def is_folder_w(path):
    if os.path.isdir(path):
        if os.access(path, os.W_OK):
            return True
    return False


def can_open_check_using(path):
    try:
        f = open(path, "a+")
        f.close()
        return False
    except Exception as e:
        log_error(e)
        return True


def log(text):
    if not testMode:
        LogUtility().info(text)
    else:
        print(text)


def log_error(text):
    if not testMode:
        LogUtility().error(text)
    else:
        print(text)

if __name__ == "__main__":
    path = r"/Users/m100101389/Perforce/9_X3Engine_PreR_mac/Mac/MacEditor/Unity.app/Contents/MacOS/Unity"
    # f = open(path, "a+")
    print(is_file_using(path))
    # f.close()
    # print(can_open_check_using(path))
