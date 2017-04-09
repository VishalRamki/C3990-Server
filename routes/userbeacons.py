from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class userbeacons(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userbeacons, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("user_id", type =  str, required=True, help="No User ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        bid = args["user_id"]
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("beacon").get_all(args["user_id"], index="owner").count().run()
        if (count <= 0):
            return {"message": {
                "content": "That User has not interacted with any beacons."
            }}
        else:
            d = r.db("beaconrebuild").table("beacon").get_all(args["user_id"], index="owner").run()
            return returnJSON(d)

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
