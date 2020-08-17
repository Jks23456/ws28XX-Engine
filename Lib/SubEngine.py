from Lib.Layer import Layer
from time import sleep
from Lib.Resourcen.Manager import getManager

class SubEngine:

    def __init__(self, pName, layercount, pCompressionClass=None):
        self.layList = []
        self.condition = []
        self.name = pName
        self.compClass = pCompressionClass
        self.isRunning = False
        self.pixellength = -1
        self.transparent = [-1, -1, -1]
        self.seed = ""
        self.manager = None

        for i in range(layercount):
            tmp = Layer()
            self.layList.append(tmp)


    def configur(self, pPipe, pPixellength, pSeed):
        if not self.isRunning:
            self.pipe = pPipe
            self.pixellength = pPixellength
            self.seed = pSeed

    def addStartingCondition(self, pCondition):
        if not self.isRunning:
            self.condition.append(pCondition)

    def addObj(self, obj, layer=0):
        self.layList[layer].addObj(obj)

    def delObj(self, obj):
        for layer in self.layList:
            layer.delObj(obj)

    def run(self):
        self.isRunning = True
        self.manager = getManager(False)
        self.manager.setSeed(self.seed)
        self.setup()
        while self.isRunning:
            try:
                self.controler()
            except Exception as error:
                print("SubEngine: Error in Controler")
                print(str(error))

    def sendFrame(self):
        self.update()
        if self.compClass is not None:
            self.pipe.send(self.compClass.compress(self.getFrame()))
        else:
            self.pipe.send(self.getFrame())

    def getFrame(self):
        plain = [self.transparent] * self.pixellength
        frames = []
        for i in range(len(self.layList)):
            frames.append(self.layList[i].getFrame(self.pixellength))

        for i in range(len(frames)):
            for j in range(self.pixellength):
                if plain[j] == self.transparent and frames[i][j] != self.transparent:
                    plain[j] = frames[i][j]
        return plain

    def controler(self):
        buff = []
        while self.pipe.poll():
            buff.append(self.pipe.recv())

        if len(buff)==0:
            sleep(0.001)
        else:
            for stri in buff:
                if stri == "t":
                    self.isRunning = False
                    self.terminate()
                    self.pipe.send("t")
                elif stri == "f":
                    self.sendFrame()
                elif stri.startswith("m:"):
                    mqtt = stri[2:].split("/")
                    self.onMessage(mqtt[0], mqtt[1])

    def terminate(self):
        pass

    def setup(self):
        pass

    def update(self):
        pass

    def onMessage(self, topic, payload):
        pass

    def getState(self):
        pass