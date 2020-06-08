import colorsys;
from Lib.SubEngine import SubEngine
from Lib.Objects.Object import Object

class FadingTrain(SubEngine):

    def __init__(self):
        super().__init__("FadingTrain", 1)
        self.addStartingCondition("TestResource")
        self.display = Object()
        self.addObj(self.display)

    def setup(self):
        factor = (1/360) * (360/self.pixellength)
        for i in range(self.pixellength):
            pixel = []
            for c in colorsys.hsv_to_rgb(factor*i,1,1):
                pixel.append(int(c*255))
            self.display.content.append(pixel)

    def update(self):
        self.display.position += 3
        if self.display.position >= self.pixellength:
            self.display.position -= self.pixellength