import configparser
import os

CONFIG_FILE_PATH = 'user_config.ini'


def save_user_choice(section, option, value):
    """
    保存用户选择到配置文件
    :param section: 配置节
    :param option: 配置项
    :param value: 配置值
    """
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE_PATH):
        config.read(CONFIG_FILE_PATH)

    if not config.has_section(section):
        config.add_section(section)

    config.set(section, option, value)

    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)


def load_user_choice(section, option, default_value=None):
    """
    从配置文件中读取用户选择
    :param section: 配置节
    :param option: 配置项
    :param default_value: 默认值，如果配置项不存在则返回该值
    :return: 配置值
    """
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE_PATH):
        config.read(CONFIG_FILE_PATH)
        if config.has_option(section, option):
            return config.get(section, option)

    return default_value

if __name__ == "__main__":
    user_choice = input("输入工作目录：")
    save_user_choice('UserSettings', 'Workfolder', user_choice)

    pre_choice = load_user_choice('UserSettings', 'Workfolder')

    print(pre_choice)