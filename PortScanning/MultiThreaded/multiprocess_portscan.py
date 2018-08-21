#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool,Lock, cpu_count
from functools import partial
import subprocess
import socket
import time
import sys
import argparse


"""
@ Author: Kai Bernardini
Multithreaded port scanner using multiprocessing. I take no responsibility for any missuse. See
License for more details.

Example Usage:
$ python3 multiprocess_portscan.py  hackthissite.org 1-1024

# Note:  hackthissite.org gives express permission to port scan it.
# More pythonic version of a port scanner can be seen in other examples
"""



###########################
###### Configuration ######
###########################
# Set Default timeout for a socket to .5 seoncds
# You may need to tune this depending on the RTT
# for your target host

socket.setdefaulttimeout(.5)
# prevent printing errors
print_lock = Lock()

# Number of Avaiable CPU cores
NUM_CORES = cpu_count()
# Determines how many threads per core will be spun up
virtualization_param = 2


# No need for this method now
del cpu_count


def port_scan(host, port):
    """
    Attempts to connect to a host as a particular port
    @Arguments:
    host -- the ip address or server hostname to scan
    port -- port to connect to
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con = sock.connect((host,port))
        with print_lock:
            print( "Port {}:      Open".format(port))
        return port
    except socket.timeout as err:
        return False



def scan_ports(host, lower=1, upper=1024):
    # With 8 cores, we would have 16 virtual threads
    p = Pool(NUM_CORES * virtualization_param)

    # Generate new function ping(host=host, port)
    ping_host = partial(port_scan, host)
    # Filter out all closed ports that returned false
    return filter(bool, p.map(ping_host, range(lower, upper)))


def main(remoteServer, port_range):
    args = sys.argv

    print_str = "* Please wait, scanning remote host {} *".format(remoteServer)
    pad = len(print_str)
    lower, upper = port_range[0], port_range[1]
    # print Banner
    print( "*" * pad)
    print( print_str)
    print( "*" * pad)
    ports = list(scan_ports(remoteServer,lower, upper ))
    print("Done.")

    print(str(len(ports)) + " ports available.")
    print(ports)


if __name__ == "__main__":
    # process sys args
    parser = argparse.ArgumentParser(description='Multi-Threaded Port Scanner in pure python')
    parser.add_argument("host", help="Target host to port scan",
                    type=str)
    parser.add_argument("port_range", help="Range of ports to scan. Example: -port_range 1-1024",
                    type=str)
    args = parser.parse_args()
    host = socket.gethostbyname(args.host)

    # [lower, upper]
    port_range = list(map(int, args.port_range.split('-')))

    start = time.time()
    print("There are {} CPU cores that this process can leverage!".format(NUM_CORES))
    subprocess.call('clear', shell=True)
    try:
        main(host, port_range)

    except KeyboardInterrupt:
        print( "You pressed Ctrl+C")
        sys.exit()
    except socket.gaierror:
        print( 'Hostname could not be resolved.')
        sys.exit()

    print("Finished Scanning in {} seconds.".format(time.time() - start))
