from multiprocessing import Process
from multiprocessing.shared_memory import SharedMemory
from Lib.Connection.TCPServer import TCPServer
import random


class MemoryMap:

    def __init__(self, pName, pCreate):
        self.name = pName
        if pCreate:
            print("cr:"+self.name)
            self.shm = SharedMemory(name=self.name,  create=True, size=4096)
        else:
            print("co:"+self.name)
            self.shm = SharedMemory(name=self.name)
        self.blocks=[]
        self.buffer = self.shm.buf
        self.available = 4096
        self.isActive = True

    def setSeed(self, pSeed):
        self.blocks =[]
        self.available = 4096

        spl = pSeed.split("|")
        tmp = []
        for str in spl:
            length = len(tmp)
            if length == 0:
                tmp.append(str)
            elif length <3:
                tmp.append(int(str))
            else:
                self.blocks.append(tmp)
                tmp = [str]

    def close(self):
        self.shm.close()
        self.isActive = False

    def unlink(self):
        self.shm.unlink()
        self.isActive = False

    def addSpace(self, pName, pSize):
        if pSize <= self.available and self.isActive:
            if len(self.blocks)==0:
                self.blocks.append([pName, 1, pSize])
                self.available = self.available - pSize
            else:
                blk = self.blocks[len(self.blocks)-1]
                self.blocks.append([pName, blk[2]+1, blk[2]+pSize])
                self.available = self.available - pSize
                self.writeData(pName, [0]*pSize)
            return True
        return False

    def isIn(self, pName):
        for blk in self.blocks:
            if pName == blk[0]:
                return True
        return False

    def readData(self, pName):
        retData = None
        for blk in self.blocks:
            if blk[0] == pName:
                retData = bytes(self.shm.buf[blk[1] - 1:blk[2]])
        return retData

    def writeData(self, pName, pData):
        if self.isActive:
            blk = None
            for tmp in self.blocks:
                if tmp[0] == pName:
                    blk = tmp

            if blk == None:
                return False

            for i in range((blk[2] + 1) - blk[1]):
                if i >= len(pData):
                    break
                self.shm.buf[blk[1] + i - 1] = pData[i]
            return True
        return False

    def getSeed(self):
        retStri = self.name
        for blk in self.blocks:
            retStri = retStri + "|" + blk[0] + "|" + str(blk[1]) + "|" + str(blk[2])
        return retStri


class ResourcenServer(TCPServer):

    def __init__(self, pManager, pName, pSize, pPort, pIp=None, pHostname=None):
        TCPServer.__init__(self, pPort, pSize, ip=pIp, hostname=pHostname, onMessageMethod=self.onMessage)
        self.manager = pManager
        self.blockName = pName

    def onMessage(self, pInput):
        self.manager.writeData(self.blockName, pInput)

class Manager:

    def __init__(self, pCreate):
        self.maps = []
        self.create = pCreate
        self.names = []
        self.nameLength = 6
        self.sockets = []

    def setSeed(self, pSeed):
        mps = pSeed.split(";")
        for m in mps:
            spl = m.split("|")
            newMap = MemoryMap(spl.pop(0), False)
            seed = ""
            for str in spl:
                seed = seed + str + "|"
            newMap.setSeed(seed)
            self.maps.append(newMap)

    def getSeed(self):
        retString = ""
        for m in self.maps:
            retString = retString + m.getSeed() + ";"
        return retString[0:len(retString)-1]

    def defineTCPInput(self, pName, pSize, pIp=None, pPort=0, pIpWhiteList = []):
        if self.create:
            self.defineData(pName, pSize)
            newSocket = ResourcenServer(self, pName, pSize, pPort, pIp=pIp)
            for wIp in pIpWhiteList:
                newSocket.addWhitlistedIp(wIp)
            newSocket.startServer()
            self.sockets.append(newSocket)

    def defineData(self, pName, pSize):
        if self.create:
            isAdded = False
            for m in self.maps:
                if m.addSpace(pName, pSize):
                    isAdded = True
                    break
            if not isAdded:
                name = self.newName()
                self.names.append(name)
                m = MemoryMap(self.newName(), True)
                m.addSpace(pName, pSize)
                self.maps.append(m)

    def readData(self, pName):
        for m in self.maps:
            data = m.readData(pName)
            if data != None:
                return data

    def writeData(self, pName, pData):
        for m in self.maps:
            if m.writeData(pName, pData):
                return True
        return False

    def newName(self):
        retString = ""
        while(retString in self.names or retString == ""):
            retString = ''.join(random.choice(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]) for i in range(self.nameLength))
        return retString

    def terminate(self):
        if self.create:
            for sck in self.sockets:
                sck.stopServer()

            for map in self.maps:
                map.close()
                map.unlink()
        else:
            for map in self.maps:
                map.close()


mainObj = None
def getManager(pCreate=False):
    global mainObj
    if mainObj == None:
        mainObj = Manager(pCreate)
    return mainObj