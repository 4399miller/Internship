from enum import Enum

from utility.singleton import Singleton

class MessageEnum(Enum):
    RefreshWorkSpace = 1,
    NotifyMessage = 2,
    ActiveHomeWindow = 3,
    OpenLabelStudio = 4,
    OpenLookTriplesView = 5,






class MessageCenter(Singleton):
    __message_container = {}

    def __add_listener(self, key, func):
        if key not in self.__message_container:
            self.__message_container[key] = []
        if func not in self.__message_container[key]:
            self.__message_container[key].append(func)

    def __remove_listener(self, key, func):
        if key in self.__message_container:
            if func in self.__message_container[key]:
                self.__message_container[key].remove(func)

    def __send_message(self, key, data):
        if key in self.__message_container:
            for func in self.__message_container[key]:
                func(data)

    @staticmethod
    def add(key, func):
        MessageCenter().__add_listener(key, func)

    @staticmethod
    def remove(key, func):
        MessageCenter().__remove_listener(key, func)

    @staticmethod
    def send(key, data):
        MessageCenter().__send_message(key, data)























