#!/usr/bin/env python
import subprocess
import sys
import threading
from queue import Queue
import time
import socket


"""
TODO: cleanup, argparse.
"""

# Config socket timeout to .5 seconds
socket.setdefaulttimeout(.5)

# Create the queue and threader
q = Queue()

# Creates a lock to standard output.
print_lock = threading.Lock()


def port_scan(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = sock.connect((target,port))
        with print_lock:
            print( "Port {}:      Open".format(port))
        sock.close()
    except socket.timeout:
        # timeout
        pass

# Retrieve the first free worker in
def threader():
    while True:
        # gets an worker from the queue
        target, port = q.get()

        # Run the example job with the avail worker in queue (thread)
        port_scan(target, port)

        # completed with the job
        q.task_done()

def main():
    # Clear the screen
    subprocess.call('clear', shell=True)

    # how many threads are we going to allow for
    n_threads = 16

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




    for x in range(n_threads):
        t = threading.Thread(target=threader)

        # classifying as a daemon, so they will die when the main dies
        t.daemon = True

        # begins, must come after daemon definition
        t.start()
    start = time.time()

    try:
        for port in range(1,65536):
            q.put((target, port))

        q.join()
    except KeyboardInterrupt:
        print( "You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print( 'Hostname could not be resolved.')
        sys.exit()

    except socket.error:
        print( "Server Connection Error")
        sys.exit()
    print("Finished in {}".format(time.time() - start))


if __name__ == '__main__':
    main()
