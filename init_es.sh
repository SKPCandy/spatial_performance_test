#!/bin/sh

curl -XDELETE http://localhost:9200/test_index

curl -XPUT http://localhost:9200/test_index -d '
{
    "mappings": {
        "poi": {
            "properties": {
                "poi_id": {"type": "string"},
                "location": {"type": "geo_point"}
            }
        }
    }
}
'
#curl -XPOST http://localhost:9200/test_index/poi/ -d '{"id": "1", "location": {"lat": "61.2180556", "lon": "-149.9002778"}}'
#
#
#curl -XGET 'http://localhost:9200/test_index/poi/_search?pretty=true' -d '
#{
#  "query": {
#    "filtered" : {
#        "query" : {
#            "match_all" : {}
#        },
#        "filter" : {
#            "geo_distance" : {
#                "distance" : "20km",
#                "location" : {
#                    "lat" : 37.9174,
#                    "lon" : -122.3050
#                }
#            }
#        }
#    }
#  }
#}'
