#!/usr/bin/env python

import argparse
import subprocess

def get_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-i", "--interface", dest="interface", help="Which interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="What to change the MAC address to")
    args = parser.parse_args()
    if not args.interface:
        parser.error("You must specify an interface, see --help")
    elif not args.new_mac:
        parser.error("You must specify a new MAC address, see --help")
    return args
    
def change_mac(interface, new_mac):
    print("Changing MAC address for {} to {}").format(interface, new_mac)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

options = get_args()
change_mac(options.interface, options.new_mac)