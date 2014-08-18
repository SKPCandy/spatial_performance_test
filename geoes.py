#!/usr/bin/env python

import time
import json
from elasticsearch import Elasticsearch

def insert(es):
    unit = 0.001
    num = 1000
    member = 0

    for i in xrange(num):
        for j in xrange(num):
            x = i * unit
            y = j * unit

            doc = {
                "poi_id": member,
                "location": {"lat": x, "lon": y}
            }

            es.index(index="test_index", doc_type="poi", body=doc)
            member += 1

def select(es):
    doc = {
        "query": {
            "filtered" : {
                "query" : {
                    "match_all" : {}
                },
                "filter": {
                    "geo_distance" : {
                        "distance" : "100 m",
                        "location" : {
                            "lat" : 0.1,
                            "lon" : 0.1
                        }
                    }
                }
            }
        }
    }

    for i in xrange(100000):
        es.search(index="test_index", doc_type="poi", body=doc)


def execute(f, es):
    start = time.time()
    f(es)
    stop = time.time()
    print "%s: %s" % (f.func_name, stop - start)

if __name__ == "__main__":
    es = Elasticsearch(hosts=["10.202.67.200:9200"])
    execute(insert, es)
    #execute(select, es)
