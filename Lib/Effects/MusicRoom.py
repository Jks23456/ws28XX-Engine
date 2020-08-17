from Lib.SubEngine import SubEngine
from Lib.Objects.Object import Object
import colorsys

class MusicRoom(SubEngine):

    def __init__(self, pBaseAngle):
        super().__init__("MusicRoom",1)
        self.addStartingCondition("Microphone")
        self.fftData = []
        self.baseAngle = pBaseAngle
        self.factor = 0

    def setup(self):
        self.cMap = [self.baseAngle]*self.pixellength
        self.obj = Object()
        self.addObj(self.obj)
        self.factor = self.pixellength/1024




    def update(self):
        self.fftData = self.manager.readData("MIC_FFT")
