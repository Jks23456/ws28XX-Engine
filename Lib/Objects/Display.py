from Lib.Connection.TCPServer import TCPServer
from Lib.Objects.Object import Object

class Display(TCPServer, Object):

    def __init__(self, pPixellength,pPosition, pPort, ip=None):
        self.pixellength = pPixellength
        TCPServer.__init__(self, pPort, self.pixellength*3, ip=ip)
        Object.__init__(self, position=pPosition, content=[[-1,-1,-1]] * self.pixellength)

    def update(self):
        try:
            frame = []
            if len(self.buffer) != 0:
                fr = self.buffer.pop(0)
                pixel = []
                for bit in fr:
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
            if len(pixel)!=3:
                return False
            for color in pixel:
                if color > 255 or color < -1:
                    return False
        return True