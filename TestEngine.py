from Lib.Controller.FrameStreamer import FrameStreamer
from Lib.Engine import Engine
from Lib.SubEngine import SubEngine
from Lib.Objects.Loading import Loading
from Lib.Effects.FrameMaster import FrameMaster
from Lib.Effects.Fading import Fading
from Lib.Effects.Alarm import Alarm


class TestEngine(SubEngine):

    def __init__(self):
        super().__init__("TestEngine", 1)
        self.l = Loading(450, 0, 150)
        self.addObj(self.l)
        self.counter = 0
        self.bool = True

    def update(self):
        if self.bool:
            self.counter = self.counter + 1
            if self.counter >= 150:
                self.bool = False
        else:
            self.counter = self.counter -1
            if self.counter <=0:
                self.bool = True
        self.l.set(self.counter)



if __name__ == '__main__':
    eng = Engine()
    eng.setControler(FrameStreamer("192.168.2.114", 6501, 450))
    eng.addSubEngine(FrameMaster(950), True)
    eng.run()
