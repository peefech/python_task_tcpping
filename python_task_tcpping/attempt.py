class Attempt:
    def __init__(self, host, port, count):
        self.host = host
        self.port = port
        self.count = count
        self.time = None
        self.passed = False
