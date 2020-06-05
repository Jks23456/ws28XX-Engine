from Lib.Engine import Engine
from Lib.Controller.FrameViewer import FrameViewer
from Lib.Effects.FadingTrain import FadingTrain
from Lib.Effects.Alarm import Alarm

if __name__ == '__main__':
   eng = Engine()
   eng.setControler(FrameViewer(450, pPixelSize=4))
   eng.addSubEngine(Alarm(9, 20), True)
   eng.addSubEngine(FadingTrain(), True)
   eng.run()