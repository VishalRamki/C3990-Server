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
    return json.dumps(jsons)

# FROM @https://stackoverflow.com/questions/5844672/delete-an-item-from-a-dictionary
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


class promotion(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(promotion, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("promotion_id", type =  str, required=True, help="No Promotion ID Provided", location="json")
        args = self.reqparse.parse_args();
        initConnection()
        # test value: 61229004-7480-44ab-b396-e5eee8ba0751
        nv = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id":args["promotion_id"] }).run()
        return returnJSON(nv)

    ## HTTP DELETE METHOD
    def delete(self):
        self.reqparse.add_argument("promotion_id", type =  str, required=True, help="No Promotion ID Provided", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        r.db("beaconrebuild").table("store_promotion").filter({"promotion_id":args["promotion_id"] }).delete().run()
        return {"deleted": args["promotion_id"]}

    ## HTTP PUT METHOD
    def put(self):
        self.reqparse.add_argument("promotion_id", type =  str, required=True, help="No Promotion ID Provided", location="json")
        self.reqparse.add_argument("update", type=str, required=True, help="JSON Update not Defined.", location="json")
        args = self.reqparse.parse_args();
        initConnection()
        # check if it exists;
        count = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": args["promotion_id"]}).count().run()
        if (count <= 0):
            return {"message": {
                "content": "There is No Promotion with that ID"
            }}
        else:
            toJSON = json.loads(args["update"].replace("'", '"'))
            r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": args["promotion_id"]}).update(removekey(toJSON, "beacons")).run()
            nv = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": args["promotion_id"]}).limit(1).run()
            return returnJSON(nv)
        pass

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("title", type=str, required=True, help="Title not Defined.", location="json")
        self.reqparse.add_argument("message", type=str, required=True, help="Message not Defined.", location="json")
        self.reqparse.add_argument("coupon", type=str, required=True, help="Coupon not Defined.", location="json")
        self.reqparse.add_argument("present", type=str, required=True, help="Present not Defined.", location="json")
        self.reqparse.add_argument("expires", type=str, required=True, help="Expires not Defined.", location="json")
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store not Defined.", location="json")
        self.reqparse.add_argument("beacon_id", type=str, required=True, help="Beacon not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()
        promo = str(uuid.uuid4())
        r.db("beaconrebuild").table("store_promotion").insert({
          "promotion_id": promo,
          "message": args["message"],
          "title": args["title"],
          "coupon": args["coupon"],
          "present": args["present"],
          "expires": args["expires"],
          "store_id": args["store_id"],
          "beacon_id": args["beacon_id"]
        }).run()
        isitthere = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": promo}).limit(1).run()
        return returnJSON(isitthere)
