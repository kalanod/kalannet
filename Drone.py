from MeshNetwork import MeshNetwork
from Message import Message


class Drone:
    class Coordinates:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def __init__(self, drone_id, position: Coordinates, range: int, network: MeshNetwork, routing_table):
        self.drone_id = drone_id
        self.position = position
        self.range = range
        self.is_connected = False
        self.memory = []
        self.channel = 0
        self.network = network
        self.routing_table = routing_table

    def connect(self):
        self.send_message(-1, 0, self.drone_id)
        self.is_connected = True
        print(f"Drone {self.drone_id} is_connected to the network.")

    def disconnect(self):
        self.is_connected = False
        print(f"Drone {self.drone_id} disconnected from the network.")

    def send_message(self, address, code, text):
        message = Message(self.channel, self, address, Message.Message_data(code, text))
        if self.is_connected:
            #signal = self.ofdm_modulation(message)
            print(f"Drone {self.drone_id} sending message: {message}")
            self.network.new_message(message)

    def receive_message(self, message):
        print(f"Drone {self.drone_id} received message: {message}")
        if message.address == self.drone_id:
            print(f"message {message} has delivered to {self.drone_id}")
        if message.address != self.drone_id and \
                message.id not in self.memory:
            self.send_message(message)

