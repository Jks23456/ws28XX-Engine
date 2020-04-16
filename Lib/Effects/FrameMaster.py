from Lib.SubEngine import SubEngine
from Lib.Objects.Display import Display
from Lib.Objects.Loading import Loading


class FrameMaster(SubEngine):

    def __init__(self, pPort, ip = None, framebuffer=150):
        super().__init__("FrameMaster", 2)
        self.port = pPort
        self.ip = ip
        self.framebufferSize = framebuffer
        self.display = None
        self.load = None

    def setup(self):
        self.load = Loading(self.pixellength, 0, self.framebufferSize)
        self.addObj(self.load, layer=0)

        self.display = Display(self.pixellength, 0, self.port, ip=self.ip, framebuffer=self.framebufferSize)
        self.display.setStreamTimeout(5)
        self.display.startServer()
        self.addObj(self.display, layer=1)

    def terminate(self):
        self.display.stopServer()


    def update(self):
        self.display.update()
        if self.display.isBuffering:
            self.load.set(len(self.display.framebuffer))
        else:
            self.load.clear()



    def onMessage(self, topic, payload):
        if topic == "TERMINATE" and payload == "TERMINATE":
            self.display.stopServer()

    def getStates(self):
        return None