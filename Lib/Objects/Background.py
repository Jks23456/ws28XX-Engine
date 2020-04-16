from Lib.Objects.Object import Object

class Background(Object):

    def __init__(self, pPixellength):
        self.color = [0, 0, 0]
        Object.__init__(self, position=pPixellength - 1, content=[self.color] * pPixellength)

        self.pixellength = pPixellength


    def setColor(self, color):
        self.content = [color] * self.pixellength