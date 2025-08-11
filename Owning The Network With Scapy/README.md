# Scapy 

This section demonstrates one of the most used netowrk modules <b>Scapy</b>. The first script shows a basic network sniffer that retrieves the first packet it sniffs and 
prints out detailed information broken down in sections by the module.  
<br>

## Sniffing Clear Text Credentials

The second script on the list <b>2.Mail_Sniffer.py</b> steals clear text email and password if:
1. The user/pass fields match the ones we defined in the script.
2. The protocol to sniff credentials on is defined in the scirpt.
3. The protocol is not encrypted (Clear-Text).
  
Furthermore, it shows how 1 module can save us many lines as this script also sniffs the network, but without the decoding overhead.
<br>
<br>
## ARP Poisoning
The idea of ARP poisoning has been around since forever, however when you build your own, you appreciate the available tools even more.
The third script in the directory demonstrates how Scapy can be used to poison ARP tables. The only addition to the original script is the <b>loggin</b> library 
which was used to suppress runtime warnings.
