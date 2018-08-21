#!/usr/bin/env python
import subprocess
import socket
import sys
from tqdm import tqdm


#
# Config socket timeout to .5 seconds
socket.setdefaulttimeout(.5)


"""
@ Author: Kai Bernardini
Single threaded port scanner. I take no responsibility for any missuse. See
License for more details.

Example Usage:
$ python3 portscan.py  hackthissite.org

# Note:  hackthissite.org gives express permission to port scan it.
# More pythonic version of a port scanner can be seen in other examples
"""


def port_scan(host, port):
    """
    Attempts to connect to a host as a particular port
    @Arguments:
    host -- the ip address or server hostname to scan
    port -- port to connect to
    """

    # (AF_INET, SOCK_STREAM) <==> (IPV4, TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Try to connect to host:port.
        con = sock.connect((host,port))
        print( "Port {}:      Open".format(port))
        sock.close()
        return port
    except socket.timeout:
        # If theres a time out, the port is probably closed
        return False


def main():
    # Clear the screen
    subprocess.call('clear', shell=True)

    # Ask for input if none is given
    args = sys.argv
    print(args)

    try:
        remoteServer = args[1]
    except:
        print("Usage not understood...")
        remoteServer    = input("Enter a remote host to scan: ")
    #
    target  = socket.gethostbyname(remoteServer)
    print_str = "* Please wait, scanning remote host {} *".format(remoteServer)
    pad = len(print_str)
    # print start
    print( "*" * pad)
    print( print_str)
    print( "*" * pad)

    open_ports = []
    try:
        # could use use a more pythonic  line
        # return filter(map(port_scan))
        for port in tqdm(range(1,1024)):
            is_open = port_scan(target, port)
            open_ports.append(is_open)

    except KeyboardInterrupt:
        print( "You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print( 'Hostname could not be resolved.')
        sys.exit()

    except socket.error:
        print( "Server Connection Error")
        sys.exit()
    return filter(open_ports)


if __name__ == '__main__':
    main()
