from Lib.Objects.Object import Object
from PIL import Image

class GifViewer(Object):

    def __init__(self, pPath):
        super().__init__()
        self.frames = []
        self.path = pPath
        self.index = 0
        self.load()

    def load(self):
        image = Image.open(self.path)
        for fCount in range(image.n_frames):
            image.seek(fCount)
            rgb = image.convert('RGB')
            tmp = []
            for pixel in range(image.size[0]):
                tmp.append(rgb.getpixel((pixel, 0)))
            self.frames.append(tmp)
        self.setImage(self.index)

    def setImage(self, pInt):
        self.index = pInt
        self.content = self.frames[pInt]

    def nextImage(self):
        self.index = self.index + 1
        if self.index >= len(self.frames):
            self.index = 0
        self.content = self.frames[self.index]