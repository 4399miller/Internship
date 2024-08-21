import json
import requests
import jwt

from requests_toolbelt import MultipartEncoder

from ..constant import *
from ..controller.userdatacontroller import *
from .message import *
from .logutility import LogUtility
from .timeutility import isLoginPreExpire


REQUEST_KEY = "Nikki@2022"
REQUEST_ENCODE = ["HS256"]


class DownFileType(Enum):
    launcher = 1,
    launcherupdater = 2,
    engine = 3,
    engineupdater = 4,
    manifest = 5,


class FileDownTaskInfo:
    def __init__(self, _id, filetype, filename, folder):
        self.id = _id
        self.filetype = filetype
        self.filename = filename
        self.folder = folder

        self.filepath = os.path.join(folder, filename)


class RequestTask:
    LogTag = "[RequestTask]"

    def __init__(self, url, data, success_call=None, fail_call=None, need_token=True, **kwargs):
        self.__token()
        self.__encode_data(data, need_token)
        self.rep = None
        self.success_callback = success_call
        self.fail_callback = fail_call
        self.url = url
        self.text = ""
        self.silent = False
        self.success = False
        self.status_code = 0
        self.timeout = 2
        self.retrytimes = 2

        if "slient" in kwargs.keys():
            self.silent = kwargs["slient"]
        if "timeout" in kwargs.keys():
            self.timeout = kwargs["timeout"]
        if "retrytimes" in kwargs.keys():
            self.retrytimes = kwargs["retrytimes"]

    def __token(self):
        self.token = ""
        if UserDataController().has(UserStatus.UserLoginToken):
            token = UserDataController().get(UserStatus.UserLoginToken)
            self.token = token

    def __encode_data(self, data, need_token):
        self.data = MultipartEncoder(fields=data)
        self.headers = {'Content-Type': self.data.content_type}
        if need_token:
            self.headers['token'] = self.token

    def post(self):
        index = 0
        err_message = "服务器异常响应，请检查内网连接"
        while index < self.retrytimes:
            try:
                index += 1
                log(f"{self.url} 第{index}次请求")
                rep = requests.post(self.url, data=self.data,
                                    headers=self.headers, timeout=self.timeout)
                self.rep = rep
                if rep.status_code != requests.codes.ok:
                    log(rep.status_code)
                    log(rep.reason)
                    err_message = f"服务器异常响应，请检查内网连接\n({rep.status_code} {rep.reason})"
                    self.success = False
                    break

                log(rep.status_code)
                try:
                    ok = self.__request_success(rep, index)
                    if not ok:
                        break
                except Exception as e:
                    log(f"request success post crash : \n{e}")
                    self.success = False
                    break

                if self.success:
                    return
            except:
                log(f"第{index}次请求 \n{traceback.format_exc()}")

        if not self.silent:
            MessageCenter.send(MessageEnum.OpenMessageBox, MessageBoxInfo(
                LogType.Warning, "请求失败", err_message))

        self.__request_failed()

    def post_new(self):
        index = 0
        err_message = "服务器异常响应，请检查内网连接"
        while index <= self.retrytimes:
            try:
                index += 1
                log(f"{self.url} 第{index}次请求")
                rep = requests.post(self.url, data=self.data,
                                    headers=self.headers, timeout=self.timeout)
                self.rep = rep
                if rep.status_code != requests.codes.ok:
                    log(rep.status_code)
                    log(rep.reason)
                    err_message = f"服务器异常响应，请检查内网连接\n({rep.status_code} {rep.reason})"
                    self.success = False

                    if not self.silent:
                        MessageCenter.send(MessageEnum.OpenMessageBox, MessageBoxInfo(
                            LogType.Warning, "请求失败", err_message))

                    return

                log(rep.status_code)
                try:
                    self.__request_end_call(rep, index)
                except Exception as e:
                    log(f"request success post crash : \n{e}")
                    self.success = False

                return
            except:
                log(f"第{index}次请求异常 \n{traceback.format_exc()}")
                return

    def get(self):
        index = 0
        err_message = "服务器异常响应"
        while index < self.retrytimes:
            try:
                index += 1
                log(f"{self.url} 第{index}次请求")
                rep = requests.get(self.url, data=self.data,
                                   headers=self.headers, timeout=self.timeout)
                self.rep = rep
                if rep.status_code != requests.codes.ok:
                    log(rep.status_code)
                    log(rep.reason)
                    err_message = f"服务器异常响应\n({rep.status_code} {rep.reason})"
                    self.success = False
                    break

                log(rep.status_code)
                try:
                    ok = self.__request_success(rep, index)
                    if not ok:
                        break
                except Exception as e:
                    log(f"request success get crash : \n{e}")
                    self.success = False
                    break

                if self.success:
                    return
            except:
                log(f"第{index}次请求 \n{traceback.format_exc()}")

        if not self.silent:
            MessageCenter.send(MessageEnum.OpenMessageBox, MessageBoxInfo(
                LogType.Warning, "请求失败", err_message))

        self.__request_failed()

    def __request_end_call(self, rep, index):
        content = json.loads(rep.text)
        if "code" in content:
            code = int(content["code"])
            if code == requests.codes.ok:
                self.success = True
                if self.success_callback is not None:
                    self.success_callback(content)
            else:
                self.success = False
                if self.fail_callback is not None:
                    self.fail_callback(content)
                log(f"{self.LogTag} failed: \n{self.url} 第{index}次请求，{code} : {rep.text}")
                return False
        else:
            self.success = False
            log(f"{self.LogTag} failed: \n{self.url} 第{index}次请求，请求返回体缺少字段code : {rep.text}")
        return True

    def __request_failed(self):
        if not self.success:
            if self.fail_callback is not None:
                self.fail_callback()

    def __request_success(self, rep, index):
        content = json.loads(rep.text)
        if "code" in content:
            code = int(content["code"])
            if code == requests.codes.ok:
                self.success = True
                if self.success_callback is not None:
                    self.success_callback(content)
            else:
                self.success = False
                log(f"{self.LogTag} failed: \n{self.url} 第{index}次请求，{code} : {rep.text}")
                return False
        else:
            self.success = False
            log(f"{self.LogTag} failed: \n{self.url} 第{index}次请求，请求返回体缺少字段code : {rep.text}")
        return True

    def filedown(self, filedown_task):
        try:
            folder = filedown_task.folder
            filepath = filedown_task.filepath
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

            log(f"{self.url}  {filedown_task.__dict__}")
            rep = requests.get(self.url, headers=self.headers,
                               stream=True, timeout=self.timeout)
            self.rep = rep
            if rep.status_code != requests.codes.ok:
                log(f"request {rep.status_code}")
                log(f"request {rep.reason}")
                self.success = False
                self.__request_failed()
                return

            log(rep.status_code)
            total_size = int(rep.headers["Content-Length"])
            if total_size < 1024*64:
                log(f"{self.url} failed bytes: {total_size} {rep.text} decode to json")
                self.success = False
                self.__request_failed()
                return

            log(f"{self.url} success bytes: {total_size}")
            if os.path.exists(filepath):
                os.remove(filepath)

            with open(filepath, "wb") as f:
                for chunk in rep.iter_content(chunk_size=1024*64):
                    f.write(chunk)
                    f.flush()

            self.success = True
            if self.success_callback is not None:
                self.success_callback(filepath)

        except:
            log(f"{self.LogTag} failed: \n {self.url} 第{0}次请求 \n {traceback.format_exc()}")
            self.success = False
            self.__request_failed()


class TokenInfo:
    def __init__(self, token):
        try:
            content = jwt.decode(token, REQUEST_KEY, REQUEST_ENCODE, options={"verify_exp": False})
            self.userid = content["userid"]
            self.username = content["username"]
            self.exp = content["exp"]
            self.avatar = content["avatar"]
            self.department = content["department"]
        except Exception as e:
            log(f"token decode crash : {e}")
            self.userid = ""
            self.username = ""
            self.exp = 0
            self.avatar = ""
            self.department = ""


def reqUserLogin(account, password, success, fail):
    data = {
        "name": account,
        "password": password,
    }
    task = RequestTask(REQUEST_USER_URL + "post", data, success, fail, retrytimes=1, timeout=5)
    task.post_new()

def reqVerifyUserLogin():
    def success(content):
        MessageCenter.send(MessageEnum.RefreshUserToken, None)
    task = RequestTask(REQUEST_USER_URL + "checktoken", {}, success, slient=True, retrytimes=1)
    task.get()

def verifyBeforeReq():
    verifyToken()

def verifyToken():
    if UserDataController().has(UserStatus.UserLoginToken):
        token = UserDataController().get(UserStatus.UserLoginToken)
        info = TokenInfo(token)
        ticks = info.exp
        if isLoginPreExpire(ticks):
            reqRefreshUserToken()

def reqRefreshUserToken():
    def success(content):
        if "data" in content:
            token = content["data"]
            UserDataController().set(UserStatus.UserLoginToken, token)

    task = RequestTask(REQUEST_USER_URL + "refreshtoken", {}, success, slient=True)
    task.get()

def reqEngines(success, failed):
    verifyBeforeReq()
    task = RequestTask(REQUEST_ENGINE_URL + "all", {}, success, failed)
    task.get()

def reqEngineDiffEntry(ekey, from_version, to_version, success, failed):
    verifyBeforeReq()
    data = {
        "ekey": ekey,
        "fromversion": str(from_version),
        "toversion": str(to_version),
    }
    task = RequestTask(REQUEST_ENGINE_DIFF_URL + "fromto", data, success, failed, slient=True, timeout=5)
    task.post()

def reqLauncherVersion(platform, mode, success, failed):
    url = f"{REQUEST_LAUNCHER_URL}all?platform={platform}&mode={mode}"
    task = RequestTask(url, {}, success, failed, need_token=False)
    task.get()

def reqLauncherUpdateVersion(platform, mode, success, failed):
    url = f"{REQUEST_LAUNCHER_UPDATE_URL}all?platform={platform}&mode={mode}"
    task = RequestTask(url, {}, success, failed, need_token=False)
    task.get()

def reqDownloadFileNoToken(downfiletask, success, failed):
    if not isinstance(downfiletask.filetype, DownFileType):
        failed()
        return

    url = f"{REQUEST_DOWN_FILE_LAUNCHER}?id={str(downfiletask.id)}&type={str(downfiletask.filetype)[13:]}"
    task = RequestTask(url, {}, success, failed, need_token=False, slient=True)
    task.filedown(downfiletask)

def reqGetUserSDK(success, failed):
    url = f"{REQUEST_SDK_URL}getUserAvailableSdk"
    task = RequestTask(url, {}, success, failed)
    task.get()

def reqNeedClearCache(ekey, from_version, to_version, success, failed):
    url = f"{REQUEST_ENGINE_URL}checkclearcache?ekey={ekey}&from={from_version}&to={to_version}"
    task = RequestTask(url, {}, success, failed)
    task.get()

def reqPostCrashInfo(username, department, enginename, unity_key, version, message, file):
    url = f"{REQUEST_LOG_URL}addErrorLog"
    # url = "http://10.10.133.36:9000/api/v1/log/addErrorLog"
    data = {
        "username": username,
        "department": department,
        "enginename": enginename,
        "enginekey": unity_key,
        "engineversion": version,
        "message": message,
        "file": (os.path.basename(file), open(file, "rb"), "text/plain"),
    }
    task = RequestTask(url, data)
    task.post()

def reqGetWebInfo(success, failed):
    url = f"{REQUEST_WEB_URL}getAll"

    task = RequestTask(url, {}, success, failed)
    task.get()

def reqPostUpdateEngineDiffInfo(from_version, to_verion, unity_key, success, failed):
    url = f"{REQUEST_FEISHU_URL}getenginediff"
    data = {
        "from": from_version,
        "to": to_verion,
        "key": unity_key
    }
    task = RequestTask(url, data, success, failed, need_token=False, slient=True)
    task.post()

def log(text):
    LogUtility().info(f"{RequestTask.LogTag} {text}")


