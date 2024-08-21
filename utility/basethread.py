import threading


class BaseThread(threading.Thread):
    def __init__(self, callback=None, callback_args=(), *args, **kwargs):
        target = kwargs.pop('target')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.callback_args = callback_args
        self.method = target


    def target_with_callback(self):
        self.method()
        if self.callback is not None:
            self.callback(*self.callback_args)

