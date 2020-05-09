from Lib.Engine import Engine
from Lib.Controller.Console import Consol
from Lib.Effects.Alarmclock import Alarmclock

if __name__ == '__main__':
   sub = Alarmclock()


   eng = Engine()
   eng.setControler(Consol(20))
   eng.addSubEngine(sub, True)
   eng.run()