

class Cache(list):

    def __init__(self, size=16):
        super(Cache, self).__init__()
        if size > 0:
            self.size = size
        else:
            raise ValueError

    def append(self, item):
        super(Cache, self).append(item)
        if len(self) > self.size:
            self.pop(0)
