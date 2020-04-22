



from multiprocessing import Process
from Lib.Resourcen.Manager import getManager
from Lib.Resourcen.Manager import MemoryMap
from time import sleep

class Reader:

   def __init__(self, pSeed):
       self.seed = pSeed

   def run(self):
      manager = getManager()
      manager.setSeed(self.seed)
      while(True):
         print(manager.readData("Test562"))
         sleep(1)

if __name__ == '__main__':
