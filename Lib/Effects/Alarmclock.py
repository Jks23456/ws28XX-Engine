from Lib.SubEngine import SubEngine
from Lib.Objects.Container import Container
from threading import Timer
from datetime import datetime

class Signal:

    def __init__(self, pSubengine, pPixellength, pFrames, pSlowMotion=3):
        self.container = Container(pSubengine, pPixellength)
        self.maxFrames = pFrames
        self.once = False
        self.slowMotion = pSlowMotion
        self.count = 0
        self.isActive = False
        self.delete = False
        self.remove = False

    def setFrame(self):
        self.count = self.count + 1
        if self.count <= self.maxFrames:
            if self.count % self.slowMotion == 0:
                self.container.nextFrame()
        else:
            self.isActive = False
            self.delete = True
            if self.once:
                self.remove = True

    def remove(self):
        self.isActive = False
        self.delete = True


class Alarm:

    def __init__(self, pH, pM, pCicle, pSignal):
        self.time = pH, pM
        self.cicle = pCicle
        self.signal = pSignal

    def getNextAlarm(self, pTime):
            if self.cicle[pTime.weekday()]:
                if pTime.hour > self.time[0] or (pTime.hour == self.time[0] and pTime.minute >= self.time[1]):
                    return self.getNextAlarm(timeShift(pTime))
                else:
                    return (datetime(pTime.year, pTime.month, pTime.day, self.time[0], self.time[1]), self.signal)
            return None

    def setCicle(self, pDay, pVal):
        self.only = False
        if pDay > -1 and pDay < 7:
            self.cicle[pDay] = pVal


class Alarmclock(SubEngine):

    def __init__(self):
        SubEngine.__init__(self, "Alarmclock", 1)
        self.alarms = []
        self.schedual = []
        self.tSchedual = None
        self.tRefresh = None

    def timerSchedual(self):
        d = datetime.now()
        for alr in self.alarms:
            tmp = alr.getNextAlarm(d)
            if tmp != None:
                self.schedual.append(tmp)

        try:
            self.tRefresh.cancel()
        except Exception:
            pass
        self.setup()

    def timerRefresh(self):
        d = datetime.now()
        print("Refresh")
        print(datetime.now())
        for alr in self.schedual:
            print(alr)
            if alr[0] <= d and not alr[1].isActive:
                alr[1].isActive = True
        self.tRefresh = Timer(60, self.timerRefresh)
        self.tRefresh.start()

    def addAlarm(self, pHoure, pMinute, pSignal,pOnce=True, pSchedual=[False]*7,):
        time = datetime.now()
        pSignal.once = pOnce
        self.addObj(pSignal.container)
        if pOnce:
            if time.hour > pHoure or (time.hour == pHoure and time.minute >= pMinute):
                self.schedual.append((timeShift(datetime(time.year, time.month, time.day, pHoure, pMinute)), pSignal))
            else:
                self.schedual.append((datetime(time.year, time.month, time.day, pHoure, pMinute), pSignal))
        else:
            alr = Alarm(pHoure, pMinute, pCicle=pSchedual)
            sch = alr.getNextAlarm(time)
            if sch != None:
                self.schedual.append((sch, pSignal))
            self.alarms.append(alr)

    def removeAlarm(self, pAlarm):
        self.delObj(pAlarm.container)

    def setup(self):
        d = datetime.now()

        self.tRefresh = Timer(61-d.second, self.timerRefresh)
        self.tRefresh.start()

        self.tSchedual = Timer((((24 - d.hour) * 60) + (60 - d.minute)) * 60 + (60 - d.second), self.timerSchedual)
        self.tSchedual.start()

    def update(self):
        for alr in self.schedual:
            if alr[1].isActive:
                alr[1].setFrame()
            elif alr[1].delete:
                self.schedual.remove(alr)
                if alr[1].remove:
                    self.delObj(alr[1].container)

    def terminate(self):
        try:
            self.tSchedual.cancel()
        except Exception:
            pass

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