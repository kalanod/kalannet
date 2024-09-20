import random


class Message:
    class Message_data:
        def __init__(self, code, text, reverse_channel):
            self.code = code
            self.text = text
            self.reverse_channel = reverse_channel

    def __init__(self, channel, sender, address, message_data):
        self.id = str(sender.drone_id) + str(random.randint(0, 99999999))
        self.channel = channel
        self.sender = sender
        self.address = address
        self.data = message_data
        self.range = sender.range
        self.ttl = 0
