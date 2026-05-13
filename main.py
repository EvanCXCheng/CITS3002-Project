import sys
from config import *
from protocol import *
from devices import *

#Can link hardware straight from list in config
def framing(packet, destination, source): 
    Type = "0x0800"
    frame_head = Frame_headers(destination[1], source[1], Type)
    frame = Frame(frame_head, Packet)


def encapsulate(segment, destination, source):
    TTL = 100
    Protocol = 17
    Total_length = segment.segment_head.length + 12
    packet_head = Packet_header(destination[0], source[0], TTL, Protocol, Total_length)
    packet = Packet(packet_head, segment)
    framing(packet)

def segmentation(input_size, destination, source):
    length = input_size + 10 #Due to header size
    checksum = "I'll fix this when i learn how checksum works"
    Type = 0
    Sequence_number = 0
    Data = "A" * input_size
    segment_head = Segment_header(destination[2], source[2], length, checksum, Type, Sequence_number)
    segment = Segment(segment_head, Data)    
    print("Host A: Layer 4: Segment created by adding transport layer header (DATA, seq=0) (encapsulation)")
    print("Host A: Layer 4: Segment sent to Network Layer")
    encapsulate(segment)
    pass #?

#on input size, not input data?
def checksum(input_size):
    print("Host A: Layer 4: Checksum computed")
    return segmentation(input_size) #somewhere, somewhere, maybe not hardcode required (can pass which layer came from, decide where to send, map in config?)


input_size = int(sys.argv[1])
print("Host A: Layer 4: Data received from Application Layer. Data size= ",input_size)

new_segment = checksum(input_size)
