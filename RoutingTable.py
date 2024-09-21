class RoutingTable:
    class Route:
        def __init__(self, address, length, next_hop):
            self.address = address
            self.length = length
            self.next_hop = next_hop

    def __init__(self, drone):
        self.table = {-1: [RoutingTable.Route(-1, 0, -1)],
                      drone.drone_id: [RoutingTable.Route(drone.drone_id, -1, drone.drone_id)]}

    def __str__(self):
        st = [f"\n              Routing Table \n" + " | ".join(["address", "length", "next_hop_id"])]
        for i in self.table:
            for j in self.table[i]:
                st.append(f"{j.address:<7} | {j.length:<6} | {j.next_hop}")
        return "\n".join(st)

    def add_rout(self, address, length, next_hop):
        if address not in self.table:
            self.table[address] = []
        self.table[address].append(self.Route(address, length, next_hop))
        self.squeeze()

    def has_rout(self, address):
        return address in self.table

    def get(self, address):
        if not self.has_rout(address):
            return False
        return sorted(self.table[address], key=lambda x: x.length)[0]

    def squeeze(self):
        for i in self.table:
            self.table[i] = [sorted(self.table[i], key=lambda x: x.length)[0]]

    def add_table(self, table, sender, ttl):
        for i in table:
            for j in table[i]:
                self.add_rout(i, j.length + ttl + 1, sender)
        self.squeeze()

    def clear(self, drone_id):
        self.table = {-1: [RoutingTable.Route(-1, 0, -1)],
                      drone_id: [RoutingTable.Route(drone_id, -1, drone_id)]}
