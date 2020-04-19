from multiprocessing import Process
from Lib.Resourcen.Manager import Manager
from Lib.Resourcen.Manager import MemoryMap
from time import sleep

if __name__ == '__main__':
   m = Manager()
   m.defineData("Test", 4000)
   m.defineData("Test1", 100)

   m2 = Manager()
   m2.setSeed(m.getSeed())

   m.writeData("Test", [5]*4000)
   print(m2.readData("Test"))