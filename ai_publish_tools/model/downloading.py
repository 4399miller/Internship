from enum import Enum


class DownloadStatus(Enum):
    start = 1,
    downloading = 2,
    installing = 3,
    end = 4,
    update = 5,
    uninstall = 6,
    uninstall_end = 7,
    error = 10,
    update_error = 11,
    uninstall_error = 12,
    install_error = 13,



