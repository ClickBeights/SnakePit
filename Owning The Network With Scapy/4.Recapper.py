from scapy.all import TCP, rdpcap

import collections
import os
import re
import sys
import zlib

OUTDIR = '/home/kali/Pictures'
PCAPS = '/home/kali'

# The following is a named-tuple of the response.
Response = collections.namedtuple('Response', ['header', 'payload'])

# 2/1 Helper function to get packet header.
def get_header(payload):
    try:
        # Take raw HTTP traffic and spit out the headers by extracting the portion of the payload that:
        # Starts at the beginning and ends with a couple of carriage return and newline pairs.
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    # Create a dictionary (header) from th decoded payload ,splitting on the colon so that the key is the part before
    # the colon and the value is the part after the colon.
    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', header_raw.decode()))
    # If the header has no key called 'Content-Type', we return None.
    if 'Content-Type' not in header:
        return None
    return header

# 2/2 Helper function to extract content of packet.
def extract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']:
        # Create variable with the 'Content-Type' from the response.
        content_type = Response.header['Content-Type'].split('/')[1]
        # Hold the content of the header itself in another variable.
        content = Response.payload[Response.payload.index(b'\r\n\r\n')+4:]
        # Decompress the content if compressed with eiter 'gzip' or 'deflate'
        if 'Content-Encoding' in Response.header:
            if Response.header['Content-Encoding'] == "gzip":
                content = zlib.decompress(Response.payload, zlib.MAX_WBITS | 32)
            elif Response.header['Content-Encoding'] == 'deflate':
                content = zlib.decompress(Response.payload)
    return content, content_type

# Reconstitutes the image presented in the packet stream.
class Recapper:
    def __init__(self, fname):
        pcap = rdpcap(fname)
        # Scapy automatically separates each TCP session for us and saves it here.
        self.sessions = pcap.sessions()
        # Create empty list to get filled with the PCAP file.
        self.responses = list()

    # A method to read the response from the PCAP fle.
    def get_response(self):
        # Iterate over the session dictionary.
        for session in self.sessions:
            payload = b''
            # Then iterate over the packets of each session.
            for packet in self.sessions[session]:
                try:
                    # Filter traffic for TCP port 80 only.
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        # Concatenate the payload of all traffic into a single payload.
                        # Same as clicking follow stream on WireShark.
                        payload += bytes(packet[TCP].payload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()
            if payload:
                # Pass the full reassembled HTTP data the variable below.
                header = get_header(payload)
                if header is None:
                    continue
                # Append the response to the response list.
                self.responses.append(Response(header=header, payload=payload))

    # A method to write the image file contained in the response and place in the directory declared earlier.
    def write(self, content_name):
        # Iterate only over the responses.
        for i, response in enumerate(self.responses):
            # Extract the content.
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                print(f'Writing {fname}')
                # Write to a file.
                with open(fname, 'wb') as f:
                    f.write(content)

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_response()
    recapper.write('image')
