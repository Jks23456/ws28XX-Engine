from tkinter import Tk, Frame
from threading import Thread
from time import sleep

class FrameViewer(Thread):

    def __init__(self, pPixellength, pPixelSize=64):
        super().__init__()
        self.pixellength = pPixellength
        self.pixelsize = pPixelSize
        self.pixel = []

    def setup(self):
        self.start()
        sleep(1)

    def setFrame(self, pFrame):
        if len(pFrame) == self.pixellength:
            for i in range(self.pixellength):
                self.pixel[i]['background'] = '#%02x%02x%02x' % tuple(pFrame[i])

    def run(self):
        self.frame = Tk()
        self.frame.wm_minsize(self.pixelsize * self.pixellength, self.pixelsize)
        self.frame.wm_maxsize(self.pixelsize * self.pixellength, self.pixelsize)
        for i in range(self.pixellength):
            tmp = Frame(self.frame, bg="#000000")
            tmp.place(x=i * self.pixelsize, y=0, width=self.pixelsize, height=self.pixelsize)
            self.pixel.append(tmp)
        self.frame.mainloop()