#Header definitions and classes for layers\
class Frame_headers:
    def __init__(self, dest_MAC, source_MAC, Type):
        self.dest_MAC = dest_MAC
        self.source_MAC = source_MAC
        self.Type = Type
    
class Packet_header:
    def __init__(self, dest_IP, source_IP, TTL, Protocol, length):
        self.dest_IP = dest_IP
        self.source_IP = source_IP
        self.TTL = TTL
        self.Protocol = Protocol
        self.Total_length = length

class Segment_header:
    def __init__(self, dest_port, source_port, length, checksum, Type, Sequence_Number):
        self.dest_port = dest_port
        self.source_port = source_port
        self.length = length
        self.checksum = checksum
        self.Type = Type
        self.Sequence_Number = Sequence_Number

class Frame: 
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data

class Packet:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data

class Segment:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data
