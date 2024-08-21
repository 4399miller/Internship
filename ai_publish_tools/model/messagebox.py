from enum import IntEnum


class LogType(IntEnum):
    Success = 1,
    Info = 2,
    Warning = 3,
    Error = 4,


class MessageBoxInfo:
    WARNING = "警告"
    ERROR = "错误"
    TIP = "提示"

    def __init__(self, type, title, content, call=None):
        self.type = type
        self.title = title
        self.content = content
        self.call = call


class NotifyInfo:
    def __init__(self, title, content, mseconds=10000):
        self.title = title
        self.content = content
        self.mseconds = mseconds







