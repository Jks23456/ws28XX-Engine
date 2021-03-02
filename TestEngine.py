from Lib.Engine import Engine
from Lib.Controller.FrameViewer import FrameViewer
from Lib.Resourcen.TestResource import TestResource
from Lib.Effects.Elements import Elements
from Lib.Controller.FrameStreamer import FrameStreamer
from Lib.Effects.Alarm import Alarm
import struct
import wave

if __name__ == '__main__':
   eng = Engine()

   #eng.setControler(FrameViewer(100, pPixelSize=8))
   eng.setControler(FrameStreamer("192.168.2.121", 6501, 207))


   eng.addSubEngine(Elements(), True)
   eng.run()
