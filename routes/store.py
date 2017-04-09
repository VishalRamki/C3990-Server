from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *


class store(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(store, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("store_id", type =  str, required=True, help="No Store ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        print("store_id: ", args["store_id"])
        store_id = args["store_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("store").get_all(store_id, index="store_id").run()
        # ntbl = r.db("beaconrebuild").table("store").eqJoin("beacons", r.db("beaconrebuild").table("store_promotion"), {index: "beacon_id"}).run()
        # print(ntbl)
        iterm = {}
        finalJSON = []
        for item in ntbl:
            # iterm['store_id'] = item['store_id']
            # iterm["store_manager_id"] = item["store_manager_id"]
            # iterm["beacons"] = item["beacons"]
            finalJSON.append(item)
            # finalJSON.append(getBeacons(item["beacons"], iterm))

        # print(finalJSON)
        return finalJSON
        # return ntbl
        # return returnJSON(ntbl)
    ## HTTP DELETE METHOD
    def delete(self):
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store ID Not Defined.")
        args = self.reqparse.parse_args()
        initConnection()
        r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").delete().run()
        return {"deleted": args["store_id"]}

    ## HTTP PUT METHOD
    def put(self):
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store ID Not Defined.")
        self.reqparse.add_argument("update", type=str, required=True, help="JSON Update not Defined.")
        args = self.reqparse.parse_args()
        initConnection()
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").count().run()
        if (count <= 0):
            return {"message": {
                "content": "There is No Store with that ID"
            }}
        else:
            toJSON = json.loads(args["update"])
            if ("beacons" in toJSON):
                # return "BEACONS"
                r.db("beaconrebuild").table("store").get_all(args["store_id"],index="store_id").update({
            #         "beacons": r.row["beacons"].default([]).append({"beacon_id": toJSON["beacons"]["beacon_id"]})
                        "beacons": toJSON["beacons"]
                }).run()
                toJSON = removekey(toJSON, "beacons")
            # # sys.stdout.flush()
            r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").update(toJSON).run()
            nv = r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").limit(1).run()
            return returnJSON(nv)

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("store_manager_id", type=str, required=True, help="Store Manager Not Defined.")
        args = self.reqparse.parse_args()
        print(args["store_manager_id"])
        # get the data from the db;
        r.connect("localhost", 28015).repl()
        print("We are printing stuf?")
        # nbtl = r.db("beaconrebuild").table("store").get_all(args["store_manager_id"], index="store_manager_id").count().run()
        genUUID = uuid.uuid4()
        r.db("beaconrebuild").table("store").insert({
          "store_id": str(genUUID),
          "store_manager_id": args["store_manager_id"],
          "beacons": []
        }).run()
        isitthere = r.db("beaconrebuild").table("store").filter({"store_id": str(genUUID)}).limit(1).run()
        return returnJSON(isitthere)
        # pass
