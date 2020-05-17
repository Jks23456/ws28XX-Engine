from Lib.Objects.Object import Object

class Container(Object):

    def __init__(self, pSubEngine, pPixellength=20):
        super().__init__()
        self.content = [[-1, -1, -1]] * pPixellength
        self.sub = pSubEngine
        self.sub.configur(None, pPixellength)
        self.sub.setup()

    def nextFrame(self):
        self.sub.update()
        self.content = self.sub.getFrame()

    def terminate(self):
        self.sub.terminate()