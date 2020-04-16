from Lib.Connection.TCPServer import TCPServer
from Lib.Objects.Object import Object

class Display(TCPServer, Object):

    def __init__(self, pPixellength,pPosition, pPort):
        self.pixellength = pPixellength
        TCPServer.__init__(pPort, self.pixellength*3,)
        Object.__init__(position=pPosition, content=[[-1,-1,-1]] * self.pixellength)

    def setup(self):
        self.startServer()

    def terminate(self):
        self.stopServer()

    def update(self):
        try:
            if len(self.buffer) != 0:
                frame = []
                pixel = []
                for bit in self.buffer:
                    if len(pixel) < 3:
                        pixel.append(int(bit))
                    else:
                        frame.append(pixel)
                        pixel = [bit]
                frame.append(pixel)
            if self.isFrame(frame):
                self.content = frame
        except Exception as e:
            print("Display: "+str(e))

    def isFrame(self, pFrame):
        if len(pFrame) != self.pixellength:
            return False

        for pixel in pFrame:
            for color in pixel:
                if color > 255 or color < -1:
                    return False
        return True