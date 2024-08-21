
# 让插件可以动态扩展上下文菜单

from enum import Enum, auto


class ContextMenuType(Enum):
    CONTEXT_MENU_PROJECT = auto()
    CONTEXT_MENU_SDK = auto()
    CONTEXT_MENU_ACCOUNT = auto()
    CONTEXT_MENU_UNITY = auto()
    CONTEXT_MENU_TRAY = auto()

    CONTEXT_PROJECT_TASK = auto()


contextmenu_handlers = {}

context_progress_handlers = {}


def register_contextmenu_handler(menu_type, menu_handler):
    if menu_type in contextmenu_handlers:
        if menu_handler not in contextmenu_handlers[menu_type]:
            contextmenu_handlers[menu_type].append(menu_handler)
    else:
        contextmenu_handlers[menu_type] = [menu_handler]


def on_contextmenu(menu_type, menu, context):
    for handler in contextmenu_handlers.get(menu_type, []):
        handler(menu, context)


def register_context_progress_handler(menu_type, menu_handler):
    if menu_type in context_progress_handlers:
        if menu_handler != context_progress_handlers[menu_type]:
            context_progress_handlers[menu_type] = menu_handler
    else:
        context_progress_handlers[menu_type] = menu_handler


def on_progress(menu_type, context):
    if menu_type in context_progress_handlers:
        return context_progress_handlers[menu_type](context)





