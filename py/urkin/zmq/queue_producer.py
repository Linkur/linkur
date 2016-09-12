import zmq

class QueueProducer:

    def __init__(self):
        print("creating zmq producer")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.socket.bind("tcp://127.0.0.1:5559")

    def push(self, info):
        print("###################################")
        self.socket.send(info.tostring())
        print("###################################")

if __name__ == "__main__":
    q = QueueProducer()
    q.push(str({"x":"y"}))
