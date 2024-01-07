class myClass:
    def __init__(self):
        self.__result = 0
        self.on_connect = []

    def connect(self):
        self.__result = 1
        self.fire()

    def add_listener(self, listener):
        self.on_connect.append(listener)

    def fire(self):
        for listener in self.on_connect:
            listener(self.__result)