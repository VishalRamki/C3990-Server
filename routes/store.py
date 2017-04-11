
##  store.py
##
##  provides the store endpoint;
##
##  ENDPOINT: /api/store
##  REST STATES: GET, DELETE, PUT, POST
##
##  Input:
##  store_id - found in the JSON component of the request or in the other fields.
##  update - found in the json or other fields.
##
##  Example: GET, DELETE
##  curl -H "Content-Type: application/json" -X <GET/DELETE> -d '{"store_id": <string:store_id>}' http://localhost:5000/api/store
##
##  Example: PUT
##  curl -H "Content-Type: application/json" -X PUT -d '{"store_id": "<string:store_id>", "update": <string:json_object_that_stringified>}' http://localhost:5000/api/store
##  NB: "UPDATE" requires a stringified JSON Object which contains the key-value pairs for the fields which you want to update. See the GET Response to see what you can modifiy
##
##  Example: POST
##  curl -H "Content-Type: application/json" -X POST -d '{"store_manager_id": <string:store_manager_id>}' http://localhost:5000/api/store
##  NB: This one simply creates an entry, which has to edited via the merchant interface.

##  Required Flask Packages;;
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.views import MethodView

import rethinkdb as r
import json, uuid, sys

## Customer Helper Functions
from functions import *


class store(MethodView):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        super(store, self).__init__()

    ##  HTTP GET METHOD
    ##  onFailure => []
    ##  onSuccess => [ArrayOf<Document>]
    ##   {
    ##   "beacons": [ArrayOf<String>],
    ##   "id": <string>,
    ##   "lat": <string>,
    ##   "long": <string>,
    ##   "name": <string>,
    ##   "store_id": <string>,
    ##   "store_manager_id": <string>,
    ##   }
    def get(self):
        self.reqparse.add_argument("store_id", type =  str, required=True, help="No Store ID Provided")
        args = self.reqparse.parse_args();
        initConnection()
        print("store_id: ", args["store_id"])
        store_id = args["store_id"]
        # get from rethink;
        ntbl = r.db("beaconrebuild").table("store").get_all(store_id, index="store_id").run()
        iterm = {}
        finalJSON = []
        for item in ntbl:
            finalJSON.append(item)


        return finalJSON

    ##  HTTP DELETE METHOD
    ##  onFailure => []
    ##      Will not happen.
    ##  onSuccess => {
    ##      "deleted": <string:store_id>
    ##  }
    def delete(self):
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store ID Not Defined.")
        args = self.reqparse.parse_args()
        initConnection()
        r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").delete().run()
        return {"deleted": args["store_id"]}

    ##  HTTP PUT METHOD
    ##  onFailure => {
    ##      "message": {
    ##          "content": "There is no Store with that ID"
    ##       }
    ##  }
    ##  onSuccess => Returns the updated Document, enclosed in an array;
    def put(self):
        self.reqparse.add_argument("store_id", type=str, required=True, help="Store ID Not Defined.")
        self.reqparse.add_argument("update", type=str, required=True, help="JSON Update not Defined.")
        args = self.reqparse.parse_args()
        initConnection()
        # check if store_id exists in database;
        count = r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").count().run()
        if (count <= 0):
            return {"message": {
                "content": "There is No Store with that ID"
            }}
        else:
            toJSON = json.loads(args["update"])
            if ("beacons" in toJSON):
                # update the beacon component first because it needs a different query.
                r.db("beaconrebuild").table("store").get_all(args["store_id"],index="store_id").update({
                        "beacons": toJSON["beacons"]
                }).run()
                ## then remove it
                toJSON = removekey(toJSON, "beacons")
            # perform standard update.
            r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").update(toJSON).run()
            nv = r.db("beaconrebuild").table("store").get_all(args["store_id"], index="store_id").limit(1).run()
            return returnJSON(nv)

    ##  HTTP POST METHOD
    ##  onFailure => []
    ##      It will either throw an error or the ReqParser will catch any bad inputs;
    ##  onSuccess => [{}]
    ##      will return the newly created document encased in an array,
    ##      similar to how HTTP GET request was carried out
    def post(self):
        self.reqparse.add_argument("store_manager_id", type=str, required=True, help="Store Manager Not Defined.")
        args = self.reqparse.parse_args()
        print(args["store_manager_id"])
        # get the data from the db;
        r.connect("localhost", 28015).repl()
        print("We are printing stuf?")
        # nbtl = r.db("beaconrebuild").table("store").get_all(args["store_manager_id"], index="store_manager_id").count().run()
        genUUID = uuid.uuid4()
        r.db("beaconrebuild").table("store").insert({
          "store_id": str(genUUID),
          "store_manager_id": args["store_manager_id"],
          "beacons": [],
          "long": "",
          "lat": ""
        }).run()
        isitthere = r.db("beaconrebuild").table("store").filter({"store_id": str(genUUID)}).limit(1).run()
        return returnJSON(isitthere)
        # pass
