from Lib.Objects.Object import Object

class Loading(Object):
    def __init__(self, pRange, pMinInput, pMaxInput, color=[0,255,0]):
        super().__init__()
        self.min = pMinInput
        self.max = pMaxInput
        self.range = pRange
        self.color = color
        self.step = int(self.range / (self.max - self.min))

    def set(self, pInput):
        self.content =[self.color] * ((pInput - self.min) * self.step)

    def clear(self):
        self.content = []