class RoutingTable:
    class Route:
        def __init__(self, address, length, next_hop):
            self.address = address
            self.length = length
            self.next_hop = next_hop

    def __init__(self):
        self.table = []

    def add_rout(self, address, length, next_hop):
        self.table.append(self.Route(address, length, next_hop))
