import glob
import logging
import os
import sys
import json

from datetime import datetime


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
            cls._instance.new()
        return cls._instance

    def new(self):
        pass


def trans_path(path):
    return path.replace("\\", "/")


def get_filename_without_ex(filepath):
    basename = os.path.basename(filepath)
    filename = os.path.splitext(basename)[0]
    return filename


def strftime_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def write_json(obj, file):
    with open(file, "w+", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


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


def clamp(n, min, max):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


def get_retarget_dst_filename(dst_char_name, file_name):
    file_name = get_filename_without_ex(file_name)
    if len(file_name) > 20:
        file_name = file_name[:20]
        logging.info(f"slice dst filename to {file_name}")

    file_name = f"[{file_name}][{dst_char_name}]"
    file_name = file_name + "Scene.fbx"
    return file_name


def get_mesh_dst_filename(dst_char_name, file_name):
    file_name = get_filename_without_ex(file_name)
    if len(file_name) > 20:
        file_name = file_name[:20]
        logging.info(f"slice dst filename to {file_name}")

    file_name = f"[{file_name}][{dst_char_name}]"
    return file_name
