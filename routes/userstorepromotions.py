from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class userstorepromotions(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userstorepromotions, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("store_id", type =  str, required=True, help="No Store ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        smi = args["store_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("store_promotion").filter({"store_id": smi}).run();
        print(ntbl)
        # ntbl = r.db("beaconrebuild").table("store").eqJoin("beacons", r.db("beaconrebuild").table("store_promotion"), {index: "beacon_id"}).run()
        # print(ntbl)
        iterm = {}
        finalJSON = []
        for item in ntbl:
            finalJSON.append(item)

        return finalJSON
        # return ntbl
        # return returnJSON(ntbl)
    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
