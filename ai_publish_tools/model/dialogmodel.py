from enum import Enum, IntEnum


class DialogType(IntEnum):
    Success = 1,
    Info = 2,
    Warning = 3,
    Error = 4,


class DialogButton(IntEnum):
    Ok = 1,
    Close = 2,
    Sure = 3,
    Yes = 4,
    No = 5,
    Open = 6,
    Quit = 7,
    Update_Immediately = 8,
    Update_After = 9,
    Cancel = 10,
    P4Switch_NoSync = 11,


BUTTON_REFLECTION = {
    DialogButton.Ok: "确定",
    DialogButton.Close: "关闭",
    DialogButton.Sure: "当然",
    DialogButton.Yes: "确定",
    DialogButton.No: "关闭",
    DialogButton.Open: "打开",
    DialogButton.Quit: "退出",
    DialogButton.Update_Immediately: "马上更新",
    DialogButton.Update_After: "今天暂不提示",
    DialogButton.Cancel: "取消",
    DialogButton.P4Switch_NoSync: "切换(不拉取最新)",

}


class DialogData:
    def __init__(self, logtype, title, content, callback=None, button1=None,
                 button2=None, *args):
        self.logType = logtype
        self.title = title
        self.content = f"{content}"
        self.callback = callback
        self.buttons = []
        if button1 is not None and isinstance(button1, DialogButton):
            self.buttons.append(button1)
        if button2 is not None and isinstance(button2, DialogButton):
            self.buttons.append(button2)
        for arg in args:
            if isinstance(arg, DialogButton):
                self.buttons.append(arg)
        if len(self.buttons) == 0:
            self.buttons.append(DialogButton.Close)


