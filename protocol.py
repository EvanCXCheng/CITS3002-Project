#Header definitions and classes for each layer
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

    #Convert Header to bytes to make Checksum calculation easier
    def get_as_bytes(self):
        #0 the checksum
        return (self.dest_port.to_bytes(2, byteorder='big') + self.source_port.to_bytes(2, byteorder='big') + self.length.to_bytes(2, byteorder='big') 
                + b'\x00\x00' + self.Type.to_bytes(1, byteorder='big') + self.Sequence_Number.to_bytes(1, byteorder='big'))

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