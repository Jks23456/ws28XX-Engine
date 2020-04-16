from Lib.Controller.FrameStreamer import FrameStreamer
from Lib.Engine import Engine
from Lib.Effects.Fading import Fading
from Lib.Effects.Alarm import Alarm


if __name__ == '__main__':
    eng = Engine()
    eng.setControler(FrameStreamer("192.168.2.114", 6501, 450))
    eng.addSubEngine(Alarm(1), True)
    eng.run()
