
##  interactstat_userstorepromo.py
##
##  provides the Stats Data for stores endpoint;
##
##  ENDPOINT: ?
##  REST STATES: GET
##
##  Input:
##  store_id: Flask looks in the default locations, including JSON
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X <GET/DELETE> -d '{"store_id": <string:store_id>}' http://localhost:5000/api/stats/interact/user/store

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


class interactstat_userstorepromo(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(interactstat_userstorepromo, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => [ArrayOf<customDocument>]
    def get(self):
        self.reqparse.add_argument("store_id", type =  str, required=True, help="No User ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        userId = args["store_id"]

        ## Get all of the stores managed by userId
        ntbl = r.db("beaconrebuild").table("store_promotion").filter({"store_id": userId}).run();

        tos = []
        beacons = []
        ## for each store
        for i in ntbl:
            ## get each beacon assigned to the store;
            for beacon in i["beacons"]:
                ## run a query to determine all the users who have interacted with this beacon;
                q2 = r.db("beaconrebuild").table("user_interactbeacon").filter(lambda store:
                        store["interacted"]["beacon_id"].contains(beacon)
                     ).run()

                # for each user that interacted with this beacon;
                for j in q2:
                    ## pull out the interaction
                    for interaction in j["interacted"]:
                        if interaction["beacon_id"] == beacon:
                            interaction["storeName"] = i["name"]
                            tos.append(interaction)
        # return an array of documents with contain the beacon_id, store_id and date;
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
