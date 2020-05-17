from Lib.SubEngine import SubEngine
from Lib.Compression.BlockCompression import getBlockCompression
from Lib.Objects.Snake import Snake

class Alarm(SubEngine):

    def __init__(self, pSnakeCount, pSnakeLenght):
        super().__init__("RedAlert", 1, True, getBlockCompression())
        self.snakeCount = pSnakeCount
        self.snakeLength = pSnakeLenght
        self.snakes = []

    def setup(self):
        steps = int(self.pixellength/self.snakeCount)
        for i in range(self.snakeCount):
            tmp = Snake(self.pixellength, self.snakeLength)
            tmp.double = steps*i
            self.addObj(tmp)
            self.snakes.append(tmp)

    def update(self):
        for snk in self.snakes:
            snk.move()

    def onMessage(self, topic, payload):
        if topic == "color":
            rgb = [255, 0, 0]
            if payload.startswith("#"):
                rgb = [int(payload[1:3], 16), int(payload[3:5], 16), int(payload[5:7], 16)]

            elif payload.startswith("rgb("):
                payload = payload[4:len(payload) - 1].split(",")
                for i in range(3):
                    rgb[i] = int(payload[i])

            for snk in self.snakes:
                snk.setColor(rgb)

    def getStates(self):
        retVal = []
        retVal.append(["strip/info/Alarm/enable", str(self.isEnabled)])
        retVal.append(["strip/info/Alarm/color", '#%02x%02x%02x' % tuple(self.rgb)])
        return retVal

