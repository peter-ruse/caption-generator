import threading


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_lock"):
            cls._lock = threading.Lock()

        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
