import time
import paho.mqtt.client as mqtt
import multiprocessing

from Lib.Strip import StripArrangement

class Engine:

    def __init__(self):
        self.isRunning = False
        self.brightness = 100
        self.subengines = []
        self.processes = []
        self.frames = {}
        self.pixels = StripArrangement()

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.subscribe("strip/effekt/#")
        self.client.subscribe("strip/command")
        self.client.subscribe("strip/color/#")
        self.client.loop_start()

    def addStrip(self, pPixellength, pPin, pDMA, pChanel, pIsReversed):
        return self.pixels.addStrip(pPixellength, pPin, pDMA, pChanel, pIsReversed)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        print([msg.topic, msg.payload])
        if topic == "strip/command":
            if msg.payload == "update":
                pass
            elif msg.payload == "reset":
                self.pixels.blackout()
        elif topic.startswith("strip/color/"):
            topic = topic[12:]
            if topic == "brightnis":
                self.brightness = int(msg.payload)
        elif topic.startswith("strip/effekt/"):
            topic = topic[13:]
            for row in self.processes:
                if topic.startswith(row[0]+"/"):
                    topic = topic[len(row[0])+1:]
                    if topic == "enable":
                        row[3] = msg.payload.lower() in ("true", "t", "1", "on")
                    elif row[2] != None:
                        row[2].send("m:"+topic+"/"+msg.payload)

    def addSubEngine(self, pSub, pIsEnabled):
        if not self.isRunning:
            self.subengines.append(pSub)
            self.processes.append([pSub.mqttTopic, None, None, pIsEnabled, pSub.isCompressed])

    def run(self):
        self.isRunning = True
        self.pixels.create()
        self.pixels.blackout()

        while self.isRunning:
            fr = time.clock()
            frames = [[-1, -1, -1]] * 450
            for row in self.processes:
                if row[3] and row[2]==None and row[1] == None:
                    self.startSubEngine(row[0])
                elif not row[3] and row[2] != None and row[1] != None:
                    self.terminateSubEngine(row[0])
                elif row[3]:
                    frame = self.frames[row[0]]
                    if row[2].poll():
                        if row[4]:
                            frame = self.decompFrame(row[2].recv())
                        else:
                            frame = row[2].recv()
                        self.frames[row[0]] = frame
                        row[2].send("f")
                    for i in range(len(frames)):
                        if frames[i] == [-1, -1, -1]:
                            frames[i] = frame[i]

            brPercent = float(self.brightness)/100
            for i in range(len(frames)):
                color = []
                for a in frames[i]:
                    color.append(int(max(0, a)*brPercent))
                self.pixels.setPixel(i, color=color)
            self.pixels.show()
        self.terminate()

    def bitToRow(self, pBits):
        retVal = [0, [0, 0, 0]]
        retVal[0] = (pBits & 4278190080) >> 24
        if retVal[0] == 255:
            retVal[0] = pBits & 255
            retVal[1] = [-1,-1,-1]
        else:
            retVal[1][0] = (pBits & 16711680) >> 16
            retVal[1][1] = (pBits & 65280) >> 8
            retVal[1][2] = pBits & 255
        return retVal

    def decompFrame(self, pFrame):
        block = []
        for data in pFrame:
            block.append(self.bitToRow(data))
        retVal = []
        for row in block:
            retVal = retVal + [row[1]]*(row[0]+1)
        return retVal

    def startSubEngine(self, pMqttTopic):
        if self.isRunning: #[pSub.mqttTopic, process, parent, True]
            newSub = None
            for sub in self.subengines:
                if sub.mqttTopic == pMqttTopic:
                    newSub = sub
                    break
            if newSub == None:
                return
            parent, child = multiprocessing.Pipe()
            process = multiprocessing.Process(target=newSub.run)
            newSub.configur(child)
            for row in self.processes:
                if row[0] == pMqttTopic:
                    row[1] = process
                    row[2] = parent
                    row[3] = True
                    break
            process.start()
            self.frames[pMqttTopic] = ([[-1, -1, -1]]*450)

    def terminateSubEngine(self, pMqttTopic):
        for row in self.processes:
            if row[0] == pMqttTopic:
                print("Terminate: "+pMqttTopic)
                row[2].send("t")
                print("Joining Process...")
                row[1].join()
                print("Done!")
                row[2].close()
                row[1] = None
                row[2] = None
                row[3] = False

    def terminateAll(self):
        for row in self.processes:
            print("Terminate Process...")
            row[2].send("t")

        for row in self.processes:
            print("Join Process...")
            row[1].join()
            row[2].close()
            row[1] = None
            row[2] = None
        print("Done!")
