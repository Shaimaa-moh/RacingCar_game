import socket
import pickle
# this class is responsible for connecting to our server


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "13.51.86.153"
        self.port = 3000
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)

            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print("Conection error: ", e)
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
