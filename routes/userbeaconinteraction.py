
##  userbeaconinteraction.py
##
##  provides the user endpoint;
##
##  ENDPOINT: /api/user/interact/beacons
##  REST STATES: GET,POST
##
##  Input:
##  user_id - found in the JSON component of the request.
##  update - found in the JSON component of the request.
##  google_oauth_token - found in the JSON component of the request.
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X GET -d '{"user_id": <string:user_id>}' http://localhost:5000/api/user/interact/beacons
##
##  Example: POST
##  curl -H "Content-Type: application/json" -X POST -d '{"user_id": <string:user_id>}' http://localhost:5000/api/user/interact/beacons

##  Required Flask Packages;;

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class userbeaconinteraction(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(userbeaconinteraction, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure =>
    ##  {
    ##      "message": {
    ##          "content": "That user does not exist"
    ##      }
    ##  }
    ##  onSuccess => Document
    ##  {
    ##      "interacted":  ArrayOf<DocumentInteractBeacon>,
    ##      "id":  <string>,
    ##      "user_id": <string>,
    ##  }
    ##  DocumentInteractBeacon =>
    ##  {
    ##      "beacon_id": <string>,
    ##      "date": <string>,
    ##      "promotion_id": <string>,
    ##      "store_id": <string>
    ##  }
    def get(self):
        self.reqparse.add_argument("user_id", type =  str, required=True, help="No User ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        bid = args["user_id"]
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("user").get_all(args["user_id"], index="user_id").count().run()
        if (count <= 0):
            return {"message": {
                "content": "That User does not exists."
            }}
        else:
            d = r.db("beaconrebuild").table("user").get_all(args["user_id"], index="user_id").run()
            return returnJSON(d)

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ## HTTP PUT METHOD
    def put(self):
        pass

    ##  HTTP POST METHOD
    ##  onFailure => []
    ##      It will either throw an error or the ReqParser will catch any bad inputs;
    ##  onSuccess => []
    ##      the post is merely an update to add to data.
    def post(self):
        self.reqparse.add_argument("user_id", type=str, required=True, help="User ID Not Defined.", location="json")
        self.reqparse.add_argument("update", type=str, required=True, help="Update Not Defined.", location="json")
        args = self.reqparse.parse_args()
        initConnection()

        count = r.db("beaconrebuild").table("user_interactbeacon").get_all(args["user_id"], index="user_id").count().run()
        ## inserts user if this is the first time user is interacting with a beacon.
        if (count <= 0):
            r.db("beaconrebuild").table("user_interactbeacon").insert({"user_id": args["user_id"], "interacted": []}).run()

        toJSON = json.loads(args["update"])
        ## appends the interaction document.
        r.db("beaconrebuild").table("user_interactbeacon").get_all(args["user_id"],index="user_id").update({
            "interacted": r.row["interacted"].default([]).append({"store_id": toJSON["store_id"], "beacon_id": toJSON["beacon_id"], "date": r.now().to_iso8601(), "promotion_id": toJSON["promotion_id"]})
        }).run()

        return []
