from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class userbeaconinteraction(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userbeaconinteraction, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("user_id", type =  str, required=True, help="No User ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        bid = args["user_id"]
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("user").get_all(args["user_id"], index="user_id").count().run()
        if (count <= 0):
            return {"message": {
                "content": "That User has not interacted with any beacons."
            }}
        else:
            d = r.db("beaconrebuild").table("user").get_all(args["user_id"], index="user_id").run()
            return returnJSON(d)

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("user_id", type=str, required=True, help="User ID Not Defined.")
        self.reqparse.add_argument("update", type=str, required=True, help="Update Not Defined.")
        args = self.reqparse.parse_args()
        initConnection()

        count = r.db("beaconrebuild").table("user_interactbeacon").get_all(args["user_id"], index="user_id").count().run()
        if (count <= 0):
            r.db("beaconrebuild").table("user_interactbeacon").insert({"user_id": args["user_id"], "interacted": []}).run()

        toJSON = json.loads(args["update"].replace("'", '"'))

        r.db("beaconrebuild").table("user_interactbeacon").get_all(args["user_id"],index="user_id").update({
            "interacted": r.row["interacted"].default([]).append({"store_id": toJSON["store_id"], "beacon_id": toJSON["beacon_id"], "date": r.now().to_iso8601(), "promotion_id": toJSON["promotion_id"]})
        }).run()
