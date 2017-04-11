
##  user.py
##
##  provides the user endpoint;
##
##  ENDPOINT: /api/user
##  REST STATES: GET, PUT, POST
##
##  Input:
##  user_id - found in the JSON component of the request.
##  update - found in the JSON component of the request.
##  google_oauth_token - found in the JSON component of the request.
##
##  Example: GET
##  curl -H "Content-Type: application/json" -X GET -d '{"user_id": <string:user_id>}' http://localhost:5000/api/user
##
##  Example: PUT
##  curl -H "Content-Type: application/json" -X PUT -d '{"user_id": "<string:user_id>", "update": <string:json_object_that_stringified>}' http://localhost:5000/api/user
##  NB: "UPDATE" requires a stringified JSON Object which contains the key-value pairs for the fields which you want to update. See the GET Response to see what you can modifiy
##
##  Example: POST
##  curl -H "Content-Type: application/json" -X POST -d '{"google_oauth_token": <string:google_oauth_token>}' http://localhost:5000/api/user

##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *

class user(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(user, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => Document
    ##  {
    ##      "google_oauth_token":  <string>,
    ##      "id":  <string>,
    ##      "user_id": <string>,
    ##  }
    def get(self):
        self.reqparse.add_argument("user_id", type =  str, required=True, help="No google_oauth_token Provided", location="json")
        args = self.reqparse.parse_args();
        initConnection()
        bid = args["user_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("user").get_all(bid, index="user_id").run()

        toJSON = []
        for doc in ntbl:
            toJSON = removekey(doc, "google_oauth_token")

        return toJSON

    ## HTTP DELETE METHOD
    def delete(self):
        pass

    ##  HTTP PUT METHOD
    ##  onFailure => {
    ##      "message": {
    ##          "content": "There is no User with that ID"
    ##       }
    ##  }
    ##  onSuccess => Returns the updated Document, enclosed in an array;
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

    ##  HTTP POST METHOD
    ##  onFailure => []
    ##      It will either throw an error or the ReqParser will catch any bad inputs;
    ##  onSuccess => [{}]
    ##      will return the newly created document encased in an array,
    ##      similar to how HTTP GET request was carried out
    def post(self):
        self.reqparse.add_argument("google_oauth_token", type =  str, required=True, help="No User Token Provided")
        args = self.reqparse.parse_args();
        initConnection()
        user_id = str(uuid.uuid4())
        r.db("beaconrebuild").table("user").insert({
          "user_id": user_id,
          "google_oauth_token": args["google_oauth_token"]
        }).run()
        isitthere = r.db("beaconrebuild").table("user").filter({"user_id": user_id}).limit(1).run()
        return returnJSON(isitthere)
