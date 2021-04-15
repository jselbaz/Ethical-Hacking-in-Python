#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-t", "--target", dest="target", help="Target IP or IP range")
    args = parser.parse_args()
    if not args.target:
        parser.error("You must specify a target, see --help")
    return args

def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    answered = scapy.srp(arp_req_broadcast, timeout=2, verbose=False)[0]

    client_list = []
    for packet in answered:
        client_dict = {"IP":packet[1].psrc,"MAC":packet[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_results(result_list):
    print("IP\t\t\tMAC Address")
    print("-----------------------------------------")
    for result in result_list:
        print(result["IP"] + "\t\t" + result["MAC"])

args = get_args()
scanned = scan(args.target)
print_results(scanned)