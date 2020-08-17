from Lib.Engine import Engine
from Lib.Controller.FrameViewer import FrameViewer
from Lib.Resourcen.TestResource import TestResource
from Lib.Effects.Elements import Elements
from Lib.Effects.Alarm import Alarm
import struct
import wave

if __name__ == '__main__':
   eng = Engine()
   eng.setControler(FrameViewer(100, pPixelSize=8))
   #eng.addResource(TestResource())
   #eng.addSubEngine(Alarm(9,5), True)
   eng.addSubEngine(Elements(), True)
   eng.run()


   #file = wave.open("C:/Users/Jan/Downloads/Test.wav","rb")
   #data = file.readframes(-1)
   #nData = []
   #for i in range(int(len(data)/4)):
     # nData.append(int(((data[i]<<8 or data[i+1])/65534)*255)) #excluding chanel and merge 2 bytes in to int
