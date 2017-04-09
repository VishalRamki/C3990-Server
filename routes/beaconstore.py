from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *


class beaconstore(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(beaconstore, self).__init__()

    ## HTTP GET METHOD
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
