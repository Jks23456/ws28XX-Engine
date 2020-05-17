from Lib.Engine import Engine
from Lib.Controller.FrameViewer import FrameViewer
from Lib.Effects.Alarmclock import Alarmclock, Signal
from Lib.Effects.Alarm import Alarm
from Lib.Effects.Fading import Fading

if __name__ == '__main__':
   sub = Alarmclock()
   sub.addAlarm(17,47, Signal(Alarm(5, 20), 450, 5000, pSlowMotion=1))

   eng = Engine()
   eng.setControler(FrameViewer(450, pPixelSize=2))
   eng.addSubEngine(sub, True)
   eng.addSubEngine(Fading(), True)
   eng.run()