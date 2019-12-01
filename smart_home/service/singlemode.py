# Date='2019/9/30 20:15'
# File Name='singlemode'
# AUTHOR='Tony'


def Singleton(cls):
    _instance = {}

    def _singleton(*args):
        if cls not in _instance:
            _instance[cls] = cls(*args)
        return _instance[cls]

    return _singleton