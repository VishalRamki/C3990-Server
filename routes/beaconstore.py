##  beaconstore.py
##
##  provides the beaconstore endpoint;
##
##  ENDPOINT: /api/beacon/store
##  REST STATES: GET
##  Input:
##  beacon_id - Flask looks in the default locations
##
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X GET -d '{"beacon_id": <string:beacon_id>}' http://localhost:5000/api/beacon/store


##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

##  Required Database
import rethinkdb as r
##  Required Python Packages;
import json, uuid, sys

## Custom Helper Functions
from functions import *


class beaconstore(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(beaconstore, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##      if Flask doesn't catch any input faux paux, then an empty [] is all they get.
    ##  onSuccess => 5
    ##    [
    ##     {
    ##         "beacons": [ArrayOf<string:beacon_id>],
    ##         "id": <string:id>,
    ##         "name": <string:name>,
    ##         "lat": <string:lat>,
    ##         "long": <string:long>
    ##         "promotion": [ ArrayOf<Document:promotion> ]
    ##             EXAMPLE DOCUMENT: {
    ##                 "active": <string:active>,
    ##                 "coupon": <string:coupon>,
    ##                 "expires": <string:expires>,
    ##                 "id": <string:id>,
    ##                 "message": <string:message>,
    ##                 "present": <string:present>,
    ##                 "promotionImage": <string:promotionImage>,
    ##                 "promotion_id": <string:promotion_id>,
    ##                 "store_id": <string:store_id>,
    ##                 "title": <string:title>
    ##             }
    ##         ,
    ##         "store_id": <string:store_id>,
    ##         "store_manager_id": <string:store_manager_id>
    ##     }
    ##  ]

    def get(self):
        self.reqparse.add_argument("beacon_id", type =  str, required=True, help="No Beacon ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        beaconId = args["beacon_id"]
        ntbl = r.db("beaconrebuild").table("store").filter(lambda store:
            store["beacons"].contains(beaconId)
        ).run()
        returnItem = []
        for item in ntbl:
            activePromo = r.db("beaconrebuild").table("store_promotion").filter({"store_id": item["store_id"], "active": "yes"}).run()
            item["promotion"] = returnJSON(activePromo)
            returnItem.append(item)
        return returnItem

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
