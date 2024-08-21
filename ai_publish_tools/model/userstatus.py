import os
import sys
from enum import Enum

from ..utility.commonutility import *

# TODO 添加后需同步UserDataController._status_never_changelist
class UserStatus(Enum):
    DownloadTempPath = 0
    InstallUnityPath = 1
    # TempPath = 2
    UserLoginToken = 3
    UserAccount = 4

    CreateProjectFolder = 5
    LocalUnityIncreaseID = 6,
    LocalProjectIncreaseID = 7,
    AutoUpdateUnity = 8,
    UpdateUnityTempDict = 9,

    PluginSettings = 10,
    ReqRemoteWebInfoTick = 11,
    ProjectDefaultUnityID = 12,


class AppData:
    m_Root = os.path.abspath(os.path.dirname(sys.argv[0])).replace('\\', '/')
    m_UserRoot = os.path.expanduser('~')

    m_DataPath = m_Root + "/data"
    m_Preference = m_DataPath + "/preference"

    m_TempPath = m_Root + "/temp"
    m_DownloadTempPath = m_TempPath
    m_InstallUnityPath = os.path.join(m_Root[:3], "Unity")
    if not in_mac:
        m_InstallUnityPath = os.path.join(m_UserRoot, "Unity")

    m_SaveRoot = save_path()
    m_NewDataPath = m_SaveRoot + "/data"
    m_NewPerference = m_NewDataPath + "/preference"
    m_UnityCache = m_NewDataPath + "/unityVersionCache.txt"
    m_ProjectCache = m_NewDataPath + "/projectCache.txt"
    m_SDKCache = m_NewDataPath + "/sdkCache.txt"


# 不再使用
class UserData:
    m_DownloadTempPath = AppData.m_DownloadTempPath
    m_InstallUnityPath = AppData.m_InstallUnityPath

