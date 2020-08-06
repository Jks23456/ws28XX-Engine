from time import sleep
from Lib.Resourcen.Manager import getManager

class Resource:

    def __init__(self, pName, pCompressionClass=None):
        self.name = pName
        self.compClass = pCompressionClass
        self.manager = None
        self.pipe = None
        self.isRunning = False
        self.isActive = False
        self.seed = ""

    def defineData(self, pManager):
        self.manager = pManager
        self.setup()
        self.manager = None

    def configur(self, pPipe, pSeed):
        self.pipe = pPipe
        self.seed = pSeed

    def run(self):
        self.isRunning = True
        self.manager = getManager(False)
        self.manager.setSeed(self.seed)
        while self.isRunning:
            buff = []
            while self.pipe.poll():
                buff.append(self.pipe.recv())

            if len(buff) == 0 and self.isActive:
                self.update()
            elif len(buff) == 0:
                sleep(0.001)

            for i in buff:
                if i == "T" and self.isActive:
                    self.deactivate()
                elif i == "A" and not self.isActive:
                    self.isActive = True
                    self.activate()

    #---Overwrite---

    def setup(self):
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass

    def update(self):
        pass