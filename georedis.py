#!/usr/bin/env python
"""geo command client"""
import socket
import time
import redis

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

if __name__ == "__main__":
    host = "localhost"
    port = 6379

    unit = 0.001
    num = 1000
    member = 0

    client = GRedis(host, port)
    client.connect()


    # insert
#    r = redis.StrictRedis(host='localhost', port=int(port))
#    r.delete("test")
#
#    start = time.time()
#    for i in range(num):
#        for j in range(num):
#            x = i * unit
#            y = j * unit
#            client.geoadd("test", str(member), x, y)
#            member += 1
#
#    end = time.time()
#    execute_time = (end - start)
#    print "insert time(%s): %s" % (num*num, execute_time)

    # search
    start = time.time()

    for i in range(100000):
        ret = client.georadius("test", 0.1, 0.1, 100)
        if ret != 1:
            print "error"

    end = time.time()
    execute_time = (end - start)
    print "search time: %s" % execute_time
