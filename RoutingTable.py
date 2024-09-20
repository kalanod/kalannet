class RoutingTable:
    class Route:
        def __init__(self, address, length, next_hop_channel, next_hop_id):
            self.address = address
            self.length = length
            self.next_hop_channel = next_hop_channel
            self.next_hop_id = next_hop_id

    def __init__(self):
        self.table = {-1: [RoutingTable.Route(-1, 1, -1, -1)]}

    def __str__(self):
        st = [f"\n              Routing Table \n" + " | ".join(["address", "length", "next_hop_channel", "next_hop_id"])]
        for i in self.table:
            for j in self.table[i]:
                st.append(f"{j.address:<7} | {j.length:<6} | {j.next_hop_channel:<16} | {j.next_hop_id}")
        return "\n".join(st)
    def add_rout(self, address, length, next_hop_channel, next_hop_id):
        if address not in self.table:
            self.table[address] = []
        self.table[address].append(self.Route(address, length, next_hop_channel, next_hop_id))

    def has_rout(self, address):
        return address in self.table

    def get(self, address):
        if not self.has_rout(address):
            return False
        return sorted(self.table[address], key=lambda x: x.length)[0]
