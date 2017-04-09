from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *


class placeorder(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(placeorder, self).__init__()

    ## HTTP GET METHOD
    def get(self):
        pass

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        self.reqparse.add_argument("email", type =  str, required=True, help="No Email Provided")
        self.reqparse.add_argument("message", type =  str, required=False, help="No Message Provided")
        self.reqparse.add_argument("beacons", type =  str, required=True, help="No Beacon Value Provided")
        args = self.reqparse.parse_args();
        initConnection()
        email = args["email"]
        message = args["message"] or ""
        beacons = args["beacons"]

        x = r.db("beaconrebuild").table("beacon_orders").insert({"email": email, "message": message, "beacons": beacons}).run()
        return {"order_id": x["generated_keys"][0]}
