import os
import re
import traceback
import psutil
import platform

cur_platform = platform.system().lower()

in_win = cur_platform == "windows"
in_mac = cur_platform == "darwin"

if in_win:
    import win32api
    import win32com.client
    import win32gui
    import win32con

def trans_path(path):
    return path.replace("\\", "/")

def clear_dll_directory():
    if in_win:
        win32api.SetDllDirectory(None)

def getPidsByProcessName(name):
    pids = []
    processes = psutil.process_iter()
    try:
        for process in processes:
            try:
                if process.name() == name:
                    print(process.name())
                    print(process.pid)
                    pids.append(process.pid)
            except psutil.NoSuchProcess:
                pass
            except:
                pass
    except:
        pass
    return pids


def getPidByProcessName(name):
    processes = psutil.process_iter()
    for process in processes:
        if process.name() == name:
            print(process.name())
            print(process.pid)
            return process
    return 0


def checkProcessMulti(process_name):
    return __checkProcessExist(process_name, 1)


def checkProcessExist(process_name):
    return __checkProcessExist(process_name, 0)


def __checkProcessExist(process_name, count):
    if in_win and process_name[-4:] != ".exe":
        process_name += ".exe"
    processCount = getPidsByProcessName(process_name)

    if len(processCount) > count:
        return True
    else:
        return False


def hasOpenedMessage():
    if in_win:
        result = win32api.MessageBox(0, "应用已打开", "提示", win32con.MB_OK)
        print("result " + str(result))
    elif in_mac:
        pass


def _hasOpenedMessage():
    if in_win:
        # result = win32api.MessageBox(0, "应用已打开", "提示", win32con.MB_OK)
        # print("result " + str(result))
        try:
            def callback(hwnd, wildcard):
                if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
                    win32gui.BringWindowToTop(hwnd)

                    shell = win32com.client.Dispatch("WScript.Shell")
                    shell.SendKeys('%')

                    # win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)

                    # win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 800, 600, 1000, 600, win32con.SWP_SHOWWINDOW)

            hwnd = win32gui.FindWindow(None, "TempLauncher")
            # win32gui.EnumWindows(callback, "TempLauncher")
            # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.BringWindowToTop(hwnd)
            # win32gui.SetWindowPos(window, win32con.HWND_TOPMOST, 0, 0, 800, 600, win32con.SWP_SHOWWINDOW)
        except:
            print(traceback.format_exc())
    elif in_mac:
        pass


def killCurProcess():
    pid = os.getpid()
    killProcessByPid(pid)


def killProcessByPid(pid):
    try:
        if in_win:
            handle = win32api.OpenProcess(1, False, pid)
            win32api.TerminateProcess(handle, -1)
        elif in_mac:
            os.system("kill -9 {}".format(pid))
    except:
        print(traceback.format_exc())


def killProcessByName(exe):
    try:
        if in_win:
            os.system("taskkill /F /IM " + exe)
        elif in_mac:
            os.system("pkill -9 {}".format(exe))
    except:
        print(traceback.format_exc())


def killProcessByPath(exe_path):
    exe_path = trans_path(exe_path)
    processes = psutil.process_iter()
    for process in processes:
        try:
            path = trans_path(process.exe())
            if path == exe_path:
                print(process.name())
                print(process.pid)
                process.kill()
        except:
            pass

if __name__ == "__main__":
    path = r"/Users/m100101389/Perforce/9_X3Engine_PreR_mac/Mac/MacEditor/Unity.app/Contents/MacOS/Unity"
    # killProcess("Unity.exe")
    # killProcessByPath(path)
    # killProcessByName("TempLauncher")
    # print(checkProcessExist("Unity.exe"))
    # getPidByProcessName("TempLauncher")
    # __checkProcessExist("TempLauncher", 0)
    _hasOpenedMessage()