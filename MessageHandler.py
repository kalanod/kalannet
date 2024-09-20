from Drone import Drone
from Message import Message


def init_message(drone, message):
    drone.send_message(message.sender.drone_id, )


def handleMessage(message: Message, drone: Drone):
    if message.data.code == 0 and message.data.text != drone.drone_id:
        # init_message
        drone.routing_table.add_rout(message.data.text, message.ttl, message.data.reverse_channel, message.sender.drone_id)
        drone.send_message(message.data.text, 1, drone.routing_table, )
    #print(drone.drone_id, message.data.text)