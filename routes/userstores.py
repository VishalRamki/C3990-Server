
##  userbeacons.py
##
##  provides the user's beacons endpoint;
##
##  ENDPOINT: /api/user/stores
##  REST STATES: GET
##
##  Input:
##  user_id - found in the JSON component of the request.
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X GET -d '{"user_id": <string:user_id>}' http://localhost:5000/api/user/stores

##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Custom Helper Functions
from functions import *


class userstores(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userstores, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => ArrayOf<Document>
    ##  Document:
    ##  {
    ##    "beacons": [ArrayOf<String>] ,
    ##    "id":  <string>,
    ##    "lat":  <string>,
    ##    "long": <string>,
    ##    "name": <string>,
    ##    "store_id": <string>,
    ##    "store_manager_id":<string>,
    ##  }
    def get(self):
        self.reqparse.add_argument("store_manager_id", type =  str, required=True, help="No Store Manager ID Provided")
        args = self.reqparse.parse_args();
        initConnection()

        smi = args["store_manager_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("store").filter({"store_manager_id": smi}).run();

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
