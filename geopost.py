#!/usr/bin/env python
"test postgres"

import psycopg2
import time

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
    unit = 0.001
    num = 1000
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
    cur = conn.cursor()
    for i in xrange(100000):
        cur.execute(
            "select id, st_astext(geom) from geotest where st_dwithin(geom, 'point(0.1 0.1)', 0.0001);")
        for record in cur:
            pass
#            print record
    cur.close()

def execute(f, conn):
    start = time.time()
    f(conn)
    stop = time.time()
    print "%s: %s" % (f.func_name, stop - start)

def main():
    conn = psycopg2.connect(host="127.0.0.1", dbname="test", user="lordsday")

    execute(drop_table, conn)
    execute(create_table, conn)
    execute(insert, conn)
    #execute(select, conn)

    conn.close()

if __name__ == "__main__":
    main()
