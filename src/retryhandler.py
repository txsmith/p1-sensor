import sys, time, threading, os, traceback, logging
from queue import Queue

class RetryHandler:
    def __init__(self, evaluator, maxTries = 10, waitTimeSeconds = 2, expBackoff = True, maxQueued = 0):
        self._evaluator = evaluator
        self._maxTries = maxTries
        self._waitTime = waitTimeSeconds
        self._expBackoff = expBackoff
        self._queue = Queue(maxQueued)
        self._tries = 0
        self._failedRequest = None

    def startWorker(self):
        def worker():
            logging.debug("Started queue-worker")
            while True:
                self._processQueue()

        self._workerThread = threading.Thread(name="queue-worker", target=worker)
        self._workerThread.daemon = True
        self._workerThread.start()

    def enqueue(self, r):
        self._queue.put(r)

    def _processQueue(self):
        request = None
        if not self._failedRequest == None:
            logging.info('Retrying failed request')
            request = self._failedRequest
        else:
            logging.debug('Processing queued request (' + str(self._queue.qsize()) + ' remaining)')
            request = self._queue.get()

        try:
            self._evaluator.eval(request)
            logging.debug('Successfully handled request')
            self._tries = 0
            self._failedRequest = None
        except Exception:
            logging.exception("Exception when evaluating request")
            self._tries += 1
            self.checkMaxTries()
            self._failedRequest = request
            waitTime = self._comupteWaitTime()
            logging.warn(self._triesStr() + ' Retry in: ' + str(waitTime) + ' seconds')
            time.sleep(waitTime)

    def checkMaxTries(self):
        if self._tries >= self._maxTries:
            logging.error('Exceeded the maximum amount of retries! Shutting down.')
            os._exit(-1)

    def _triesStr(self):
        return '(' + str(self._tries) +  '/' +str(self._maxTries) + ')'

    def _comupteWaitTime(self):
        if self._expBackoff:
            return self._waitTime*(2**(self._tries-1))
        else:
            return self._waitTime
