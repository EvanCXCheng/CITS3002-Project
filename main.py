import sys
from config import *
from protocol import *
from devices import *



HostA = Host("Host A", Host_A[0], Network_1, Host_A[1], Host_A[2], Host_A_Routing_Table)
HostB = Host("Host B", Host_B[0], Network_2, Host_B[1], Host_B[2], Host_B_Routing_Table)
Router1 = Router("Router R1", [Router_interface_1[0], Router_interface_2[0]], [Router_interface_1[1], Router_interface_2[1]], Router_Routing_Table)


input_size = int(sys.argv[1])
print("Host A: Layer 4: Data received from Application Layer. Data size= ",input_size)

frame = HostA.create_segment(input_size, HostB)
frame = Router1.receive_frame(frame)
HostB.receive_frame(frame, 0)

ack = HostB.create_ack(1, HostA)
ack = Router1.receive_frame(ack)
HostA.receive_frame(ack, 1)