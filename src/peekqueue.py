
class Full(Exception):
    pass

class Empty(Exception):
    pass

class Queue(object):
    def __init__(self, maxSize = 0):
        self._list = []
        self._maxQueued = maxSize

    def push(self, i):
        if self._maxQueued and len(self._list) >= self._maxQueued:
            raise Full
        else:
            self._list.append(i)

    def pop(self):
        if (len(self._list) == 0):
            raise Empty
        else:
            r = self._list[0]
            del self._list[0]
            return r

    def peek(self):
        if (len(self._list) == 0):
            raise Empty
        else:
            return self._list[0]

    def empty(self):
        return len(self._list) == 0

    def size(self):
        return len(self._list)

    def toList(self):
        return self._list
