#!/usr/bin/env python
"""Postgres Performance Test

Options:
    -i  insert
    -s  search
"""

import psycopg2
import time
import sys
import getopt

# pylint: disable=C0111

def drop_table(conn):
    cur = conn.cursor()
    cur.execute("drop index geo_index;")
    cur.execute("drop table geotest;")
    cur.close()

def create_table(conn):
    cur = conn.cursor()
    cur.execute("create table geotest(id integer, geom geometry);")
    cur.execute("create index geo_index on geotest using gist(geom);")
    cur.close()

def insert(conn):
    num = 1000
    unit = 0.001
    member = 0

    cur = conn.cursor()
    for i in xrange(num):
        for j in xrange(num):
            x = i * unit
            y = j * unit
            stmts = "insert into geotest values(%s, 'point(%s %s)');" % (member, x, y)
            cur.execute(stmts)
            member += 1
    cur.close()
    conn.commit()

def select(conn):
    num = 100000

    cur = conn.cursor()
    for i in xrange(num):
        cur.execute(
            "select id, st_astext(geom) from geotest where st_dwithin(geom, 'point(0.1 0.1)', 0.0001);")
        for record in cur:
            pass
    cur.close()

def execute(func, conn):
    start = time.time()
    func(conn)
    stop = time.time()
    print "%s: %s" % (func.func_name, stop - start)

def usage():
    print __doc__

def main(argv):
    insert_test = False
    search_test = False

    # parse options
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
    conn = psycopg2.connect(host="127.0.0.1", dbname="test", user="lordsday")

    drop_table(conn)
    create_table(conn)

    if insert_test:
        execute(insert, conn)

    if search_test:
        execute(select, conn)

    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])
