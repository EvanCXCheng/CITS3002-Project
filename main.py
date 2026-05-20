import sys
import os
from config import *
from protocol import *
from devices import *

HostA = Host("Host A", Host_A[0], Network_1, Host_A[1], Host_A[2], Host_A_Routing_Table)
HostB = Host("Host B", Host_B[0], Network_2, Host_B[1], Host_B[2], Host_B_Routing_Table)
Router1 = Router("Router R1", [Router_interface_1[0], Router_interface_2[0]], [Router_interface_1[1], Router_interface_2[1]], Router_Routing_Table)

input_size = int(sys.argv[1])
data = os.urandom(input_size) #Bytes
print("Host A: Layer 4: Data received from Application Layer. Data size= ",input_size)
rdt = 0
i = 0
while i < input_size:
    segment = HostA.create_segment(min(MAX_SIZE, input_size - i), HostB, data[i:i+MAX_SIZE], rdt)
    frame = Router1.receive_frame(segment)
    error_check = HostB.receive_frame(frame, rdt)

    if error_check == "Old Ack":
        #This means that the error happened at the receiver and that it should then send an ACK with an old sequence number
        ack = HostB.create_ack(input_size, HostA, 1 - rdt)
        ack = Router1.receive_frame(ack)
        seq_check = HostA.receive_frame(ack, rdt)
        
    else:
        #Otherwise send a normal ack
        ack = HostB.create_ack(input_size, HostA, rdt)
        ack = Router1.receive_frame(ack)
        seq_check = HostA.receive_frame(ack, rdt)

    if error_check == "Old Seg":
        #If a normal ACK was sent this wont trigger. 
        #If an old ACK is sent, resend the current one
        print("Host A: Layer 4: Old ACK received. Resending current segment.")
        continue

    rdt = 1 - rdt
    i+=MAX_SIZE