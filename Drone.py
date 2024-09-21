import MessageHandler
from MeshNetwork import MeshNetwork
from Message import Message
from RoutingTable import RoutingTable


class Drone:
    class Coordinates:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def __init__(self, drone_id, position: Coordinates, range: int, network: MeshNetwork):
        self.drone_id = drone_id
        self.position = position
        self.range = range
        self.is_connected = False
        self.memory = []
        self.channel = 0
        self.network = network
        self.routing_table: RoutingTable = RoutingTable(self)

    def connect(self):
        self.is_connected = True
        self.send_message(-1, 0, self.drone_id)
        print(f"Drone {self.drone_id} is_connected to the network.")

    def disconnect(self):
        self.is_connected = False
        print(f"Drone {self.drone_id} disconnected from the network.")

    def send_message(self, address, code, text):
        message = Message(self.channel, self, address, Message.Message_data(code, text))
        if message.data.code != 0 and message.data.code != 1:
            print(f"Drone {self.drone_id} sending message: {message.data.text}")
        self.memory.append(message.id)
        self.network.new_message(message)


    def send_message2(self, message):
        if message.data.code != 0 and message.data.code != 1:
            print(f"Drone {self.drone_id} sending message: {message.data.text}")
        self.memory.append(message.id)
        self.network.new_message(message)


    def receive_message(self, message: Message):
        if not self.is_connected:
            return
        if message.data.code != 0 and message.data.code != 1:
            print(f"Drone {self.drone_id} received message: {message.data.text}")
        if message.address == self.drone_id or message.address == -1:
            MessageHandler.handleMessage(message, self)
            if message.data.code != 0 and message.data.code != 1:
                print(f"message {message.data.text} has delivered to {self.drone_id}")
        if (self.routing_table.has_rout(message.address) or message.address == -1) and \
                message.address != self.drone_id and message.id not in self.memory:
            message.channel = self.channel
            message.sender = self
            message.ttl += 1
            self.send_message2(message)
