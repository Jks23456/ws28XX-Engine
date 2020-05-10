from Lib.Objects.Object import Object
from Lib.Effects.Fading import Fading


class Container(Object):

    def __init__(self, pSubEngine, pPixellength=20):
        super().__init__()
        self.sub = pSubEngine

        self.sub.configur(None, pPixellength)
        self.sub.setup()

    def newFrame(self):
        self.sub.update()
        self.content = self.sub.getFrame()

    def terminate(self):
        self.sub.terminate()