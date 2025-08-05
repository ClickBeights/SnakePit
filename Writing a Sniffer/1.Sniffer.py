import socket
import os

# Host to listen on:
# Can set this to all interfaces if testing in a VM Linux box as otherwise it gets confused with many interfaces.
HOST = '192.168.1.12'

def main():
    # Create raw socket.
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    # The 0 is to listen on all ports.
    sniffer.bind((HOST, 0))

    # Include the IP header in the capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Determine if we are on Windows, if so, send an IOCTL to the network driver to enable promiscuous mode.
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # Read one packet and print it entirely raw with no decoding "For testing purposes".
    print(sniffer.recvfrom(65535))

    # If we're on Windows, turn off promiscuous mode before exiting
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
    main()
