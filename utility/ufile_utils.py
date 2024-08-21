import http
import json
import logging
import os.path
import threading
import time
from enum import Enum
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import requests
from requests_toolbelt import MultipartEncoder

from ufile import config, filemanager, multipartuploadufile


PublicKey = "4TpzVeImxSl7JZuZD4ZcKx37LdQs"
PrivateKey = "FBhtPo09orRBb2prh7sdjXJPvSn80jcDWEA1ZS8cPnUl"


class Region(Enum):
    region_wlcb = "华北二"


us3_region_dict = {
    Region.region_wlcb: ".cn-wlcb.ufileos.com"
}


class UfileManager:
    def __init__(self, public_key, private_key, buckey, suffix_region):
        self.public_key = public_key
        self.private_key = private_key
        self.buckey = buckey

        self.upload_suffix = us3_region_dict[suffix_region]
        self.download_suffix = self.upload_suffix

        self.ufile_handler = filemanager.FileManager(self.public_key,
                                                     self.private_key,
                                                     self.upload_suffix,
                                                     self.download_suffix)

    @staticmethod
    def get_wlcb_handle():
        return UfileManager(PublicKey, PrivateKey,
                            "ai-center-ml-dataset", Region.region_wlcb)

    def get_file_list(self, prefix, header=None, sub_prefix=False):
        marker = ""
        limit = 500
        file_list = []
        while True:
            ret, resp = self.ufile_handler.getfilelist(self.buckey,
                                                       prefix=prefix,
                                                       marker=marker,
                                                       limit=limit,
                                                       header=header)

            for content in ret["DataSet"]:
                file_path = content["FileName"]
                if file_path[-1] == "/":
                    continue
                if sub_prefix:
                    file_path = file_path[len(prefix):]

                file_path = file_path.strip("/")
                file_list.append(file_path)

            marker = ret["NextMarker"]
            # it sames some problem, contents length show less than maxkeys, right?
            if len(marker) <= 0 or limit < len(ret["DataSet"]):
                break

        return file_list

    def list_objects(self, prefix, delimiter="", header=None, sub_prefix=False):
        marker = ""
        maxkeys = 500
        file_list = []
        while True:
            ret, resp = self.ufile_handler.listobjects(self.buckey, prefix=prefix,
                                                       marker=marker, maxkeys=maxkeys,
                                                       delimiter=delimiter, header=header)
            assert resp.status_code == 200

            for content in ret["Contents"]:
                file_path = content["Key"]
                if file_path[-1] == "/":
                    continue
                if sub_prefix:
                    file_path = file_path[len(prefix):]

                file_path = file_path.strip("/")
                file_list.append(file_path)

            marker = ret["NextMarker"]
            # it sames some problem, contents length show less than maxkeys, right?
            if len(marker) <= 0 or maxkeys < len(ret["Contents"]):
                break

        return file_list

    def put_file(self, local_file, remote_file):
        ok = False
        error = ""
        for i in range(1, 4):
            try:
                ret, resp = self.ufile_handler.putfile(self.buckey,
                                                       remote_file,
                                                       local_file)

                if resp.status_code == 200:
                    ok = True
                    return True
                else:
                    ok = False
                    error = resp.error
                    logging.error(f"put file {local_file} failed. Error : {error}")
                    continue
            except Exception as ex:
                logging.error(f"put file {local_file} failed. Exception : {ex}")
                return ok

        if not ok:
            logging.error(f"put file {local_file} failed. Error : {error}")

        return ok

    def multipart_upload_file(self, local_file, remote_file):
        multipart_ufile_handler = multipartuploadufile.MultipartUploadUFile(
            self.public_key,
            self.private_key,
            self.upload_suffix
        )

        ret, resp = multipart_ufile_handler.uploadfile(self.buckey,
                                                       remote_file,
                                                       local_file)
        while True:
            if resp.status_code == 200:
                break
            elif resp.status_code == -1:
                ret, resp = multipart_ufile_handler.resumeuploadfile()
            else:
                logging.error(resp.error)
                break

    def put_folder(self, local_folder, remote_folder):
        if not os.path.exists(local_folder):
            return

        task = []
        start = datetime.now()
        for rel, dirs, files in os.walk(local_folder):
            for file in files:
                file_path = trans_path(os.path.join(rel, file))
                sub_path = file_path[len(local_folder):].strip("/")
                remote_file_path = trans_path(os.path.join(remote_folder, sub_path))

                task.append((file_path, remote_file_path))

        for filepath, remote_filepath in task:
            result = self.put_file(filepath, remote_filepath)
            if result:
                continue
            else:
                raise Exception(f"put file({filepath}) error, task failed")

        logging.info(f"put folder cost {datetime.now() - start}")

    def put_folder_threading(self, local_folder, remote_folder, timeout=1200):
        if not os.path.exists(local_folder):
            return

        task = []
        start = datetime.now()
        for rel, dirs, files in os.walk(local_folder):
            for file in files:
                file_path = trans_path(os.path.join(rel, file))
                sub_path = file_path[len(local_folder):].strip("/")
                remote_file_path = trans_path(os.path.join(remote_folder, sub_path))

                task.append((file_path, remote_file_path))

        with ThreadPoolExecutor(max_workers=10) as pool:
            all_task = []
            for filepath, remote_filepath in task:
                if os.path.getsize(filepath) > 1024*1024*1024:
                    all_task.append(pool.submit(self.multipart_upload_file, filepath, remote_filepath))
                else:
                    all_task.append(pool.submit(self.put_file, filepath, remote_filepath))

            done, all_task = wait(all_task, return_when=ALL_COMPLETED,
                                  timeout=timeout)
            if len(all_task) > 0:
                raise Exception(f"upload process error, some file not upload!!!\n{local_folder}")

        logging.info(f"put folder cost {datetime.now() - start}")

    def download_file(self, remote_file, local_file):
        if not os.path.exists(os.path.dirname(local_file)):
            os.makedirs(os.path.dirname(local_file), exist_ok=True)

        ret, resp = self.ufile_handler.download_file(self.buckey,
                                                     remote_file,
                                                     local_file)

        if resp.status_code == 200:
            return True
        else:
            logging.error(resp)
            return False

    def download_folder(self, remote_folder: str, local_folder: str):
        if not os.path.exists(local_folder):
            os.makedirs(local_folder, exist_ok=True)

        task = []
        start = datetime.now()
        for file in self.get_file_list(remote_folder, sub_prefix=True):
            file_path = trans_path(os.path.join(local_folder, file))
            remote_file_path = trans_path(os.path.join(remote_folder, file))

            task.append((file_path, remote_file_path))

        all_task = []
        with ThreadPoolExecutor(max_workers=30) as pool:
            for filepath, remote_filepath in task:
                all_task.append(pool.submit(self.download_file, remote_filepath, filepath))

            wait(all_task, return_when=ALL_COMPLETED)

            # result = self.download_file(remote_filepath, filepath)
            # if result:
            #     continue
            # else:
            #     raise Exception(f"download file({filepath}) error, task failed")

        logging.info(f"download folder cost {datetime.now() - start}")

    def delete_file(self, remote_file):
        ret, resp = self.ufile_handler.deletefile(self.buckey,
                                                  remote_file)

        if resp.status_code == 204:
            return True
        else:
            logging.error(resp.error)
            return False

    # def delete_folder(self, remote_file):
    #     ret, resp = self.ufile_handler.deletefile(self.buckey,
    #                                               remote_file)
    #
    #     if resp.status_code == 204:
    #         return True
    #     else:
    #         logging.error(ret)
    #         return False

    def wait_for_sync_juice(self, remote_file_folder, timeout=1800):
        data = {
            "us3_path": remote_file_folder,
            "bucket_name": "ai-center-ml-dataset",
            "jfs_vol_name": "aigc-dataset-ucw"
        }
        data = MultipartEncoder(fields=data)
        headers = {'Content-Type': data.content_type}
        rep = requests.post("http://117.50.196.21/jfs/sync_us3_files",
                            headers=headers, data=data)
        if rep.status_code == 200:
            result = json.loads(rep.text)
            if result["has_error"]:
                raise Exception(f"sync_us3_files异常，{rep.text}")
            else:
                task_id = result["task_id"]
        else:
            raise Exception(f"sync_us3_files异常，{rep.text}")

        wait_result = False
        temp_time = datetime.now()

        while True:
            time.sleep(5)

            rep = requests.get(f"http://117.50.196.21/jfs/{task_id}")
            if rep.status_code == 200:
                result = json.loads(rep.text)
                if result["has_error"]:
                    raise Exception(f"sync_us3_files异常，{rep.text}")
                else:
                    result = result["task_finished"]
                    if result:
                        wait_result = True
            else:
                raise Exception(f"sync_us3_files异常，{rep.text}")

            if wait_result:
                break

            if (datetime.now() - temp_time).total_seconds() > timeout:
                break

        if not wait_result:
            raise Exception(f"sync_us3_files异常，timeout error")


def trans_path(path:str):
    return path.replace("\\", "/")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ufile_handle = UfileManager.get_wlcb_handle()

    result = ufile_handle.get_file_list("dataset/ai_result/2024.08.06/")
    print(len(result))

    ufile_handle.download_folder("dataset/ai_result/2024.08.06/",
                                 f"D:/")











