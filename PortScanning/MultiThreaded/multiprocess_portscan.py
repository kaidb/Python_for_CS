#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool,Lock, cpu_count
from functools import partial
import subprocess
import socket
import time
import sys
import argparse


###################
## Configuration ##
###################
socket.setdefaulttimeout(.5)
print_lock = Lock()
# Number of Avaiable CPU cores
NUM_CORES = cpu_count()

# No need for this method not
del cpu_count


def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con = sock.connect((host,port))
        with print_lock:
            print( "Port {}:      Open".format(port))
        return port
    except socket.timeout as err:
        return False



def scan_ports(host, lower=1, upper=1024):
    # processs pool 65536
    p = Pool(NUM_CORES * 2)

    # Generate new function ping(host=host, port)
    ping_host = partial(scan_port, host)
    # Filter out all closed ports that returned false
    return filter(bool, p.map(ping_host, range(lower, upper)))


def main():
    args = sys.argv
    try:
        remoteServer = args[1]
        print(remoteServer)
    except:
        print("Usage not understood...")
        remoteServer    = input("Enter a remote host to scan: ")

    if len(args) == 4:
        upper = args[2]
        lower = args[3]
    print_str = "* Please wait, scanning remote host {} *".format(remoteServer)
    pad = len(print_str)
    # print Banner
    print( "*" * pad)
    print( print_str)
    print( "*" * pad)
    ports = list(scan_ports(remoteServer))
    print("\nDone.")

    print(str(len(ports)) + " ports available.")
    print(ports)


if __name__ == "__main__":
    # process sys args
    parser = argparse.ArgumentParser(description='Multi-Threaded Port Scanner in pure python')
    parser.add_argument("host", help="Target host to port scan",
                    type=str)
    parser.add_argument("port_range", help="Target host to port scan",
                    type=str)


    start = time.time()
    print("There are {} CPU cores that this process can leverage!".format(NUM_CORES))
    subprocess.call('clear', shell=True)
    try:
        main()

    except KeyboardInterrupt:
        print( "You pressed Ctrl+C")
        sys.exit()
    except socket.gaierror:
        print( 'Hostname could not be resolved.')
        sys.exit()

    print("Finished Scanning in {} seconds.".format(time.time() - start))
