import sys, logging, datetime
from calendar import monthrange

from p1reader import *
from firebaseops import *
from retryhandler import *
from sketch import *

from config import config

logging.getLogger('').handlers = []
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=config['logLevel'])

# fb = FirebaseLoggingEvaluator()
fb = FirebaseLiveEvaluator(config)
# fbE = FirebaseExceptionEvaluator(config)
handler = RetryHandler(fb, config['exceptionRetries'])
handler.startWorker()

def pushHourToFirebase(measurements):
    handler.enqueue(Node('measurements').child('hour').set(measurements))

def pushDayToFirebase(measurements):
    handler.enqueue(Node('measurements').child('day').set(measurements))

def pushWeekToFirebase(measurements):
    handler.enqueue(Node('measurements').child('week').set(measurements))

def pushMonthToFirebase(measurements):
    handler.enqueue(Node('measurements').child('month').set(measurements))

def pushYearToFirebase(measurements):
    handler.enqueue(Node('measurements').child('year').set(measurements))


logging.info('Fetching previous records...')
yearData = fb.eval(Node('measurements').child('year').get()).val()
monthData = fb.eval(Node('measurements').child('month').get()).val()
weekData = fb.eval(Node('measurements').child('week').get()).val()
dayData = fb.eval(Node('measurements').child('day').get()).val()
quarterData = fb.eval(Node('measurements').child('quarterHour').get()).val()

now = datetime.now()
daysInMonth = monthrange(now.year, now.month)[1]

yearSketch = Sketch(12, pushYearToFirebase)
if yearData:
    yearSketch.setData(yearData)

monthSketch = Sketch(daysInMonth, pushMonthToFirebase, [yearSketch])
if monthData:
    monthSketch.setData(monthData)

weekSketch = Sketch(5, pushWeekToFirebase)
if weekData:
    weekSketch.setData(weekData)

daySketch = Sketch(24*4, pushDayToFirebase, [weekSketch, monthSketch], lambda ms: sum(ms)/4)
if dayData:
    daySketch.setData(dayData)

# Live usage from the 15 minutes (90 measurements, one per 10 seconds)
quarterSketch = Sketch(90, lambda x: x, [daySketch], lambda ms: sum(ms)/90)
if quarterData:
    quarterSketch.setData(quarterData)

try:
    lastUpdate = fb.eval(Node('last-update').get()).val()
    lastMeasure = datetime.strptime(lastUpdate, '%Y-%m-%dT%H:%M:%S')
    logging.info('Last update was: ' + lastUpdate)
except:
    lastMeasure = None

try:
    logging.info('Waiting for input...')
    reader = Reader()

    packet = reader.readPacket()
    while packet:
        now = packet.getDatetime()

        handler.enqueue(Update({
            'last-update': now.isoformat(),
            'current-tariff': packet.currentTariff,
            'current-usage': packet.kWhUsage,
            't1-counter': packet.t1,
            't2-counter': packet.t2
        }))

        if lastMeasure:
            if not (int(lastMeasure.minute/60*4) == int(now.minute/60*4)):
                logging.debug('15 minutes passed')
                quarterSketch.propagateSummary()

            if not (lastMeasure.day == now.day):
                logging.debug('A day passed')
                daySketch.propagateSummary()

            if not (lastMeasure.isocalendar()[2] == now.isocalendar()[2]):
                logging.debug('A week passed')
                weekSketch.propagateSummary()

            if not (lastMeasure.month == now.month):
                logging.debug('A month passed')
                monthSketch.propagateSummary()
                monthSketch.resize(monthrange(now.year, now.month)[1])

        quarterSketch.rotate(now.isoformat(), packet.kWhUsage)
        lastMeasure = now
        packet = reader.readPacket()
except KeyboardInterrupt:
    sys.exit(0)

handler.joinWorker();
