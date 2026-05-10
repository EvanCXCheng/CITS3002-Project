import sys
from config import *
from protocol import *
from devices import *


def framing(packet):
    dest_MAC = Router_interface_1[1]
    source_MAC = Host_A[1]
    Type = "0x0800"
    frame_head = Frame_headers(dest_MAC, source_MAC, Type)
    frame = Frame(frame_head, Packet)


def encapsulate(segment):
    dest_IP = Host_B[0]
    source_IP = Host_A[0]
    TTL = 100
    Protocol = 17
    Total_length = segment.segment_head.length + 12
    packet_head = Packet_header(dest_IP, source_IP, TTL, Protocol, Total_length)
    packet = Packet(packet_head, segment)
    framing(packet)

def segmentation(input_size):
    dest_port = 80
    source_port = 5000
    length = input_size + 10 #Due to header size
    checksum = "I'll fix this when i learn how checksum works"
    Type = 0
    Sequence_number = 0
    Data = "A" * input_size
    segment_head = Segment_header(dest_port,source_port,length,checksum,Type,Sequence_number)
    segment = Segment(segment_head, Data)    
    print("Host A: Layer 4: Segment created by adding transport layer header (DATA, seq=0) (encapsulation)")
    print("Host A: Layer 4: Segment sent to Network Layer")
    encapsulate(segment)
    pass


def checksum(input_size):
    print("Host A: Layer 4: Checksum computed")
    return segmentation(input_size)


input_size = int(sys.argv[1])
print("Host A: Layer 4: Data received from Application Layer. Data size= ",input_size)

new_segment = checksum(input_size)
