from Lib.SubEngine import SubEngine
from Lib.Objects.Display import Display
from Lib.Objects.Loading import Loading
from Lib.Objects.Object import Object
from Lib.Effects.Fading import Fading

class FrameMaster(SubEngine):

    def __init__(self, pPort, ip = None, framebuffer=150):
        super().__init__("FrameMaster", 3)
        self.port = pPort
        self.ip = ip
        self.framebufferSize = framebuffer
        self.display = None
        self.load = None
        self.waitingObj = Object()

    def setup(self):
        self.waitingObj.content = [[100,0,0]]*self.pixellength
        self.addObj(self.waitingObj, layer=0)

        self.load = Loading(self.pixellength, 0, self.framebufferSize)
        self.addObj(self.load, layer=1)



        self.display = Display(self.pixellength, 0, self.port, ip=self.ip, framebuffer=self.framebufferSize)
        self.display.setStreamTimeout(5)
        self.display.startServer()
        self.addObj(self.display, layer=2)

    def terminate(self):
        self.display.stopServer()

    def update(self):
        if self.display.isConnected:
            self.waitingObj.isVisible = False
            self.display.update()
            if self.display.isBuffering:
                self.load.set(len(self.display.framebuffer))
            else:
                self.load.clear()
        else:
            self.waitingObj.isVisible = True
            self.display.resetBuffer()