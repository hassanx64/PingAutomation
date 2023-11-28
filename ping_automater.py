#!/usr/bin/python
import subprocess
import argparse
import platform

def check_ip(ip):
    # Adjusting ping command based on the operating system
    if platform.system().lower() == "windows":
        command = ['ping', '-n', '1', ip]  # Windows command for one ping packet
    else:
        command = ['ping', '-c', '1', ip]  # Linux/Unix command for one ping packet

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        if "1 received" in output:  # Check for success response in the output
            return True, ip  # IP is reachable
        else:
            return False, ip  # IP is unreachable
    except subprocess.CalledProcessError:
        return False, ip  # IP is unreachable

def ping_from_file(filename):
    try:
        with open(filename, 'r') as file:
            ips_to_ping = file.read().splitlines()
            results = [check_ip(ip) for ip in ips_to_ping]
            reachable_ips = [ip for (reachable, ip) in results if reachable]
            unreachable_ips = [ip for (reachable, ip) in results if not reachable]

            print("Reachable IPs:")
            for ip in reachable_ips:
                print(ip)

            print("\nUnreachable IPs:")
            for ip in unreachable_ips:
                print(ip)

            print(f"\nTotal Reachable IPs: {len(reachable_ips)}")
            print(f"Total Unreachable IPs: {len(unreachable_ips)}")

    except FileNotFoundError:
        print("File not found.")

# Parsing command line arguments
parser = argparse.ArgumentParser(description='Ping IPs from a file')
parser.add_argument('-f', '--file', help='File containing list of IPs to ping', required=True)
args = parser.parse_args()

# Calling function to ping IPs from the file
ping_from_file(args.file)
