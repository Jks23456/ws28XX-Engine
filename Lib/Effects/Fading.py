from colorsys import hsv_to_rgb

from Lib.SubEngine import SubEngine
from Lib.Objects.Background import Background

class Fading(SubEngine):

    def __init__(self):
        SubEngine.__init__(self, "Fading", 1)
        self.background = None
        self.angle = 0.0   # in °
        self.speed = 1.0   # °/s
        self.const = 1/360 #const for 1° in %

    def setup(self):
        self.background = Background(self.pixellength)
        self.addObj(self.background)

    def update(self):
        self.angle += self.speed
        if self.angle >=360:
            self.angle -= 360
        pixel = []

        for c in hsv_to_rgb(self.angle/360, 1, 1):
            pixel.append(c * 255)
        self.background.setColor(pixel)