#Host and router classes
class Host:
    def __init__(self, IP, Subnet, MAC):
        self.IP = IP
        self.Subnet = Subnet
        self.MAC = MAC

class Router:
    def __init__(self, IP, Subnet):
        self.IP = IP
        self.Subnet = Subnet
        self.routing_table = {}
