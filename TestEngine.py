from multiprocessing import Process
from Lib.Resourcen.Manager import Manager
from Lib.Resourcen.Manager import MemoryMap
from time import sleep

class Reader:

   def __init__(self, pSeed):
       self.seed = pSeed

   def run(self):
      manager = Manager()
      manager.setSeed(self.seed)
      while(True):
         print(manager.readData("Test"))
         sleep(1)

if __name__ == '__main__':
   m = Manager()
   m.defineData("Test", 10)
   m.defineData("Test1", 10)


   r = Reader(m.getSeed())
   Process(target=r.run).start()

   sleep(5)
   m.writeData("Test", [9]*10)
