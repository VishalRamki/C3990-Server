
##  userbeacons.py
##
##  provides the user's store's promotion endpoint;
##
##  ENDPOINT: /api/user/store/promotion
##  REST STATES: GET
##
##  Input:
##  user_id - found in the JSON component of the request.
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X GET -d '{"user_id": <string:user_id>}' http://localhost:5000/api/user/store/promotion

##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class userstorepromotions(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userstorepromotions, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => ArrayOf<Document>
    ##  Document:
    ## {
    ##     "active":  <string>
    ##     "coupon":  <string>
    ##     "expires":  <string>
    ##     "id":  <string>
    ##     "message":  <string>
    ##     "present":  <string>
    ##     "promotionImage":  <string>
    ##     "promotion_id": <string>
    ##     "store_id": <string>
    ##     "title": <string>
    ## }
    def get(self):
        self.reqparse.add_argument("store_id", type =  str, required=True, help="No Store ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        smi = args["store_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("store_promotion").filter({"store_id": smi}).run();

        iterm = {}
        finalJSON = []
        for item in ntbl:
            finalJSON.append(item)

        return finalJSON

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ## HTTP POST METHOD
    def post(self):
        pass
