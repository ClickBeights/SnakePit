import ipaddress
import os
import socket
import struct
import sys

# Defines a python structure that will map the first 20 bytes of the received buffer into a friendly IP header.
class IP:
    # self is how Python remembers the data inside your object.
    # buff is the buffer or binary data that will be formated.
    def __init__(self, buff=None):
        # Interpret the raw buffer buff using a specific binary layout. The format string '<BBHHHBBH4s4s' says:
        # < = little endian for x64 machine native format
        # B = 1 byte (unsigned char)
        # H = 2 bytes (unsigned short)
        # 4s = 4 bytes as a string (used for IPs)
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        # The following 2 lines are binary manipulation which is required to specify bits width (Easier with ctypes).
        # Right-Shift the byte by 4 (prepending four 0s) to get only the high-order nybble (1st 4 bits in the byte).
        self.ver = header[0] >> 4
        # Using the Boolean & with 0xF (00001111) to apply 1s on the low-order nybble. This effectively nullifies the
        # high-order nybble and leaves the last 4 bits unaltered. 1 & 1 = 1.
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # Human-readable IP address
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Map protocol constants to their names
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No Protocol for %s' % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)

def sniff(host):
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # Determine if we are on Windows, if so, send an IOCTL to the network driver to enable promiscuous mode.
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            # Read a packet. This grabs just the raw packet data, and ignores the sender info.
            raw_buffer = sniffer.recvfrom(65535)[0]
            # Create an IP header from the first 20 bytes. Extracts the first 20 bytes of the IP packet (the IP header)
            ip_header = IP(raw_buffer[0:20])
            # Print the detected protocol and hosts
            print('Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
    except KeyboardInterrupt:
        # If used on Windows, turn off promiscuous mode
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.1.20'
    sniff(host)
