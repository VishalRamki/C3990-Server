from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *


class interactstat_store(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(interactstat_store, self).__init__()

    ## HTTP GET METHOD
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
