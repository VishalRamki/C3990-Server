from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class userfavourite(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userfavourite, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("user_id", type=str, required=True, help="User ID Not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()

        response = r.db("beaconrebuild").table("user_favouritestore").get_all(args["user_id"], index="user_id").run()

        ## okay for each user;

        document = []
        fs = []
        for user in response:
            ## use the single user to create
            for store in user["favouritestores"]:
                x = r.db("beaconrebuild").table("store").filter({"store_id": store}).run()
                # for each;
                for store in x:
                    z = r.db("beaconrebuild").table("store_promotion").filter({"store_id": store["store_id"], "active": "yes"}).run()
                    for promo in z:
                        store["promotion"] = promo
                    fs.append(store)
            user["favouritestores"] = fs
            return user

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("user_id", type=str, required=True, help="User ID Not Defined.", location="json")
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store Id", location="json")
        args = self.reqparse.parse_args()
        initConnection()

        count = r.db("beaconrebuild").table("user_favouritestore").get_all(args["user_id"], index="user_id").count().run()
        if (count <= 0):
            r.db("beaconrebuild").table("user_favouritestore").insert({"user_id": args["user_id"], "favouritestores": []}).run()

        toJSON = json.loads(args["update"])

        r.db("beaconrebuild").table("user_favouritestore").get_all(args["user_id"],index="user_id").update({
            "favouritestores": r.row["favouritestores"].default([]).append(args["store_id"])
        }).run()

        return []
