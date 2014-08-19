#!/usr/bin/env python
"""MongoDB Performance Test"""

import time
import pymongo
import sys


def select(client):
    num = 100000

    query = {
        "loc": {
            "$near": {
                "$geometry" : {
                    "type" : "Point" , "coordinates": [ 0.1, 0.1 ] }, "$maxDistance": 100
            }
        }
    }

    db = client.geodb
    for i in range(num):
        posts = db.test.find(query)
        #print posts.count()
        for post in posts:
            pass
        #print post

def execute(func, client):
    start = time.time()
    func(client)
    stop = time.time()
    print "%s: %s" % (func.func_name, stop - start)

def main(argv):
    client = pymongo.MongoClient('localhost', 27017)
    execute(select, client)

if __name__ == "__main__":
    main(sys.argv[1:])
