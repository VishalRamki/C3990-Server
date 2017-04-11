
##  functions.py
##  command: [none]
##
##  Description:
##
##  functions.py contain generic functions used by multiple endpoints, particualrly
##  in the routes folder.

import rethinkdb as r
import json, uuid, sys


##
##  getBeacons([], {})
##
##  it is used by a couple endpoints prvide more data when returning.;
##
def getBeacons(beaconData, obj):
    nbeacons = r.db("beaconrebuild").table("store_promotion").get_all(obj["store_id"], index="store_id").run()
    print(nbeacons)
    bex = {}
    for beacon in nbeacons:
        bex["beacon_id"] = beacon["beacon_id"]
        bex["promotions"] = beacon["promotions"]
        obj["beacons"].append(bex)
    # ntt = r.db("beaconrebuild").table("store")
    return json.dumps(obj)


##
##  initConnection()
##
##  Used by all endpoints to connect to the database;
##  'locahost' refers to the database that is currently running on a server
##  next to it.
##
def initConnection():
    return r.connect("localhost", 28015).repl()


##
##  returnJSON(CURSOR or {})
##
##  this function was used to convert the Cursor object returned by RethinkDB
##  queries into a JSON appropriate reponse; (just a Dict)
##
def returnJSON(isitthere):
    jsons = []
    for i in isitthere:
        jsons.append(i)
    return jsons


##
##  removekey(DICTIONARY, STRING)
##
##  removes a particular key, denoted by STRING, from the dictionary;
##  used mostly when the server logic has to do an update by the update payload
##  contains data that isn't supposed to be there;
##
##  FROM @https://stackoverflow.com/questions/5844672/delete-an-item-from-a-dictionary
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r
