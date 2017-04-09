from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class oauth(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(oauth, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("google_oauth_token", type=str, required=False, help="No google_oauth_token Provided")
        args = self.reqparse.parse_args()
        initConnection()
        bid = args["google_oauth_token"]
        print(bid)
        # get from rethink;
        isitthere = r.db("beaconrebuild").table("user").filter({"google_oauth_token": bid}).count().run()
        print(isitthere)
        if (isitthere <= 0):
            return {"error": "1"}

        ntbl = r.db("beaconrebuild").table("user").get_all(bid, index="google_oauth_token").run()
        # print(ntbl)
        toJSON = []
        for doc in ntbl:
            toJSON = removekey(doc, "google_oauth_token")
        # print(toJSON)
        return toJSON
        # return {"g":"g"}

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
