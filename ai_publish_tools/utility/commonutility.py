import os
import shutil
import mmap
from multiprocessing import shared_memory


from .platformutility import in_win, in_mac


class SharedMemory:
    _instances = {}

    class ExistsError(Exception):
        pass

    def __init__(self, tagname, size):
        self.__size = size
        self.__real_size = size + 1
        self.__tagname = tagname
        self.__smem = None

    def is_blank(self):
        self.__smem.seek(0)
        return len(self.__smem.read(self.__size).strip('\x00')) == 0

    def size(self):
        return self.__size

    def real_size(self):
        return self.__real_size

    def tagname(self):
        return self.__tagname

    def create(self):
        if self.__tagname in SharedMemory._instances:
            self.__smem = SharedMemory._instances[self.__tagname]
            return

        self.__smem = mmap.mmap(-1, self.__real_size, tagname=self.__tagname, access=mmap.ACCESS_WRITE)
        self.__smem.seek(0)
        if self.__smem.read(self.__real_size).strip(b'\x00'):
            raise SharedMemory.ExistsError('already exists')
        # 末尾增1 判断锁是否存在
        self.__smem.seek(self.__size)
        self.__smem.write(b'0')
        SharedMemory._instances[self.__tagname] = self.__smem

    def lock(self):
        self.__smem.seek(self.__size)
        self.__smem.write(b'1')

    def unlock(self):
        self.__smem.seek(self.__size)
        self.__smem.write(b'0')

    def is_locked(self):
        self.__smem.seek(self.__size)
        return self.__smem.read(1).decode() == '1'

    def write(self, bstring: bytes, seek=0):
        if bstring.__class__ is str:
            bstring = bstring.encode()

        self.__smem.seek(seek)
        self.__smem.write(bstring)
        self.__smem.flush()

    def clear(self):
        self.__smem.seek(0)
        self.__smem.write(b'\x00'*self.__size)
        self.__smem.flush()

    def _read(self, length, size, seek):
        if size <= 0:
            size = length
        size = min(length - seek, size)
        self.__smem.seek(seek)
        return self.__smem.read(size)

    def read(self, size=-1, seek=0):
        return self._read(self.__size, size, seek)

    def read_real(self, size=-1, seek=0):
        return self._read(self.__real_size, size, seek)

    def close(self):
        self.__smem.seek(0)
        self.__smem.close()

    def is_closed(self):
        return self.__smem.closed


def init_shared_memory():
    smem = SharedMemory("TempLauncher", 1024)
    smem_create(smem)
    if smem.is_blank():
        smem.lock()
        smem.write(b'00000')
        smem.unlock()


def exe_already_opened(type_name):
    smem = SharedMemory("TempLauncher", 1024)
    smem_create(smem)
    state = smem.read().decode()
    state = state.replace('\x00', '0')
    name_to_opened = {
        'app': bool(int(state[0])),
        'updater': bool(int(state[1])),
        'admon': bool(int(state[2])),
    }
    return name_to_opened[type_name]


def set_exe_already_opened(type_name, value):
    value = int(value)
    name_to_index = {
        'app': 0,
        'updater': 1,
        'damon': 3,
    }
    smem = SharedMemory("TempLauncher", 1024)
    smem_create(smem)
    smem.lock()
    smem.write(str(value).encode(), name_to_index[type_name])
    smem.unlock()


def set_should_open_management_panel(value):
    value = int(value)
    smem = SharedMemory("TempLauncher", 1024)
    smem_create(smem)
    smem.lock()
    smem.write(str(value).encode(), 2)


def check_should_open_management_panel():
    smem = SharedMemory("TempLauncher", 1024)
    smem_create(smem)
    state = smem.read().decode()
    state = state.replace('\x00', '0')
    if bool(int(state[2])):
        set_should_open_management_panel(False)
        return True
    else:
        return False


def smem_create(smem):
    try:
        smem.create()
    except:
        pass


def save_path():
    if in_win:
        return "C:/Users/Public/Documents/PapeLauncher"
    elif in_mac:
        return os.path.join(os.path.expanduser("~"), "Documents/PapeLauncher")
    else:
        raise ""


def makesure_file_R(file):
    if not os.path.exists(file):
        return

    if not os.access(file, os.R_OK):
        os.chmod(file, 0o755)


def makesure_file_RW(file):
    if not os.path.exists(file):
        return

    if not os.access(file, os.W_OK) or not os.access(file, os.R_OK):
        os.chmod(file, 0o766)


def makesure_file_RWX(file):
    if not os.path.exists(file):
        return

    if not os.access(file, os.W_OK) or not os.access(file, os.R_OK) or not os.access(file, os.X_OK):
        os.chmod(file, 0o777)


def makesure_folder_RW(folder):
    if not os.path.exists(folder):
        return

    modify_permission(folder, 0o766)


def makesure_folder_RWX(folder):
    if not os.path.exists(folder):
        return

    modify_permission(folder, 0o777)


def modify_permission(folder, permission):
    for relpath, dirs, files in os.walk(folder):
        for dir in dirs:
            dir_path = os.path.join(folder, relpath, dir)
            os.chmod(dir_path, permission)

        for file in files:
            file_path = os.path.join(folder, relpath, file)
            os.chmod(file_path, permission)


def is_safe_path(path):
    for c in path:
        if ord(c) > 127:
            return False
    return True


def find_dir(start_folder, dir_name):
    for relpath, dirs, files in os.walk(start_folder):
        if dir_name in dirs:
            full_path = os.path.join(start_folder, relpath, dir_name)
            return True, full_path
    return False, None


def find_file(start_folder, file_name):
    for relpath, dirs, files in os.walk(start_folder):
        if file_name in files:
            full_path = os.path.join(start_folder, relpath, file_name)
            return True, full_path
    return False, None


def find_files(start_folder, file_name):
    exist_files = []
    for relpath, dirs, files in os.walk(start_folder):
        if file_name in files:
            full_path = os.path.join(start_folder, relpath, file_name)
            exist_files.append(full_path)
    return exist_files


def trans_key_to_folder(key):
    splits = key.split("_", 1)
    md5 = splits[0][:8]
    other = splits[1]

    temp = {
        "Release": "R",
        "Debug": "D",
        "PreRelease": "P",
        "Windows": "win",
        "Mac": "mac",
    }
    for k, v in temp.items():
        other = other.replace(k, v)
    return f"{md5}_{other}"


def get_unity_exe_path(install_folder):
    if in_win:
        full_path = os.path.join(install_folder, "Windows/WindowsEditor/Unity.exe")
        if not os.path.exists(full_path):
            find, full_path = find_file(install_folder, "Unity.exe")
            if find:
                return full_path
        return full_path
    elif in_mac:
        # find, full_path = find_file(install_folder, "Unity")
        # if find:
        #     return full_path
        return os.path.join(install_folder, "Mac/MacEditor/Unity.app/Contents/MacOS/Unity")
    else:
        raise ""


def get_unityCrash_exe_path(install_folder):
    if in_win:
        # find, full_path = find_file(install_folder, "Unity.exe")
        # if find:
        #     return full_path
        return os.path.join(install_folder, "Windows/WindowsEditor/Data/Tools/UnityCrashHandler64.exe")
    elif in_mac:
        return ""
    else:
        raise ""


def get_unity_dotnet_exe_path(install_folder):
    if in_win:
        full_path = os.path.join(install_folder, "Windows/WindowsEditor/Data/NetCore/Sdk-2.2.107/dotnet.exe")
        if not os.path.exists(full_path):
            find, full_path = find_file(os.path.join(install_folder, "Windows/WindowsEditor/Data"),
                                        "dotnet.exe")
            if find:
                return full_path
        return full_path
    elif in_mac:
        return ""
    else:
        raise ""


def get_unity_VBCSCompiler_exe_path(install_folder):
    if in_win:
        # find, full_path = find_file(install_folder, "VBCSCompiler.exe")
        # if find:
        #     return full_path
        return os.path.join(install_folder, "Windows/WindowsEditor/Data/Tools/Roslyn/VBCSCompiler.exe")
    elif in_mac:
        return ""
    else:
        raise ""


def checkUnityProject(path):
    asset_path = os.path.join(path, "Assets")
    if not os.path.exists(asset_path):
        return False
    return True


def copydir(from_dir, to_dir):
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    files = os.listdir(from_dir)
    for f in files:
        from_file = os.path.join(from_dir, f)
        to_file = os.path.join(to_dir, f)
        if os.path.isdir(from_file):
            copydir(from_file, to_file)
        else:
            shutil.copy(from_file, to_file)


def prettyXml(element, indent="\t", newline="\n", level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作






