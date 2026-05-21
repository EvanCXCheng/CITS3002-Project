import sys
from config import *
from protocol import *

#Host class with implementation logic
class Host:
    def __init__(self, Name, IP, Subnet, MAC, Port, routing_table):
        self.Name = Name
        self.IP = IP
        self.Subnet = Subnet
        self.MAC = MAC
        self.Port = Port
        self.routing_table = routing_table
    
    def make_checksum(self, headers, data):
        input_size = headers.length
        header_bytes = headers.get_as_bytes()
        data = header_bytes + data
        #Buffer
        if input_size % 2 != 0:
            data = data + b'\x00'
        checksum = 0 
        for i in range(0, input_size, 2):
            word = int.from_bytes(data[i:i+2], byteorder='big')
            checksum += word 
            #Wraparound, checksum has 17 bits
            if checksum > 0xFFFF:
                checksum = (checksum & 0xFFFF) + 0x0001
        checksum = ~checksum & 0xFFFF
        return checksum

    #Host receives data from Network Layer in Data Link Layer, bundle packet into frame
    def create_frame(self, packet, destination): 
        print(f"{self.Name}: Layer 2: Packet received from Network Layer ")
        dest_MAC = IP_MAC_Table[destination] 
        source_MAC = self.MAC
        print(f"{self.Name}: Layer 2: Destination MAC lookup for next-hop IP ({destination}) → {dest_MAC}")
        Type = "0x0800"
        frame_head = Frame_headers(dest_MAC, source_MAC, Type)
        frame = Frame(frame_head, packet)
        print(f"{self.Name}: Layer 2: Frame created: SRC_MAC={source_MAC}, DST_MAC={dest_MAC}")
        print(f"{self.Name}: Layer 2: Frame sent \n")
        #Send frame to router (logic handled in main.py)
        return(frame)

    #Host receives data from Transport Layer in Network Layer, bundle segment into packet
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
        print(f"{self.Name}: Layer 3: Packet forwarded to Data Link Layer \n")
        #Send to data link layer
        return(self.create_frame(packet, next_hop))

    #Data received from application layer, Host bundles data into segment
    def create_segment(self, input_size, destination, data, rdt):
        dest_port = destination.Port
        source_port = self.Port
        length = input_size + 10 #Due to header size
        Type = 0
        Sequence_number = rdt
        segment_head = Segment_header(dest_port, source_port, length, 0, Type, Sequence_number)
        checksum = self.make_checksum(segment_head, data)
        print(f"{self.Name}: Layer 4: Checksum computed")
        segment_head.checksum = checksum
        segment = Segment(segment_head, data)    
        print(f"Host A: Layer 4: Segment created by adding transport layer header (DATA, seq={rdt}) (encapsulation)")
        print("Host A: Layer 4: Segment sent to Network Layer \n")
        #Send to network layer
        return(self.create_packet(segment, destination))

    #Host receives segment from Network Layer
    def receive_segment(self, segment, expected_rdt):
        print(f"{self.Name}: Layer 4: Segment received from Network Layer")
        #Verify the data is correct
        checksum = self.make_checksum(segment.headers, segment.data)
        if checksum != segment.headers.checksum:
            print(checksum, segment.headers.checksum)
            print(f"{self.Name}: Layer 4: Checksum verification failed")
            print(f"{self.Name}: Layer 4: Segment discarded due to checksum error")
            return("Bad Checksum")
        print(f"{self.Name}: Layer 4: Checksum verified")
        #Rdt 2.2
        if segment.headers.Sequence_Number == expected_rdt:
            if segment.headers.Type == 1:
                print(f"{self.Name}: Layer 4: ACK received: seq={segment.headers.Sequence_Number} \n")
            else:
                print(f"{self.Name}: Layer 4: DATA segment delivered to Application Layer. Data size={segment.headers.length-10}")
        else:
            if segment.headers.Type == 0:
                #This happens when its NOT an ack msg. This means that the receiver should send an ACK with the old sequence number
                return("Old Ack")
            else:
                #This happens when it IS an ack msg. This means that the sender should resend the data it just sent.
                return("Old Seg")
    
    #Host receives packet from Data Link Layer, unbundle segment
    def receive_packet(self, packet, expected_rdt):
        print(f"{self.Name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet.headers.source_IP}, DST_IP={packet.headers.dest_IP}, TTL={packet.headers.TTL}")
        print(f"{self.Name}: Layer 3: Destination IP read: {packet.headers.dest_IP}")
        print(f"{self.Name}: Layer 3: Packet identified as local delivery")
        print(f"{self.Name}: Layer 3: Segment delivered to Transport Layer \n")
        #Send segment to Transport Layer
        return (self.receive_segment(packet.data, expected_rdt))

    #Host receives a frame from the router, unbundle the Network Layer packet
    def receive_frame(self, frame, expected_rdt):
        if frame.headers.dest_MAC == "BB:BB:BB:BB:BB:BB":
            interface = "Interface 1"
        else:
            interface = "Interface 2"
        print(f"{self.Name}: Layer 2: Frame received")
        print(f"{self.Name}: Layer 2: Source MAC learned: {frame.headers.source_MAC}")
        print(f"{self.Name}: Layer 2: Packet delivered to Network Layer \n")
        #Send packet to Network Layer
        return(self.receive_packet(frame.data, expected_rdt))

    #Similar to create segment, set type to 1 for ACK message
    def create_ack(self, input_size, destination, rdt):
        dest_port = destination.Port
        source_port = self.Port
        length = 10 #Due to header size
        Type = 1
        Sequence_number = 0
        segment_head = Segment_header(dest_port, source_port, length, 0, Type, Sequence_number)
        segment_head.Sequence_Number = rdt
        checksum = self.make_checksum(segment_head, b'')
        segment_head.checksum = checksum
        segment = Segment(segment_head, b'')    
        print(f"{self.Name}: Layer 4: Segment created by adding transport layer header (ACK, seq={rdt})")
        print(f"{self.Name}: Layer 4: Segment sent to Network Layer \n")
        return(self.create_packet(segment, destination))
    
#Router class with implementation logic
class Router:
    def __init__(self, Name, IP, MAC, routing_table):
        self.Name = Name
        self.IP = IP
        self.MAC = MAC
        self.routing_table = routing_table

    #Router receives packet from Network Layer, bundles into frame, sends to Host on Data Link Layer
    def forward_frame(self, packet, destination):
        print(f"{self.Name}: Layer 2: Packet received from Network Layer ")
        dest_MAC = IP_MAC_Table[destination]
        if dest_MAC == "DD:DD:DD:DD:DD:DD":
            source_MAC = self.MAC[1]
            interface = "Interface 2"
        else:
            source_MAC = self.MAC[0]
            interface = "Interface 1"
        print(f"{self.Name}: Layer 2: Destination MAC lookup for next-hop IP ({destination}) → {dest_MAC}")
        Type = "0x0800"
        frame_head = Frame_headers(dest_MAC, source_MAC, Type)
        frame = Frame(frame_head, packet)
        print(f"{self.Name}: Layer 2: Frame created: SRC_MAC={source_MAC}, DST_MAC={dest_MAC}")
        print(f"{self.Name}: Layer 2: Frame forwarded on {interface} \n")
        return(frame)

    #Router receives packet from Data Link Layer, makes routing decision
    def receive_packet(self, packet):
        print(f"{self.Name}: Layer 3: Packet received from Data Link Layer: SRC_IP={packet.headers.source_IP}, DST_IP={packet.headers.dest_IP}, TTL={packet.headers.TTL}")
        print(f"{self.Name}: Layer 3: Destination IP read: {packet.headers.dest_IP}")
        packet.headers.TTL -= 1
        if packet.headers.TTL <= 0:
            print(f"{self.Name}: Layer 3: TTL expired. Packet dropped.")
            return
        print(f"{self.Name}: Layer 3: TTL decremented: {packet.headers.TTL + 1} → {packet.headers.TTL}")
        next_hop = self.routing_table[packet.headers.dest_IP][0]
        print(f"{self.Name}: Layer 3: Routing table lookup performed")
        print(f"{self.Name}: Layer 3: Next-hop IP determined: {next_hop}")
        if next_hop == "10.0.2.20":
            interface = "Interface 2"
        else:
            interface = "Interface 1"
        print(f"{self.Name}: Layer 3: Outgoing interface selected ({interface})")
        print(f"{self.Name}: Layer 3: Packet forwarded to Data Link Layer \n")
        return(self.forward_frame(packet, next_hop))

    #Router receives frame from Data Link Layer, send to Network Layer
    def receive_frame(self, frame):
        if frame.headers.dest_MAC == "BB:BB:BB:BB:BB:BB":
            interface = "Interface 1"
        else:
            interface = "Interface 2"
        print(f"{self.Name}: Layer 2: Frame received on {interface}")
        print(f"{self.Name}: Layer 2: Source MAC learned: {frame.headers.source_MAC} on {interface}")
        print(f"{self.Name}: Layer 2: Packet delivered to Network Layer \n")
        return(self.receive_packet(frame.data))

