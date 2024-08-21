import functools


class Version:
    __first = 0
    __second = 0
    __third = 0
    __forth = 0

    def __init__(self, version):
        split = version.split('.')
        self.__first = int(split[0])
        self.__second = int(split[1])
        self.__third = int(split[2])
        if len(split) > 3:
            self.__forth = int(split[3])

    def __gt__(self, other):
        if self.__first > other.__first:
            return True
        elif self.__first == other.__first:
            if self.__second > other.__second:
                return True
            elif self.__second == other.__second:
                if self.__third > other.__third:
                    return True
                elif self.__third == other.__third:
                    if self.__forth > other.__forth:
                        return True
        return False

    def __lt__(self, other):
        return not self.__gt__(other) and not self.__eq__(other)

    def __eq__(self, other):
        return (self.__first == other.__first and self.__second == other.__second
                and self.__third == other.__third and self.__forth == other.__forth)

    @staticmethod
    def satisfy(version):
        try:
            return Version(version)
        except:
            return None

    def tostring(self):
        return f"{self.__first}.{self.__second}.{self.__third}{'.' + str(self.__forth) if self.__forth != 0 else ''}"


class RemoteCommonItem:
    def __init__(self, id, mode, version, number, force, platform):
        self.id = id
        self.mode = mode
        self.version = version
        self.number = number
        self.force = force == 1
        self.platform = platform

    @staticmethod
    def satisfy(data):
        keys = ["ID", "Mode", "Version", "BuildNumber", "ForceUpdate", "Platform"]
        for key in keys:
            if key not in data:
                return None
            if isinstance(data[key], str) and data[key] == "":
                return None

        if not Version.satisfy(data[keys[2]]):
            return None

        if data[keys[5]] is None:
            return None

        return RemoteCommonItem(data[keys[0]], data[keys[1]],
                                data[keys[2]], data[keys[3]], data[keys[4]],
                                data[keys[5]])


class LauncherVersionInfo:
    def __init__(self, data, mode, platform):
        self.newLauncher = None
        self.minLauncher = None

        remote_launchers = []
        for info in data:
            launcher = RemoteCommonItem.satisfy(info)
            if launcher is not None:
                if platform == launcher.platform and mode == launcher.mode:
                    remote_launchers.append(launcher)

        if len(remote_launchers) > 0:
            def cmp(x, y):
                if Version(x.version) > Version(y.version):
                    return 1
                elif Version(x.version) == Version(y.version):
                    if x.number > y.number:
                        return 1
                    else:
                        return -1
                else:
                    return -1

            remote_launchers = sorted(remote_launchers, key=functools.cmp_to_key(cmp), reverse=True)

            self.newLauncher = remote_launchers[0]
            for launcher in remote_launchers:
                if launcher.force:
                    self.minLauncher = launcher
                    break

    def satisfy(self):
        return self.newLauncher is not None and self.minLauncher is not None

    def get_new_launcher(self):
        return self.newLauncher

    def get_min_launcher(self):
        return self.minLauncher


class RemoteUnityItem:
    def __init__(self, _id, key, mode, platform, version, note, clearCache):
        self.id = int(_id)
        self.__key = key
        self.mode = mode
        self.platform = platform
        self.version = version
        self.note_url = note
        self.clear_cache = clearCache == "true"

        self.__path = self.__key.replace("_", "/")

    def key(self):
        return self.__key

    def path(self):
        return self.__path

    @staticmethod
    def satisfy(data):
        keys = ["ID", "Ekey", "Mode", "Platform", "Version", "Note", "Clearcache"]
        for key in keys:
            if key not in data:
                return None

        if not Version.satisfy(data[keys[4]]):
            return None

        return RemoteUnityItem(data[keys[0]], data[keys[1]], data[keys[2]],
                               data[keys[3]], data[keys[4]], data[keys[5]],
                               data[keys[6]])


class RemoteDepartmentItem:
    def __init__(self, _id, department, key, version, min_version, engines, name):
        self.id = str(_id)
        self.__department_name = department.replace(",", "_")
        self.__key = key
        self.version = version
        self.min_version = min_version
        self.cur_engine = RemoteUnityItem.satisfy(engines[0])
        self.min_engine = RemoteUnityItem.satisfy(engines[1])
        self.mode = self.cur_engine.mode
        self.platform = self.cur_engine.platform
        self.name = name
        self.note_url = self.cur_engine.note_url

        self.__path = self.__key.replace("_", "/")
        self.__department_key = f"{_id}_{self.__key}"

    def department_name(self):
        return self.__department_name

    def department_key(self):
        return self.__department_key

    def unity_key(self):
        return self.__key

    def path(self):
        return self.__path

    @staticmethod
    def satisfy(data):
        keys = ["ID", "Department", "Ekey", "Version", "MinVersion",
                "Engines", "Name"]
        for key in keys:
            if key not in data:
                return None

        if not Version.satisfy(data[keys[3]]) or not Version.satisfy(data[keys[4]]):
            return None

        if data[keys[5]] is None or not len(data[keys[5]]) >= 2:
            return None
        else:
            for engine in data[keys[5]]:
                if not RemoteUnityItem.satisfy(engine):
                    return None

        return RemoteDepartmentItem(data[keys[0]], data[keys[1]], data[keys[2]],
                                    data[keys[3]], data[keys[4]], data[keys[5]],
                                    data[keys[6]])


class RemoteUpdateItem:
    def __init__(self, _id, ekey, begin, end):
        self.id = int(_id)
        self.unity_key = ekey
        self.from_version = begin
        self.to_version = end

        self.__path = self.unity_key.replace("_", "/")

    def key(self):
        return self.unity_key

    def path(self):
        return self.__path

    @staticmethod
    def satisfy(data):
        keys = ["ID", "Ekey", "FromVersion", "ToVersion"]
        for key in keys:
            if key not in data:
                return None

        return RemoteUpdateItem(data[keys[0]], data[keys[1]], data[keys[2]],
                                data[keys[3]])


class RemoteUnityInfo:
    def __init__(self, department):
        self.department = department
        self.department_id = department.id
        self.department_key = department.department_key()
        self.department_name = department.department_name()
        self.unity_key = department.unity_key()
        self.mode = department.mode
        self.platform = department.platform
        self.name = department.name
        self.note_url = department.note_url

        self.new_unity = department.cur_engine
        self.min_unity = department.min_engine


class RemoteUnityVersionDetails:
    def __init__(self, unity_content, cur_platform):
        remote_unitys = {}
        self.__remote_unitys = remote_unitys

        if unity_content is not None:
            for info in unity_content:
                department_item = RemoteDepartmentItem.satisfy(info)
                if department_item is None:
                    continue
                # important
                if cur_platform not in department_item.unity_key():
                    continue

                if department_item.id not in remote_unitys:
                    remote_unitys[str(department_item.id)] = RemoteUnityInfo(department_item)

    def satisfy(self):
        return len(self.__remote_unitys) > 0

    def contain_unity(self, id):
        return id in self.__remote_unitys

    def get_remote_unity(self, id):
        if self.contain_unity(id):
            return self.__remote_unitys[id]
        else:
            return None

    def get_min_unity(self, id):
        if self.contain_unity(id):
            return self.__remote_unitys[id].min_unity
        else:
            return None

    def get_new_unity(self, id):
        if self.contain_unity(id):
            return self.__remote_unitys[id].new_unity
        else:
            return None

    def construct_by_mode(self):
        result = {}
        for key, unity in self.__remote_unitys.items():
            if unity.mode not in result:
                result[unity.mode] = []

            result[unity.mode].append(unity)
        return result


SDK_DOWNLOAD_START_NUMBER = 10000

class RemoteSDKItem:
    def __init__(self, _id, key, mode, platform):
        self.id = int(_id)
        self.key = key
        self.mode = mode
        self.platform = platform
        self.department_id = str(self.id + SDK_DOWNLOAD_START_NUMBER)

        self.__path = self.key.replace("_", "/")

    def path(self):
        return self.__path

    @staticmethod
    def satisfy(data):
        keys = ["ID", "Ekey", "Mode", "Platform"]
        for key in keys:
            if key not in data:
                return None

        return RemoteSDKItem(data[keys[0]], data[keys[1]], data[keys[2]],
                             data[keys[3]])


class RemoteSDKDetails:
    def __init__(self, data_content, cur_platform):
        remote_sdk = {}
        self.__remote_sdk = remote_sdk

        if data_content is not None:
            for info in data_content:
                item = RemoteSDKItem.satisfy(info)
                if item is None:
                    continue
                # important
                if cur_platform != item.platform:
                    continue

                if item.department_id not in remote_sdk:
                    remote_sdk[item.department_id] = item

    def construct_by_mode(self):
        result = {}
        for key, unity in self.__remote_sdk.items():
            if unity.mode not in result:
                result[unity.mode] = []

            result[unity.mode].append(unity)
        return result

    def contain_sdk(self, department_id):
        return department_id in self.__remote_sdk

    def get_remote_sdk(self, department_id):
        if self.contain_sdk(department_id):
            return self.__remote_sdk[department_id]
        else:
            return None


class RemoteInfoItem:
    def __init__(self, _id, des, title, openurl, order):
        self.id = int(_id)
        self.des = des
        self.title = title
        self.openurl = openurl
        self.order = int(order)

    @staticmethod
    def satisfy(data):
        keys = ["ID", "Description", "Title", "Url", "OrderInfo"]
        for key in keys:
            if key not in data:
                return None

        return RemoteInfoItem(data[keys[0]], data[keys[1]], data[keys[2]],
                              data[keys[3]], data[keys[4]])







