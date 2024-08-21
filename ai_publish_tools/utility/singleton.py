

class Singleton(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
            cls._instance.new()
        return cls._instance

    def new(self) -> "run once in __new__":
        pass
