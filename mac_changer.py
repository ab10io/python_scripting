#!/usr/bin/env python

import subprocess
import re
import optparse


# Function to get the command line arguments
def get_options():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Please enter your interface name here!")
    parser.add_option("-m", "--mac_address", dest="mac_address", help="Please enter your mac address here!")
    options, arguments = parser.parse_args()

    if not options.interface:
        parser.error("Please enter your interface name.")
    elif not options.mac_address:
        parser.error("Please enter you new MAC address")

    print("[>] Parsing the arguments.")

    return options


# Function to get the current MAC address
def get_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))

    if mac_address_search:
        return mac_address_search[0]
    else:
        print("[-] Could not read MAC address")


# Change the MAC address
def change_mac_address(interface, new_mac):
    print("[+] Changing the MAC address for", interface, "to", new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("**************Changing the MAC address**************")
    subprocess.call(["ifconfig"])


# Calling functions
options = get_options()
old_mac_address = get_mac_address(options.interface)
print("[>] Old MAC address:", str(old_mac_address))
change_mac_address(options.interface, options.mac_address)
new_mac_address = get_mac_address(options.interface)
if new_mac_address == options.mac_address:
    print("[+] MAC address was successfully changed to: " + new_mac_address)
else:
    print("[-] MAC address couldn't be changed.")