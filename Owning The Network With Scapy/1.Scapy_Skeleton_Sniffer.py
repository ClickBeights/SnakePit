# Scapy: Interactive packet manipulation tool.
from scapy.all import sniff
# An aptly usage looks as follows: sniff(filter="", iface="any", prn=function, count=N)
# filter uses BPF to filter sniffed packets.
# iface uses network interfaces, empty = all.
# prn is used to call back a function that will take the packet as single parameter if matched.
# counter is for ow many packets we want to sniff, empty = unlimited.

# The call back function that will receive the packet. Basically printing the packet using show().
def packet_callback(packet):
    print(packet.show())

# Command Scapy to start sniffing.
def main():
    sniff(prn=packet_callback,count=1)

if __name__ == '__main__':
    main()
