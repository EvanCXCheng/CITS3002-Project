# CITS3002-Project

## Running The Program
To simulate sending a message of data size x, run:     
python main.py x

## Implementation

Segments, packets, and frames are represented with classes in the protocol.py file. Their headers are represented  
with their own classes, which are included with the data in the segment/packet/frame class.  
The config.py file includes the known fixed topology for the simulation. For simplicity, each node in the network can  
access everything in the config file, to avoid having to share them on instantiation.  
The devices.py file includes classes used for Hosts and the Router. The classes include methods for all the major data transfer,  
including all the major functionalities of the data link, network, and transport layer. Where possible, the methods will call each other 
to correctly simulate how a Host/Router can do much of the processing in isolation.  
When the data is transferred across links, the logic for this is handled in main.py, with main running commands for data to be received from a host,  
and the hosts performing the rest of the encapsulation and verification on their own. If at any point an error occurs (rdt sequence number wrong or  
checksum wrong), the program either resends the data or ACK as required. main.py also instantiates the hosts and router, reads in the data size,  
creates data as random bytes for that size, then sends them in 500 byte segments (max data size).

