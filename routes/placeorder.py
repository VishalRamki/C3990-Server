
##  placeorder.py
##
##  provides place order endpoint;
##
##  ENDPOINT: /api/order
##  REST STATES: GET
##
##  Input:
##  email: Flask looks in the default locations, including JSON
##  message: Flask looks in the default locations, including JSON
##  beacons: Flask looks in the default locations, including JSON
##  user_id: Flask looks in the default locations, including JSON
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X GET -d '{"user_id": <string:user_id>, "message": <string:message>, "beacons": <string:beacons>}' http://localhost:5000/api/order


##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

##  Required Database
import rethinkdb as r
##  Required Python Packages;
import json, uuid, sys

## Custom Helper Functions
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

    ##  HTTP POST METHOD
    ##  onFailure => []
    ##      this won't return an error unless there is something wrong with the
    ##      database.
    ##  onSuccess => Document
    ##      Document Example:
    ##      {
    ##          "order_id": <string>
    ##      }
    ##
    def post(self):
        self.reqparse.add_argument("email", type =  str, required=True, help="No Email Provided")
        self.reqparse.add_argument("message", type =  str, required=False, help="No Message Provided")
        self.reqparse.add_argument("beacons", type =  str, required=True, help="No Beacon Value Provided")
        self.reqparse.add_argument("user_id", type =  str, required=True, help="No Beacon Value Provided")
        args = self.reqparse.parse_args();
        initConnection()
        ## bind it to local variables;
        email = args["email"]
        message = args["message"] or ""
        beacons = args["beacons"]
        user_id = args["user_id"]

        ## Insert
        x = r.db("beaconrebuild").table("beacon_orders").insert({"email": email, "message": message, "beacons": beacons, "user_id": user_id}).run()
        ## Return the order id.
        return {"order_id": x["generated_keys"][0]}
