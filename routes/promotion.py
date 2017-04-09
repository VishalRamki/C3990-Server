from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class promotion(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(promotion, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        self.reqparse.add_argument("promotion_id", type =  str, required=True, help="No Promotion ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        # test value: 61229004-7480-44ab-b396-e5eee8ba0751
        nv = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id":args["promotion_id"] }).run()
        return returnJSON(nv)

    ## HTTP DELETE METHOD
    def delete(self):
        self.reqparse.add_argument("promotion_id", type =  str, required=True, help="No Promotion ID Provided")
        args = self.reqparse.parse_args()
        initConnection()
        r.db("beaconrebuild").table("store_promotion").filter({"promotion_id":args["promotion_id"] }).delete().run()
        return {"deleted": args["promotion_id"]}

    ## HTTP PUT METHOD
    def put(self):
        self.reqparse.add_argument("promotion_id", type =  str, required=True, help="No Promotion ID Provided")
        self.reqparse.add_argument("update", type=str, required=True, help="JSON Update not Defined.")
        args = self.reqparse.parse_args();
        initConnection()
        # check if it exists;
        count = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": args["promotion_id"]}).count().run()
        if (count <= 0):
            return {"message": {
                "content": "There is No Promotion with that ID"
            }}
        else:
            ## create object from json string;
            toJSON = json.loads(args["update"])

            ## check if update contains active;
            if ((("active" in toJSON) or toJSON["active"] == "yes") and ("store_id" in toJSON)):
                r.db("beaconrebuild").table("store_promotion").filter({"store_id": toJSON["store_id"]}).update({"active": "no"}).run()

            ## uhhh do things.
            r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": args["promotion_id"]}).update(toJSON).run()
            nv = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": args["promotion_id"]}).limit(1).run()
            return returnJSON(nv)
        pass

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("title", type=str, required=True, help="Title not Defined.")
        self.reqparse.add_argument("message", type=str, required=True, help="Message not Defined.")
        self.reqparse.add_argument("coupon", type=str, required=True, help="Coupon not Defined.")
        self.reqparse.add_argument("present", type=str, required=False, help="Present not Defined.")
        self.reqparse.add_argument("expires", type=str, required=True, help="Expires not Defined.")
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store not Defined.")
        self.reqparse.add_argument("beacon_id", type=str, required=False, help="Beacon not Defined.")
        self.reqparse.add_argument("active", type=str, required=True, help="Activity not Defined.")
        self.reqparse.add_argument("promotionImage", type=str, required=False, help="Image not Defined.")
        args = self.reqparse.parse_args()
        initConnection()

        ## Check if new active;wegwe
        if (args["active"] == "yes"):
            r.db("beaconrebuild").table("store_promotion").filter({"store_id": args["store_id"]}).update({"active": "no"}).run()

        ## generate new Promotion UUID
        promo = str(uuid.uuid4())
        r.db("beaconrebuild").table("store_promotion").insert({
          "promotion_id": promo,
          "message": args["message"],
          "title": args["title"],
          "coupon": args["coupon"],
          "present": "",
          "expires": args["expires"],
          "store_id": args["store_id"],
          "promotionImage": args["promotionImage"],
        #   "beacon_id": "",
          "active": args["active"]
        }).run()
        isitthere = r.db("beaconrebuild").table("store_promotion").filter({"promotion_id": promo}).limit(1).run()
        return returnJSON(isitthere)
