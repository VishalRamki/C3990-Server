from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *


class userstores(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userstores, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("store_manager_id", type =  str, required=True, help="No Store Manager ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        print("store_manager_id: ", args["store_manager_id"])
        smi = args["store_manager_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("store").filter({"store_manager_id": smi}).run();
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
