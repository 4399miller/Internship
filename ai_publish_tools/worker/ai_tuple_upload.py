import glob
import logging
import os
import shutil
import traceback
from datetime import datetime

from utility.ufile_utils import UfileManager


def upload_result(upload_folder, remote_folder):
    ufile_handler = UfileManager.get_wlcb_handle()
    ufile_handler.put_folder_threading(upload_folder, remote_folder)


def get_all_images(root_dir):
    file_list = []
    for rel, dirs, files in os.walk(root_dir):
        file_list += [os.path.join(rel, f) for f in files if f.endswith(".png")]

    return file_list


def list_png_to_dir(output_folder, image_dirs: [str]):
    if len(image_dirs) == 0:
        return None

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder, ignore_errors=True)
    os.mkdir(output_folder)

    array_filelist = [get_all_images(image_dir) for image_dir in image_dirs]
    filecount = len(array_filelist[0])
    for files in array_filelist[1:]:
        if filecount != len(files):
            raise Exception(f"Error : file count not equal \n{image_dirs}")

    for i in range(filecount):
        for array in array_filelist:
            file = array[i]
            sub_folder = os.path.join(output_folder, f"{i:0>6d}")
            if not os.path.exists(sub_folder):
                os.mkdir(sub_folder)

            new_file = os.path.join(sub_folder, f"{os.path.basename(file)}")
            shutil.copyfile(file, new_file)

    return output_folder


def form_triple(folder_paths, copy_folder_root, remote_folder):
    try:
        if len(folder_paths) != 3:
            return False, "Error: The dictionary does not contain exactly 3 elements."

        list_png_to_dir(copy_folder_root, folder_paths)

        upload_result(copy_folder_root, remote_folder)

        return True, None
    except Exception as e:
        print(traceback.format_exc())
        return False, str(e)


if __name__ == "__main__":
    # upload_result("", "")



    pass



















