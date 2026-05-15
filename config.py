#parameters (IP, MAC, routing tables)
Network_1 = "10.0.1.0/24"
Network_2 = "10.0.2.0/24"
Router_interface_1 = ["10.0.1.1", "BB:BB:BB:BB:BB:BB"]
Router_interface_2 = ["10.0.2.1", "CC:CC:CC:CC:CC:CC"]
Host_A = ["10.0.1.10", "AA:AA:AA:AA:AA:AA", 5000]
Host_B = ["10.0.2.20", "DD:DD:DD:DD:DD:DD", 80]
Host_A_Routing_Table = {"10.0.2.20" : "10.0.1.1"}
Host_B_Routing_Table = {"10.0.1.10" : "10.0.2.1"}
Router_Routing_Table = {"10.0.2.20" : ["10.0.2.20", "CC:CC:CC:CC:CC:CC"], "10.0.1.10" : ["10.0.1.10", "BB:BB:BB:BB:BB:BB"]}
IP_MAC_Table = {
    "10.0.1.10" : "AA:AA:AA:AA:AA:AA",
    "10.0.1.1" : "BB:BB:BB:BB:BB:BB",
    "10.0.2.1" : "CC:CC:CC:CC:CC:CC",
    "10.0.2.20" : "DD:DD:DD:DD:DD:DD"
}