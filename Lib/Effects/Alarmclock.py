from Lib.SubEngine import SubEngine
from threading import Timer
from datetime import datetime

class Effect:

    def __init__(self, pSub, pFrames):
        self.count = 0



class Alarm:

    def __init__(self, pH, pM, pCicle):
        self.time = pH, pM
        self.cicle = pCicle

    def getNextAlarm(self, pTime):
            if self.cicle[pTime.weekday()]:
                if pTime.hour > self.time[0] or (pTime.hour == self.time[0] and pTime.minute >= self.time[1]):
                    return self.getNextAlarm(timeShift(pTime))
                else:
                    return datetime(pTime.year, pTime.month, pTime.day, self.time[0], self.time[1])

    def setCicle(self, pDay, pVal):
        self.only = False
        if pDay > -1 and pDay < 7:
            self.cicle[pDay] = pVal


class Alarmclock(SubEngine):

    def __init__(self):
        SubEngine.__init__(self, "Alarmclock", 1)
        self.alarms = []
        self.schedual = []
        self.timer = None

    def timerUpdate(self):
        d = datetime.now()
        for alr in self.alarms:
            tmp = alr.getNextAlarm(d)
            if tmp != None:
                self.schedual.append(tmp)

        self.timer = Timer(86400, self.timerUpdate)
        self.timer.start()

    def addAlarm(self, pHoure, pMinute, pOnce=True, pSchedual=[False]*7):
        time = datetime.now()
        if pOnce:
            if time.hour > pHoure or (time.hour == pHoure and time.minute >= pMinute):
                self.schedual.append(timeShift(datetime(time.year, time.month, time.day, pHoure, pMinute)))
            else:
                self.schedual.append(datetime(time.year, time.month, time.day, pHoure, pMinute))
        else:
            alr = Alarm(pHoure, pMinute, pCicle=pSchedual)
            sch = alr.getNextAlarm(time)
            if sch != None:
                self.schedual.append(sch)
            self.alarms.append(alr)

    def setup(self):
        d = datetime.now()
        self.timer = Timer((((24 - d.hour) * 60) + (60 - d.minute)) * 60 + (60 - d.second), self.timerUpdate)
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