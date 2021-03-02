from Lib.Effects.FrameMaster import FrameMaster
from Lib.Effects.Fading import Fading
from Lib.Engine import Engine
from Lib.Controller.StripArrangement import StripArrangement
from Lib.Objects.Object import Object


if __name__ == '__main__':
    eng = Engine()
    strip = StripArrangement()
    strip.addStrip(207, 18, 10, 0, False)

    eng.setControler(strip)
    #eng.startMQTT("strip")
    eng.addSubEngine(FrameMaster(6501, ip="192.168.2.121", framebuffer=30), True)
    #eng.addSubEngine(Fading(), True)
    eng.run()
