from Lib.Controller.StripArrangement import StripArrangement
from Lib.Effects.FrameMaster import FrameMaster
from Lib.Effects.Fading import Fading
from Lib.Engine import Engine

from Lib.Objects.Object import Object




if __name__ == '__main__':
    strip = StripArrangement()
    strip.addStrip(245, 13, 11, 1, False)
    strip.addStrip(205, 18, 10, 0, True)

    eng = Engine()
    eng.setControler(strip)
    eng.startMQTT("strip")
    eng.addSubEngine(FrameMaster(6501, ip="192.168.2.121"), True)
    #eng.addSubEngine(Fading(), False)
    eng.run()
