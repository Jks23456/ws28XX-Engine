from Lib.SubEngine import SubEngine
from Lib.Objects.Panel import Panel

from random import randrange
import colorsys


class Elements(SubEngine):

    def __init__(self):
        super().__init__("FadingDot", 1)
        self.clock = 0
        self.baseAngle = 55 #FireAngle=10, WaterAngle=60, AirAngle=55,  EarthAngle=30,

    def setup(self):
        self.panel = Panel()
        self.panel.gauss(True)
        self.addObj(self.panel)
        self.createMap(5)

    def createMap(self, pAggressive):
        self.map = []
        for _ in range(self.pixellength):
            self.map.append(randrange(self.baseAngle - pAggressive, self.baseAngle + pAggressive, 1))
        self.mapToObj()

    def update(self):
        self.mutate()
        self.mapToObj()

    def mutate(self):
        for i in range(len(self.map)):
            if randrange(1,10,1)<3:
                val = self.valueCalc(self.map[i])
                self.map[i] += randrange(val[0], val[1], 1)

    def valueCalc(self, pValue):
        retVal = [0, 0]
        x = pValue - self.baseAngle
        if x <= 10:
            retVal[1] = round(0.025*(x-10)*(x-10)+0.3)

        if x >= -10:
            retVal[0] = round(-0.025*(x-10)*(x-10)-0.3)

        return retVal

    def mapToObj(self):
        newContent = []
        for i in self.map:
            pixel = []
            for c in colorsys.hsv_to_rgb(i/100, 1, 1):
                pixel.append(int(c * 255))
            newContent.append(pixel)
        self.panel.setContent(newContent)