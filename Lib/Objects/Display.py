from Lib.Connection.TCPServer import TCPServer
from Lib.Objects.Object import Object
from Lib.Objects.Loading import Loading

class Display(TCPServer, Object):

    def __init__(self, pPixellength, pPosition, pPort, ip=None, framebuffer=150):
        TCPServer.__init__(self, pPort, pPixellength * 3 * 50, ip=ip)
        Object.__init__(self, position=pPosition, content=[[-1, -1, -1]] * pPixellength)
        self.pixellength = pPixellength
        self.framebufferSize = framebuffer
        self.framebuffer = []
        self.isBuffering = True

    def update(self):
        try:
            frame = []
            if len(self.buffer) != 0:
                package = self.buffer.pop(0)
                pixel = []
                for fr in package:
                    newFrame = []
                    for bit in fr:
                        if len(pixel) < 3:
                            pixel.append(int(bit))
                        else:
                            newFrame.append(pixel)
                            pixel = [bit]
                    if len(frame) == self.pixellength:
                        frame.append(newFrame)

            if not self.isFrame(frame):
                return

        except Exception as e:
            print("Display: "+str(e))

        self.framebuffer.append(frame)
        if self.isBuffering:
            if len(self.framebuffer) > self.framebufferSize:
                self.isBuffering = False
        else:
            self.content = self.framebuffer.pop(0)
            if len(self.framebuffer)==0:
                self.isBuffering = True

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

    def resetBuffer(self):
        self.framebuffer = []
        self.isBuffering = True
        self.content = []
