from Lib.Engine import Engine
from Lib.SubEngine import SubEngine
from Lib.Objects.GifViewer import GifViewer
from Lib.Controller.Console import Consol
from Lib.Effects.Alarmclock import Alarmclock

class Sub(SubEngine):

   def __init__(self):
      super().__init__("Sub", 1)
      self.obj = GifViewer("C:/Users/Jan/Desktop/TestAnimation.gif")
      self.obj.position = 10
      self.addObj(self.obj)

   def update(self):
      self.obj.nextImage()


if __name__ == '__main__':
   sub = Alarmclock()
   bo = [False, False, False, True, True, False, True]
   sub.addAlarm(19,30, pSchedual=bo, pOnce=False)
   sub.addAlarm(18,30, pOnce=True)

   eng = Engine()
   eng.setControler(Consol(20))
   eng.addSubEngine(sub, True)
   eng.run()