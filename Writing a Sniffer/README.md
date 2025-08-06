# Writing a Sniffer

This section demonstrates how to build a sniffer in python, starting with a single raw packet capture using 1.Sniffer.py

## Decoding the IP layer

The second script (<b>2.Sniffer_IP_Header_Decoder.py</b>) in this directory was created to better understand how to extract IP addresses from a binary formed raw packet.  
It uses the struct module to define a python structure that maps the first 20 bytes of the received buffer into a friendly IP header. 
Furthermore, we use bit shifting to assign either high-order nybble or low-order nybble by either shifting bits right or left.
