#!/usr/bin/env python
"""Redis Performance Test

Options:
    -i  insert
    -s  select
"""
import socket
import time
import redis
import sys
import getopt

# pylint: disable=C0103
# pylint: disable=C0111

class GRedis(object):
    "geo command"
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, int(self.port)))

    def geoadd(self, geoset, member, x, y):
        packet = 'geoadd %s %s %s "%s"\r\n' % (geoset, x, y, member)
        self.sock.sendall(packet)

        fp = self.sock.makefile('r')
        packet = fp.readline()
        return packet

    def georadius(self, geoset, x, y, radius):
        packet = 'georadius %s %s %s %s m\r\n' % (geoset, x, y, radius)
        self.sock.sendall(packet)

        fp = self.sock.makefile('r')
        packet = fp.readline()
        num = int(packet[1:])

        for i in xrange(num):
            length = fp.readline()
            value = fp.readline()
        return num


def insert(client):
    num = 1000
    unit = 0.001
    member = 0

    for i in range(num):
        for j in range(num):
            x = i * unit
            y = j * unit
            client.geoadd("test", str(member), x, y)
            member += 1

def select(client):
    num = 100000
    for i in range(num):
        ret = client.georadius("test", 0.1, 0.1, 100)
        if ret != 1:
            print "error"

def execute(func, client):
    start = time.time()
    func(client)
    stop = time.time()
    print "%s: %s" % (func.func_name, stop - start)

def usage():
    print __doc__

def main(argv):
    host = "localhost"
    port = 6379

    # parse options
    insert_test = False
    search_test = False

    if not len(argv):
        usage()
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "is")
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == "-i":
            insert_test = True
        elif opt == "-s":
            search_test = True

    # execute test
    r = redis.StrictRedis(host=host, port=int(port))
    r.delete("test")

    client = GRedis(host, port)
    client.connect()

    if insert_test:
        execute(insert, client)

    if search_test:
        execute(select, client)

if __name__ == "__main__":
    main(sys.argv[1:])
