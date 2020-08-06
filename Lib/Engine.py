import time
import multiprocessing
from Lib.Resourcen.Manager import getManager


class ProcessWrap:

    def __init__(self, pObj, pIsEnabled):
        self.name = pObj.name
        self.object = pObj
        self.process = None
        self.pipe = None
        self.isAcknowledged = True
        self.isEnabled = pIsEnabled
        self.compClass = pObj.compClass

    def isActive(self):
        return self.pipe != None and self.process != None

    def reset(self):
        if self.isActive():
            self.pipe.close()
            self.pipe = None
            self.process = None
        self.isAcknowledged = True
        self.isEnabled = False

class Engine:

    def __init__(self):
        self.isRunning = False
        self.brightness = 100
        self.processes = []
        self.resourcen = []
        self.frames = {}
        self.controller = None
        self.pixellength = 0
        self.manager = getManager(True)

    def startMQTT(self, pAddress, pName):
        import paho.mqtt.client as mqtt
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(pAddress[0], pAddress[1], 60)
        self.client.subscribe(pName+ "/effekt/#")
        self.client.subscribe(pName+ "/command")
        self.client.subscribe(pName+ "/color/#")
        self.client.loop_start()

    def setControler(self, pControler):
        self.controller = pControler

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
            for prWrap in self.processes:
                if topic.startswith(prWrap.name+"/"):
                    topic = topic[len(prWrap.name)+1:]
                    if topic == "enable":
                        prWrap.isEnabled = str(msg.payload).lower() in("true","t","on","1")
                        print(prWrap.isEnabled)
                    elif prWrap.isActive:
                        prWrap.pipe.send("m:"+topic+"/"+msg.payload)

    def addSubEngine(self, pSub, pIsEnabled):
        if not self.isRunning:
            self.processes.append(ProcessWrap(pSub, pIsEnabled))

    def addResource(self, pResource):
        if not self.isRunning:
            self.resourcen.append(ProcessWrap(pResource, False))

    def run(self):
        try:
            self.isRunning = True
            self.controller.setup()
            self.pixellength = self.controller.pixellength

            print("Define all Resources")
            for prWrap in self.resourcen:
                print(prWrap.name)
                prWrap.object.defineData(self.manager)

            print("Start all Resources:")
            for prWrap in self.resourcen:
                print(prWrap.name)
                parent, child = multiprocessing.Pipe()
                prWrap.process = multiprocessing.Process(target=prWrap.object.run)
                prWrap.object.configur(child, self.manager.getSeed())
                prWrap.pipe = parent
                prWrap.process.start()

            while self.isRunning:
                fr = time.perf_counter()
                frames = [[-1, -1, -1]] * self.pixellength
                for prWrap in self.processes:
                    if prWrap.isEnabled and prWrap.isAcknowledged and prWrap.isActive():
                        prWrap.isAcknowledged = False
                        prWrap.pipe.send("f")
                for prWrap in self.processes:
                    if prWrap.isEnabled and not prWrap.isActive():
                        self.startSubEngine(prWrap)
                    elif not prWrap.isEnabled and prWrap.isActive():
                        self.terminateSubEngine(prWrap)
                    elif prWrap.isEnabled:
                        frame = self.frames[prWrap.name]

                        buff = []
                        while prWrap.pipe.poll():
                            buff.append(prWrap.pipe.recv())
                            prWrap.isAcknowledged = True

                        if len(buff)>0:
                            if prWrap.compClass is not None:
                                frame = prWrap.compClass.decompress(buff.pop(len(buff) - 1))
                            else:
                                frame = buff.pop(len(buff) - 1)
                            self.frames[prWrap.name] = frame
                        for i in range(min(len(frame),len(frames), self.pixellength)):
                            if frames[i] == [-1, -1, -1]:
                                frames[i] = frame[i]

                brPercent = float(self.brightness) / 100
                completeFrame = []
                for i in range(len(frames)):
                    color = []
                    for a in frames[i]:
                        color.append(int(max(0, a) * brPercent))
                    completeFrame.append(color)

                self.controller.setFrame(completeFrame)

                fr = time.perf_counter() - fr
                if fr <= 0.02:
                    time.sleep(0.02 - fr)
        except KeyboardInterrupt:
            self.terminateAll()
        except Exception as e:
            print("Error: in Engine")
            print(e)
            self.terminateAll()

    def startSubEngine(self, prWrap):
        if self.isRunning and not prWrap.isActive(): #[pSub.mqttTopic, process, parent, True]
            print("Start: " + prWrap.name)
            print("Activate Conditions:")
            for c in prWrap.object.condition:
                for r in self.resourcen:
                    if r.name == c:
                        r.pipe.send("A")
                        print(c)

            parent, child = multiprocessing.Pipe()
            prWrap.process = multiprocessing.Process(target=prWrap.object.run)
            prWrap.object.configur(child, self.pixellength, self.manager.getSeed())
            prWrap.pipe = parent
            prWrap.isEnabled = True
            self.frames[prWrap.name] = ([[-1, -1, -1]] * self.pixellength)
            prWrap.process.start()

    def terminateSubEngine(self, prWrap):
        if prWrap.isActive():
            print("Terminate: " + prWrap.name)
            prWrap.pipe.send("t")
            acn = False
            while not acn:
                if prWrap.pipe.recv() == "t":
                    acn = True
            print("Joining Process...")
            prWrap.process.join()
            print("Done!")
            prWrap.pipe.close()
            prWrap.process = None
            prWrap.pipe = None
            prWrap.isEnabled = False

            print("Deactivate Conditions:")
            for c in prWrap.object.condition:
                for r in self.resourcen:
                    if r.name == c:
                        r.pipe.send("T")
                        print(c)

    def terminateAll(self):
        self.isRunning = False
        for wrap in self.processes:
            self.terminateSubEngine(wrap)