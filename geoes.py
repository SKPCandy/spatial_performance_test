#!/usr/bin/env python
"""Elasticsearch Performance Test

Options:
    -i  insert
    -s  search
"""

import time
import sys
import getopt
from elasticsearch import Elasticsearch

# pylint: disable=C0111
# pylint: disable=C0103

def insert(es):
    num = 1000 # total num = num * num
    unit = 0.001
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
    num = 10

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

    for i in xrange(num):
        es.search(index="test_index", doc_type="poi", body=doc)

def execute(func, es):
    start = time.time()
    func(es)
    stop = time.time()
    print "%s: %s" % (func.func_name, stop - start)

def usage():
    print __doc__

def main(argv):
    # parse options
    insert_test = False
    search_test = False

    if len(argv) == 0:
        usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(argv, "is")
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-i":
            insert_test = True
        elif opt == "-s":
            search_test = True

    # execute test
    es = Elasticsearch(hosts=["10.202.67.200:9200"])

    if insert_test:
        execute(insert, es)

    if search_test:
        execute(select, es)

if __name__ == "__main__":
    main(sys.argv[1:])
