
##  interactstat_store.py
##
##  provides the Stats Data for stores endpoint;
##
##  ENDPOINT: /api/stats/interact/store
##  REST STATES: GET
##
##  Input:
##  store_id: Flask looks in the default locations, including JSON
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X <GET/DELETE> -d '{"store_id": <string:store_id>}' http://localhost:5000/api/stats/interact/store

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


class interactstat_store(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(interactstat_store, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => [ArrayOf<customDocument>]
    ##    CustomDocument Example:  {
    ##      "beacon_id": <string:beacon_id>,
    ##      "date": <string:date>,
    ##      "promotion_id": <string:promotion_id>,
    ##      "store_id": <string:store_id>
    ##   }
    ##
    def get(self):
        self.reqparse.add_argument("store_id", type =  str, required=True, help="No Store ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        storeId = args["store_id"]
        ntbl = r.db("beaconrebuild").table("user_interactbeacon").filter(lambda store:
            store["interacted"]["store_id"].contains(storeId)
        ).run()
        tos = []
        for j in ntbl:
            for i in j["interacted"]:
                if i["store_id"] == storeId:
                    tos.append(i)
        return tos

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
