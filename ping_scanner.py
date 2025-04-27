#!/usr/bin/env python3


import asyncio
import sys
import os
from icmplib import async_multiping
import argparse
from sys import exit, argv


# Add flaggs
parser = argparse.ArgumentParser(description="Netword Ping Scanner")
parser.add_argument("-c", "--cidr", required=True,
                    help="CIDR notation", type=str)


# Format the CIDR Range to be used in the async function
args = parser.parse_args()
# Prints help menu if no arguments are given
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

cidr_part = args.cidr.split("/")[0]
base = ".".join(cidr_part.split(".")[:-1])

# If alive.txt already exists, remove it
if os.path.exists("alive.txt"):
    os.remove("alive.txt")

# Print a little message to let the user know whats going on
print(f"[+] Scanning {args.cidr}")


# Main function that pings the IP's in CIDR range
async def net_scan():
    # Formatting the user input into IP's ina  range
    ip_list = [f"{base}.{i}" for i in range(1, 254)]
    # Sending ICMP ping's to multiple hosts
    hosts = await async_multiping(
        ip_list, count=1, privileged=False, interval=1, family=4
    )

    for host in hosts:
        if host.is_alive:
            # If host is alive prints to screen
            print(f"[+] {host.address} is alive...")

            # If host is alive saves to file for later
            with open("alive.txt", "a") as f:
                f.write(f"{host.address}\n")


try:
    asyncio.run(net_scan())

# Handles user keyboard intrupts gracefully
except KeyboardInterrupt:
    print("\n[-] Keyboard interupt detected closing...")
    print("[+] Done")
    sys.exit(0)
