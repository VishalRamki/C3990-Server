from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## This needs to go in its own file;
def getBeacons(beaconData, obj):
    nbeacons = r.db("beaconrebuild").table("store_promotion").get_all(obj["store_id"], index="store_id").run()
    print(nbeacons)
    bex = {}
    for beacon in nbeacons:
        bex["beacon_id"] = beacon["beacon_id"]
        bex["promotions"] = beacon["promotions"]
        obj["beacons"].append(bex)
    # ntt = r.db("beaconrebuild").table("store")
    return json.dumps(obj)

def initConnection():
    return r.connect("localhost", 28015).repl()

def returnJSON(isitthere):
    jsons = []
    for i in isitthere:
        jsons.append(i)
    return jsons

# FROM @https://stackoverflow.com/questions/5844672/delete-an-item-from-a-dictionary
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


class user(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(user, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("user_id", type =  str, required=True, help="No User ID Provided", location="json")
        args = self.reqparse.parse_args();
        initConnection()
        bid = args["user_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("user").get_all(bid, index="user_id").run()
        # print(ntbl)
        toJSON = []
        for doc in ntbl:
            toJSON = removekey(doc, "google_oauth_token")
        # print(toJSON)
        return toJSON

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        self.reqparse.add_argument("user_id", type=str, required=True, help="User ID Not Defined.", location="json")
        self.reqparse.add_argument("update", type=str, required=True, help="JSON Update not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("user").get_all(args["user_id"], index="user_id").count().run()
        if (count <= 0):
            return {"message": {
                "content": "There is No User with that ID"
            }}
        else:
            toJSON = json.loads(args["update"].replace("'", '"'))
            r.db("beaconrebuild").table("user").get_all(args["user_id"], index="user_id").update(toJSON).run()
            nv = r.db("beaconrebuild").table("user").get_all(args["user_id"], index="user_id").limit(1).run()
            return returnJSON(nv)

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("g_oauth_token", type =  str, required=True, help="No User Token Provided", location="json")
        args = self.reqparse.parse_args();
        initConnection()
        user_id = str(uuid.uuid4())
        r.db("beaconrebuild").table("user").insert({
          "user_id": user_id,
          "google_oauth_token": args["g_oauth_token"]
        }).run()
        isitthere = r.db("beaconrebuild").table("user").filter({"user_id": user_id}).limit(1).run()
        return returnJSON(isitthere)
