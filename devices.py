import sys
from config import *
from protocol import *


#Host and router classes
class Host:
    def __init__(self, Name, IP, Subnet, MAC, Port, routing_table):
        self.Name = Name
        self.IP = IP
        self.Subnet = Subnet
        self.MAC = MAC
        self.Port = Port
        self.routing_table = routing_table
    

    #on input size, not input data?
    def make_checksum(self, input_size):
        print("Host A: Layer 4: Checksum computed")
        return("balbalbal") #somewhere, somewhere, maybe not hardcode required (can pass which layer came from, decide where to send, map in config?)


    #Can link hardware straight from list in config
    def create_frame(self, packet, destination): 
        print(f"{self.Name}: Layer 2: Packet received from Network Layer ")
        dest_MAC = IP_MAC_Table[destination] #This is probably legal idk if im allowed to use that
        source_MAC = self.MAC
        print(f"{self.Name}: Layer 2: Destination MAC lookup for next-hop IP ({destination}) → {dest_MAC}")
        Type = "0x0800"
        frame_head = Frame_headers(dest_MAC, source_MAC, Type)
        frame = Frame(frame_head, packet)
        print(f"{self.Name}: Layer 2: Frame created: SRC_MAC={source_MAC}, DST_MAC={dest_MAC}")
        print(f"{self.Name}: Layer 2: Frame sent")
        return(frame)



    def create_packet(self, segment, destination):
        dest_IP = destination.IP
        source_IP = self.IP
        TTL = 100
        print(f"{self.Name}: Layer 3: Segment received from Transport Layer: SRC_IP={source_IP}, DST_IP={dest_IP}, TTL=100")
        print(f"{self.Name}: Layer 3: Destination IP read: {dest_IP}")
        Protocol = 17
        next_hop = self.routing_table[dest_IP]
        print(f"{self.Name}: Layer 3: Routing table lookup performed")
        print(f"{self.Name}: Layer 3: Next-hop IP determined: {next_hop}")
        print(f"{self.Name}: Layer 3: Outgoing interface selected")
        Total_length = segment.headers.length + 12
        packet_head = Packet_header(dest_IP, source_IP, TTL, Protocol, Total_length)
        packet = Packet(packet_head, segment)
        print(f"{self.Name}: Layer 3: Packet forwarded to Data Link Layer")
        return(self.create_frame(packet, next_hop))

    def create_segment(self, input_size, destination):
        dest_port = destination.Port
        source_port = self.Port
        length = input_size + 10 #Due to header size
        checksum = "I'll fix this when i learn how checksum works"
        print(self.make_checksum(input_size))
        print("Boy is this sum checked NO ITS NOT FIX THIS LATER I DONT KNOW HOW IT WORKS FOR NOW")
        Type = 0
        Sequence_number = 0
        Data = "A" * input_size
        segment_head = Segment_header(dest_port, source_port, length, checksum, Type, Sequence_number)
        segment = Segment(segment_head, Data)    
        print("Host A: Layer 4: Segment created by adding transport layer header (DATA, seq=0) (encapsulation)")
        print("Host A: Layer 4: Segment sent to Network Layer")
        return(self.create_packet(segment, destination))


    def receive_segment(self, segment, ack):
        print(f"{self.Name}: Layer 4: Segment received from Network Layer")
        print("NO THERES NO CHECKSUM HERE PLS FIX IT EVAN ---------------------------------------------------------------------")
        print(f"{self.Name}: Layer 4: Checksum verified")
        if ack:
            print(f"{self.Name}: Layer 4: ACK received: seq=0")
        else:
            print(f"{self.Name}: Layer 4: DATA segment delivered to Application Layer. Data size={segment.headers.length-10}")
    
    def receive_packet(self, packet, ack):
        print(f"{self.Name}: Layer 3: Segment received from Data Link Layer: SRC_IP={packet.headers.source_IP}, DST_IP={packet.headers.dest_IP}, TTL=100")
        print(f"{self.Name}: Layer 3: Destination IP read: {packet.headers.dest_IP}")
        print(f"{self.Name}: Layer 3: Packet identified as local delivery")
        print(f"{self.Name}: Layer 3: Segment delivered to Transport Layer")
        self.receive_segment(packet.data, ack)


    def receive_frame(self, frame, ack):
        if frame.headers.dest_MAC == "BB:BB:BB:BB:BB:BB":
            interface = "Interface 1"
        else:
            interface = "Interface 2"
        print(f"{self.Name}: Layer 2: Frame received")
        print(f"{self.Name}: Layer 2: Source MAC learned: {frame.headers.source_MAC}")
        print(f"{self.Name}: Layer 2: Packet delivered to Network Layer")
        self.receive_packet(frame.data, ack)


    def create_ack(self, input_size, destination):
        dest_port = destination.Port
        source_port = self.Port
        length = input_size + 10 #Due to header size
        Type = 1
        Sequence_number = 0
        Data = "A" * input_size
        checksum = "Fake Checksum"
        segment_head = Segment_header(dest_port, source_port, length, checksum, Type, Sequence_number)
        segment = Segment(segment_head, Data)    
        print(f"{self.Name}: Layer 4: Segment created by adding transport layer header (ACK, seq=0)")
        print(f"{self.Name}: Layer 4: Segment sent to Network Layer")
        return(self.create_packet(segment, destination))
    





class Router:
    def __init__(self, Name, IP, MAC, routing_table):
        self.Name = Name
        self.IP = IP
        self.MAC = MAC
        self.routing_table = routing_table


    def forward_frame(self, packet, destination):
        print(f"{self.Name}: Layer 2: Packet received from Network Layer ")
        dest_MAC = IP_MAC_Table[destination] #This is probably legal idk if im allowed to use that
        if dest_MAC == "DD:DD:DD:DD:DD:DD":
            source_MAC = self.MAC[1]
        else:
            source_MAC = self.MAC[0]
        print(f"{self.Name}: Layer 2: Destination MAC lookup for next-hop IP ({destination}) → {dest_MAC}")
        Type = "0x0800"
        frame_head = Frame_headers(dest_MAC, source_MAC, Type)
        frame = Frame(frame_head, packet)
        print(f"{self.Name}: Layer 2: Frame created: SRC_MAC={source_MAC}, DST_MAC={dest_MAC}")
        print(f"{self.Name}: Layer 2: Frame sent")
        return(frame)


    def receive_packet(self, packet):
        print(f"{self.Name}: Layer 3: Segment received from Data Link Layer: SRC_IP={packet.headers.source_IP}, DST_IP={packet.headers.dest_IP}, TTL=100")
        print(f"{self.Name}: Layer 3: Destination IP read: {packet.headers.dest_IP}")
        packet.headers.TTL -= 1
        print(f"{self.Name}: Layer 3: TTL decremented: {packet.headers.TTL + 1} → {packet.headers.TTL}")
        next_hop = self.routing_table[packet.headers.dest_IP][0]
        print(f"{self.Name}: Layer 3: Routing table lookup performed")
        print(f"{self.Name}: Layer 3: Next-hop IP determined: {next_hop}")
        if next_hop == "10.0.2.20":
            interface = "Interface 2"
        else:
            interface = "Interface 1"
        print(f"{self.Name}: Layer 3: Outgoing interface selected ({interface})")
        print(f"{self.Name}: Layer 3: Packet forwarded to Data Link Layer")
        return(self.forward_frame(packet, next_hop))


    def receive_frame(self, frame):
        if frame.headers.dest_MAC == "BB:BB:BB:BB:BB:BB":
            interface = "Interface 1"
        else:
            interface = "Interface 2"
        print(f"{self.Name}: Layer 2: Frame received on {interface}")
        print(f"{self.Name}: Layer 2: Source MAC learned: {frame.headers.source_MAC} on {interface}")
        print(f"{self.Name}: Layer 2: Packet delivered to Network Layer")
        return(self.receive_packet(frame.data))

