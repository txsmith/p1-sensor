import sys
from datetime import datetime

class DummyReader:

    def __init__(self):
        self.timestamp = '161218232000'
        self.trigger = False

    def readPacket(self):
        if self.trigger:
            raise Exception('DummyReader')
        self.timestamp = str(int(self.timestamp) + 10)
        self.trigger = True
        return P1Packet(self.timestamp, 374.72, 425.357, 0.200, 0, 1)

class Reader:
    def readPacket(self):
        _timestamp = None
        _t1 = None
        _t2 = None
        _kWhUsage = None
        _ampUsage = None
        _currentTariff = None

        for line in sys.stdin:
            if '0-0:1.0.0' in line:
                _timestamp = line.split('(')[1].split('W')[0]
            elif '1-0:1.8.1' in line:
                _t1 = line.split('(')[1].split('*')[0]
            elif '1-0:1.8.2' in line:
                _t2 = line.split('(')[1].split('*')[0]
            elif '1-0:1.7.0' in line:
                _kWhUsage = line.split('(')[1].split('*')[0]
            elif '1-0:31.7.0' in line:
                _ampUsage = line.split('(')[1].split('*')[0]
            elif '0-0:96.14.0' in line:
                _currentTariff = line.split('(')[1].split(')')[0]
            elif '!' in line:
                if _timestamp and _t1 and _t2 and _kWhUsage and _ampUsage and _currentTariff:
                    return P1Packet(_timestamp, float(_t1), float(_t2), float(_kWhUsage), float(_ampUsage), int(_currentTariff))

class P1Packet:
    def __init__(self, timestamp, t1, t2, kWhUsage, ampUsage, currentTariff):
        self.timestamp = timestamp
        self.t1 = t1
        self.t2 = t2
        self.kWhUsage = kWhUsage
        self.ampUsage = ampUsage
        self.currentTariff = currentTariff

    def getDatetime(self):
        year = 2000 + int(self.timestamp[0:2])
        month = int(self.timestamp[2:4])
        day = int(self.timestamp[4:6])
        hour = int(self.timestamp[6:8])
        minute = int(self.timestamp[8:10])
        seconds = int(self.timestamp[10:12])
        return datetime(year, month, day, hour, minute, seconds)
