from Lib.SubEngine import SubEngine
from Lib.Compression.BlockCompression import getBlockCompression

class Pixel:

    def __init__(self, pColor):
        pass

class PixelCrash(SubEngine):

    def __init__(self):
        super().__init__("PixelCrash", 2, getBlockCompression())

    def update(self):
        pass