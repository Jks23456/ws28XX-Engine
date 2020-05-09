from Lib.SubEngine import SubEngine
from threading import Timer
from datetime import datetime

class TimeKeeper:

    def __init__(self, pH, pM, pOnce=True):
        self.time = pH, pM
        self.only = True
        self.active = pOnce
        self.cicle = [False]*7

    def getNextAlarm(self, pTime):
        print(pTime.weekday())
        if self.active:
            if self.only:
                self.active = False
                if pTime.hour > self.time[0] or (pTime.hour == self.time[0] and pTime.minute <= self.time[1]):
                    return timeShift(pTime)
                else:
                    return datetime(pTime.year, pTime.month, pTime.day, self.time[0], self.time[1])
            elif self.cicle[pTime.weekday()]:
                return datetime(pTime.year, pTime.month, pTime.day, self.time[0], self.time[1])

    def setCicle(self, pDay, pVal):
        self.only = False
        if pDay > -1 and pDay < 7:
            self.cicle[pDay] = pVal


class Alarmclock(SubEngine):

    def __init__(self):
        SubEngine.__init__(self, "Alarmclock", 1)
        self.schedual = []
        self.timer = None

    def timerUpdate(self):
        self.timer = Timer(86400, self.timerUpdate)
        self.timer.start()

    def setup(self):
        d = datetime.now()
        self.timer = Timer((((23 - d.hour) * 60) + (60 - d.minute)) * 60 + (60 - d.second), self.timerUpdate)
        self.timer.start()

    def terminate(self):
        try:
            self.timer.cancel()
        except Exception:
            pass

    def update(self):
        time = datetime.now()

    def onMessage(self, topic, payload):
        pass

    def getStates(self):
        return None


def timeShift(pTime):
    pTime = datetime.now()
    retVal = None
    status = 0

    t = [pTime.year, pTime.month, pTime.day+1]

    while retVal == None:
        try:
            retVal = datetime(t[0], t[1], t[2], hour=pTime.hour, minute= pTime.minute)
        except ValueError as v:
            print(v)
            status = status + 1
            if status == 1:
                t[2] = 1
                t[1] = t[1] + 1
            elif status == 2:
                t[1] = 1
                t[0] = t[0] + 1
            else:
                return None
    return retVal
