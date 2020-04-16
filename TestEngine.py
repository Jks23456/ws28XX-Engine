from Lib.Controller.FrameStreamer import FrameStreamer
from Lib.Engine import Engine
from Lib.Effects.Fading import Fading
from Lib.Effects.FrameMaster import FrameMaster


if __name__ == '__main__':
    strip = FrameStreamer("192.168.2.114", 6501, 450)
    eng = Engine()
    eng.setControler(strip)
    eng.addSubEngine(FrameMaster(6501, "192.168.2.109"), True)
    eng.addSubEngine(Fading(), True)
    eng.run()
