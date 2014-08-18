#!/usr/bin/env python
"test mongodb"
import time
import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient('localhost', 27017)
    db = client.geodb

    query = {
        "loc": {
            "$near": {
                "$geometry" : {
                    "type" : "Point" , "coordinates": [ 0.1, 0.1 ] }, "$maxDistance": 100
            }
        }
    }

    start = time.time()

    for i in range(100000):
        posts = db.test.find(query)
        #print posts.count()
        for post in posts:
            pass
        #print post

    end = time.time()
    execution_time = (end - start) # Convert to ms
    print execution_time
