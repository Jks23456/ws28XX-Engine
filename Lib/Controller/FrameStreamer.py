from Lib.Connection.TCPClient import TCPClient

class FrameStreamer:

    def __init__(self, pAddress, pPort, pPixellength):
        self.tcp = TCPClient(pAddress, pPort, pPixellength*3)
        self.tcp.setTimeout(1)
        self.pixellength = pPixellength
        self.buffer = []

    def setup(self):
        self.tcp.connect()

    def setFrame(self, pFrame):
        self.buffer.append(pFrame)
        if self.tcp.isConnected and len(self.buffer) == 50:
            data = []
            for frame in self.buffer:
                for pixel in frame:
                    for color in pixel:
                        data.append(color)
            self.tcp.sendData(data)
            self.buffer = []