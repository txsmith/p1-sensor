from peekqueue import *
import logging

class Sketch(object):
    'A range of measurements that can be summarized and forwarded to another Sketch'

    def __init__(self, amount, onRotate, nextSketches = None, sumFn = sum):
        self._sketchSize = amount
        self._onRotate = onRotate
        self._next = nextSketches
        self._queue = Queue()
        self._sum = sumFn

    def rotate(self, timestamp, newMeasurement):
        logging.debug('Sketch({}): received new measurement'.format(self._sketchSize))
        if self._queue.size() == self._sketchSize:
            self._queue.pop()
        self._queue.push({'t': timestamp, 'x': newMeasurement})
        self._onRotate(self._queue.toList())

    def propagateSummary(self):
        if self._next:
            logging.debug('Sketch({}): full rotation complete, propagating'.format(self._sketchSize))
            summary = self.sumMeasurements(self._queue.toList())
            for s in self._next:
                s.rotate(summary['t'], summary['x'])

    def resize(self, newSize):
        self._sketchSize = newSize
        while (self._queue.size() > newSize):
            self._queue.pop()

    def setData(self, data):
        for item in data:
            self._queue.push(item)

    def sumMeasurements(self, measurements):
        lastTimestamp = None
        s = []
        for m in measurements:
            s.append(m['x'])
            lastTimestamp = m['t']

        return {'t': lastTimestamp, 'x': self._sum(s)}
