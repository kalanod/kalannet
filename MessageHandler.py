from Message import Message


def init_message(drone, message):
    drone.send_message(message.sender.drone_id, )


def handleMessage(message: Message, drone):
    if message.data.code == 0 and message.data.text != drone.drone_id:
        # init_message
        drone.routing_table.add_rout(message.data.text, message.ttl, message.sender.drone_id)
        drone.send_message(message.data.text, 1, drone.drone_id)

    if message.data.code == 1:
        drone.routing_table.add_rout(message.data.text, 1, message.data.text)

    if message.data.code == 2:
        drone.routing_table.add_table(message.data.text, message.sender.drone_id, message.ttl)

    if message.data.code == 3:
        drone.received.append(message)
