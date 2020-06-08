from Lib.Resourcen.Resource import Resource

class TestResource(Resource):

    def __init__(self):
        super().__init__("TestResource")
        self.count = 0

    def setup(self):
        self.manager.defineData("Test0",5)
        self.manager.defineData("Test1",50)

    def activate(self):
        print("Activated")

    def deactivate(self):
        print("Deactivated")

    def update(self):
        self.count += 1
        if self.count >= 10:
            self.count = 0
        self.manager.writeData("Test0",[self.count] * 5)
        self.manager.writeData("Test1",[self.count] * 50)