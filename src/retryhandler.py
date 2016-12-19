import sys, time, threading, os, traceback, logging
from peekqueue import *

class RetryHandler:
    def __init__(self, evaluator, maxTries = 10, waitTimeSeconds = 2, expBackoff = True, maxQueued = 0):
        self._evaluator = evaluator
        self._maxTries = maxTries
        self._waitTime = waitTimeSeconds
        self._expBackoff = expBackoff
        self._queue = Queue(maxQueued)
        self._tries = 0
        self._inGracePeriod = False
        self._graceTimer = None

    def tryEval(self, node):
        self._queue.push(node)
        if self._inGracePeriod:
            logging.debug('Grace period is not yet over, queueing request...')
        else:
            self._processQueue()

    def _processQueue(self):
        logging.debug('Processing queued requests (' + str(self._queue.size()) + ' remaining)')
        success = self._doTryEval(self._queue.peek())
        if (success):
            logging.debug('Successfully handled request')
            self._queue.pop()
            if not self._queue.empty():
                self._processQueue()

    def _doTryEval(self, node):
        try:
            self._evaluator.eval(node)
            self._tries = 0
            return True
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            self._tries += 1
            self.checkMaxTries()
            self.grace()
            return False

    def checkMaxTries(self):
        if self._tries >= self._maxTries:
            logging.error('Exceeded the maximum amount of retries!')
            os._exit(-1)

    def _triesStr(self):
        return '(' + str(self._tries) +  '/' +str(self._maxTries) + ')'

    def grace(self):
        self._inGracePeriod = True
        waitTime = self._comupteWaitTime()
        waitTime = self._comupteWaitTime()

        def endGrace():
            success = self._processQueue()
            self._inGracePeriod = not success

        self._graceTimer = threading.Timer(waitTime, endGrace)
        self._graceTimer.start()
        logging.warn(self._triesStr() + ' An exception occured. Retry in: ' + str(waitTime) + ' seconds')

    def _comupteWaitTime(self):
        if self._expBackoff:
            return self._waitTime**self._tries
        else:
            return self._waitTime
