from Lib.Controller.Console import Consol
from Lib.Engine import Engine
from Lib.Effects.Fading import Fading
from Lib.Effects.FrameMaster import FrameMaster


if __name__ == '__main__':
    eng = Engine()
    eng.setControler(Consol(15))
    eng.addSubEngine(FrameMaster(6501,"192.168.2.109"), True)
    eng.run()
