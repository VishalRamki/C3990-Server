from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class beacon(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(beacon, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("beacon_id", type =  str, required=True, help="No Beacon ID Provided", location="json")
        args = self.reqparse.parse_args();
        initConnection()
        print("beacon_id: ", args["beacon_id"])
        bid = args["beacon_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("beacon").get_all(bid, index="beacon_id").run()
        print(ntbl)
        return json.dumps(ntbl)

    ## HTTP DELETE METHOD
    def delete(self):
        self.reqparse.add_argument("beacon_id", type=str, required=True, help="Beacon ID Not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").delete().run()
        return {"deleted": args["beacon_id"]}

    ## HTTP PUT METHOD
    def put(self):
        self.reqparse.add_argument("beacon_id", type=str, required=True, help="Beacon ID Not Defined.", location="json")
        self.reqparse.add_argument("update", type=str, required=True, help="JSON Update not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").count().run()
        if (count <= 0):
            return {"message": {
                "content": "There is No Beacon with that ID"
            }}
        else:
            toJSON = json.loads(args["update"].replace("'", '"'))
            print(args["update"])

            r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").update(toJSON).run()
            nv = r.db("beaconrebuild").table("beacon").get_all(args["beacon_id"], index="beacon_id").limit(1).run()
            # print(json.dumps(nv))
            return returnJSON(nv)

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("beacon_uuid", type=str, required=True, help="Beacon ID Not Defined.", location="json")
        self.reqparse.add_argument("beacon_major", type=str, required=True, help="JSON Update not Defined.", location="json")
        self.reqparse.add_argument("beacon_minor", type=str, required=True, help="JSON Update not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        beacon_id = str(uuid.uuid4())
        r.db("beaconrebuild").table("beacon").insert({
          "beacon_id": beacon_id,
          "uuid": args["beacon_uuid"],
          "major": args["beacon_major"],
          "minor": args["beacon_minor"],
          "claimed": "false",
          "owner": "null"
        }).run()
        isitthere = r.db("beaconrebuild").table("beacon").filter({"beacon_id": beacon_id}).limit(1).run()
        return returnJSON(isitthere)
