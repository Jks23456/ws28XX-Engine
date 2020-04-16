

class FakePipe:

    def __init__(self):
        self.buffer = []
        self.frames = []
        self.messages = []

    def poll(self):
        return len(self.buffer) != 0

    def send(self, plain):
        self.frames.append(plain)
        print(self.frames)

    def recv(self):
        if self.poll():
            return self.messages.pop(0)
        return None

    def message(self, pMessage):
        self.messages.append(pMessage)

    def getFrame(self):
        if len(self.frames)!=0:
            return self.frames.pop(0)
        return []