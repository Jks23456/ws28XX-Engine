class Panel:

    def __init__(self):
        self.transparent = [-1 ,-1 ,-1]
        self.position = 0
        self.isVisible = True 
        self.content = []

        self.kernelContent = []

        self.isMirrored = False
        self.isLooped = False
        self.isRepeated = False
        self.repeats = 0

        self.gaussMatrix = []
        self.gaussNummber = 0
        self.gaussActive = False

        self.setGaussMatrix([41,26,16,7,4,1])

    def setContent(self, pContent):
        self.kernelContent = pContent[:]
        self.processing()

    def stayMirrored(self, pBoolean):
        self.isMirrored = pBoolean
        self.processing()

    def stayRepeated(self, pBoolean, pNum):
        if pNum > 0 and pBoolean:
            self.isRepeated = True
            self.repeats = pNum
        else:
            self.isRepeated = False
            self.repeats = 0
        self.processing()

    def gauss(self, pIsActive):
        self.gaussActive = pIsActive

    def setGaussMatrix(self, pMatrix):
        self.gaussMatrix = pMatrix
        tmp = 0
        for i in self.gaussMatrix:
            tmp += i

        self.gaussNummber = tmp*2 - self.gaussMatrix[0]

    def stayLooped(self, pBoolean):
        self.isLooped = pBoolean
        self.processing()

    def shift(self, pixel=[-1,-1,-1]):
        #lastPixel = self.kernelContent[len(self.kernelContent) - 1]
        lastPixel = self.kernelContent.pop(len(self.kernelContent) - 1)
        if self.isLooped:
            self.kernelContent.insert(0, lastPixel)
        else:
            self.kernelContent.insert(0, pixel)
        self.processing()

    def insert(self, index, pixel):
        self.kernelContent.insert(index, pixel)
        self.processing()

    def replace(self, index, pixel):
        self.kernelContent[index] = pixel
        self.processing()

    def processing(self):
        newContent = self.kernelContent[:]

        # Mirror
        if self.isMirrored:
            for i in range(len(self.kernelContent) - 1, -1, -1):
                newContent.append(self.kernelContent[i])

        # Repeat
        if self.isRepeated:
            newContent = newContent * self.repeats

        #Gauss
        if self.gaussActive:
            gc = []
            for pixel in range(len(newContent)):
                chanels = [0,0,0]
                for gaussMode in range(len(self.gaussMatrix)):
                    if gaussMode == 0:
                        for color in range(3):
                            chanels[color] = newContent[pixel][color] * self.gaussMatrix[0]
                    else:
                        valH = pixel + gaussMode
                        if valH >= len(newContent):
                            valH -= len(newContent)

                        valL = pixel - gaussMode
                        if valL < 0:
                            valL += len(newContent)

                        for color in range(3):
                            chanels[color] += (newContent[valH][color] + newContent[valL][color]) * self.gaussMatrix[gaussMode]

                for color in range(3):
                    chanels[color] = int(chanels[color] / self.gaussNummber)
                gc.append(chanels)
            self.content = gc[:]
        else:
            # Push to Content
            self.content = newContent
