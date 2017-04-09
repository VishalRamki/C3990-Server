from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *


class interactstat_userstore(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(interactstat_userstore, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("user_id", type =  str, required=True, help="No User ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        userId = args["user_id"]
        # ntbl = r.db("beaconrebuild").table("store").filter({"store_manager_id": userId}).merge(lambda store:
        #     {"beacons": r.db("beaconrebuild").table("user_interactbeacon").filter(lambda store:
        #         store["interacted"]["beacon_id"].contains(store["beacons"])
        #     ).coerce_to("array")}
        # ).run()

        ## Get all of the stores managed by userId
        ntbl = r.db("beaconrebuild").table("store").filter({"store_manager_id": userId}).run();
        # return returnJSON(ntbl)
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
                # return returnJSON(q2)
                # for each user that interacted with this beacon;
                for j in q2:
                    # return returnJSON(j["interacted"])
                    ## pull out the interaction
                    for interaction in j["interacted"]:
                        if interaction["beacon_id"] == beacon:
                            interaction["storeName"] = i["name"]
                            ## now lets get the promotion data for it;
                            x = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": interaction["promotion_id"]}).run()
                            ## now get the single entity inside it;
                            for promo in x:
                                interaction["promotion"] = promo
                            tos.append(interaction)
            # beacons.append(tos)
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
